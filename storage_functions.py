from __future__ import annotations

import json
import logging

import azure.functions as func

from src.csv_logic import normalize_csv
from src.order_logic import ValidationError, normalize_order, process_normalized_order


storage_blueprint = func.Blueprint()


def json_response(payload: dict, status_code: int) -> func.HttpResponse:
    return func.HttpResponse(
        body=json.dumps(payload),
        status_code=status_code,
        mimetype="application/json",
    )


@storage_blueprint.function_name(name="SubmitOrder")
@storage_blueprint.route(
    route="orders",
    methods=["POST"],
    auth_level=func.AuthLevel.ANONYMOUS,
)
@storage_blueprint.queue_output(
    arg_name="order_message",
    queue_name="raw-orders",
    connection="DataStorage",
)
def submit_order(
    req: func.HttpRequest,
    order_message: func.Out[str],
) -> func.HttpResponse:
    """Validate an HTTP order and send it to local Queue Storage."""
    try:
        normalized = normalize_order(req.get_json())
    except (ValueError, ValidationError) as exc:
        return json_response({"error": str(exc)}, 400)

    order_message.set(json.dumps(normalized))
    return json_response(
        {"status": "accepted", "order_id": normalized["order_id"]},
        202,
    )


@storage_blueprint.function_name(name="ProcessOrder")
@storage_blueprint.queue_trigger(
    arg_name="message",
    queue_name="raw-orders",
    connection="DataStorage",
)
@storage_blueprint.blob_output(
    arg_name="output_blob",
    path="processed-orders/{rand-guid}.json",
    connection="DataStorage",
)
def process_order(
    message: func.QueueMessage,
    output_blob: func.Out[str],
) -> None:
    """Process one queue message and write a JSON blob."""
    payload = json.loads(message.get_body().decode("utf-8"))
    processed = process_normalized_order(payload)
    output_blob.set(json.dumps(processed, indent=2))
    logging.info("Processed order %s.", processed["order_id"])


@storage_blueprint.function_name(name="ProcessCsv")
@storage_blueprint.blob_trigger(
    arg_name="input_blob",
    path="landing/{name}.csv",
    connection="DataStorage",
    source="LogsAndContainerScan",
)
@storage_blueprint.blob_output(
    arg_name="curated_blob",
    path="curated/{name}.jsonl",
    connection="DataStorage",
)
def process_csv(
    input_blob: func.InputStream,
    curated_blob: func.Out[str],
) -> None:
    """Normalize valid CSV rows and log rejected rows."""
    jsonl, rejected = normalize_csv(input_blob.read())
    curated_blob.set(jsonl)

    for rejected_row in rejected:
        logging.warning("Rejected CSV row: %s", json.dumps(rejected_row))

    logging.info(
        "Processed %s with %d rejected rows.",
        input_blob.name,
        len(rejected),
    )

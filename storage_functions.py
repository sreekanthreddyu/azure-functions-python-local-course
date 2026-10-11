from __future__ import annotations  # Lets type hints be stored without resolving them immediately.

import json  # Converts order data to and from JSON text for queue and blob messages.
import logging  # Writes processing details and rejected CSV rows to the Functions logs.

import azure.functions as func  # Provides the Functions blueprint, HTTP, queue, blob, and stream types.

from src.csv_logic import normalize_csv  # Connects uploaded CSV bytes to reusable CSV-cleaning logic.
from src.order_logic import ValidationError, normalize_order, process_normalized_order  # Reuses order checks and processing outside the Functions bindings.


storage_blueprint = func.Blueprint()  # Collects storage-related handlers so the main app can register them together.


def json_response(payload: dict, status_code: int) -> func.HttpResponse:  # Shares one JSON response format across the HTTP handlers here.
    return func.HttpResponse(  # Builds the HTTP response returned to the caller.
        body=json.dumps(payload),  # Converts the response dictionary into JSON text.
        status_code=status_code,  # Uses the success or error code chosen by the handler.
        mimetype="application/json",  # Tells the caller that the response body is JSON.
    )  # Finishes creating and returns the response.


@storage_blueprint.function_name(name="SubmitOrder")  # Gives this handler a stable name in the Functions host.
@storage_blueprint.route(  # Connects an HTTP route to the handler below.
    route="orders",  # Sets the route path to /api/orders.
    methods=["POST"],  # Accepts order data sent in a POST request.
    auth_level=func.AuthLevel.ANONYMOUS,  # Allows local callers without a function key.
)  # Finishes the HTTP trigger binding.
@storage_blueprint.queue_output(  # Connects the handler's output parameter to Azure Queue Storage.
    arg_name="order_message",  # Matches this binding to the handler parameter with the same name.
    queue_name="raw-orders",  # Sends each accepted order to the raw-orders queue.
    connection="DataStorage",  # Reads the storage connection setting from local or app configuration.
)  # Finishes the queue output binding.
def submit_order(
    req: func.HttpRequest,  # Receives the incoming HTTP request matched by the route above.
    order_message: func.Out[str],  # Receives the queue output handle matched by arg_name above.
) -> func.HttpResponse:  # Returns an HTTP response to the caller.
    """Validate an HTTP order and send it to local Queue Storage."""  # Describes how the HTTP and queue bindings work together.
    try:  # Handles malformed JSON and expected order validation errors.
        normalized = normalize_order(req.get_json())  # Parses the request JSON and applies the shared order rules.
    except (ValueError, ValidationError) as exc:  # Catches JSON parsing errors and invalid order data.
        return json_response({"error": str(exc)}, 400)  # Reports invalid input without writing a queue message.

    order_message.set(json.dumps(normalized))  # Places the valid order on the queue through the output binding.
    return json_response(  # Confirms acceptance after setting the queue output.
        {"status": "accepted", "order_id": normalized["order_id"]},  # Returns status and the order identifier.
        202,  # Uses HTTP 202 to say the order was accepted for later processing.
    )  # Finishes and returns the acceptance response.


@storage_blueprint.function_name(name="ProcessOrder")  # Gives the queue-processing handler a stable host name.
@storage_blueprint.queue_trigger(  # Starts this function when a message arrives in the configured queue.
    arg_name="message",  # Matches the queue input binding to the handler parameter named message.
    queue_name="raw-orders",  # Reads messages from the same queue written by SubmitOrder.
    connection="DataStorage",  # Uses the configured local or app storage connection.
)  # Finishes the queue trigger binding.
@storage_blueprint.blob_output(  # Connects an output parameter to Blob Storage.
    arg_name="output_blob",  # Matches this output binding to the handler parameter named output_blob.
    path="processed-orders/{rand-guid}.json",  # Writes each processed order to a blob with a generated unique name.
    connection="DataStorage",  # Uses the same configured storage account as the queue binding.
)  # Finishes the blob output binding.
def process_order(
    message: func.QueueMessage,  # Receives the queue message that caused this function to run.
    output_blob: func.Out[str],  # Receives the blob output handle matched by arg_name above.
) -> None:  # Returns no HTTP response because the queue trigger runs in the background.
    """Process one queue message and write a JSON blob."""  # Describes the queue-to-blob flow.
    payload = json.loads(message.get_body().decode("utf-8"))  # Decodes the message bytes and parses its JSON content.
    processed = process_normalized_order(payload)  # Applies the shared order-processing logic to the message data.
    output_blob.set(json.dumps(processed, indent=2))  # Writes the processed order as readable JSON to the bound blob path.
    logging.info("Processed order %s.", processed["order_id"])  # Records which order was processed.


@storage_blueprint.function_name(name="ProcessCsv")  # Gives the CSV handler a stable host name.
@storage_blueprint.blob_trigger(  # Starts this function when a matching input blob is detected.
    arg_name="input_blob",  # Matches the input binding to the handler parameter named input_blob.
    path="landing/{name}.csv",  # Watches CSV files in landing and captures each filename as name.
    connection="DataStorage",  # Uses the configured local or app storage connection.
    source="LogsAndContainerScan",  # Uses blob logs plus container scans to find changed blobs.
)  # Finishes the blob trigger binding.
@storage_blueprint.blob_output(  # Connects the cleaned CSV result to an output blob.
    arg_name="curated_blob",  # Matches the output binding to the handler parameter named curated_blob.
    path="curated/{name}.jsonl",  # Writes JSON Lines under curated using the input file's captured name.
    connection="DataStorage",  # Uses the same configured storage account as the input binding.
)  # Finishes the blob output binding.
def process_csv(
    input_blob: func.InputStream,  # Receives the file content and metadata from the blob trigger.
    curated_blob: func.Out[str],  # Receives the output handle matched by the curated blob binding.
) -> None:  # Returns no HTTP response because the blob trigger runs in the background.
    """Normalize valid CSV rows and log rejected rows."""  # Describes how the blob input is transformed into output.
    jsonl, rejected = normalize_csv(input_blob.read())  # Reads the CSV bytes and separates cleaned output from rejected rows.
    curated_blob.set(jsonl)  # Writes the cleaned rows to the output blob through its binding.

    for rejected_row in rejected:  # Visits each row that the shared CSV logic could not accept.
        logging.warning("Rejected CSV row: %s", json.dumps(rejected_row))  # Logs the rejected row for troubleshooting.

    logging.info(  # Records a summary after processing the input file.
        "Processed %s with %d rejected rows.",  # Formats the input name and rejected-row count into the log message.
        input_blob.name,  # Supplies the name of the CSV blob that triggered this run.
        len(rejected),  # Supplies the number of rows that were rejected.
    )  # Finishes writing the summary log entry.

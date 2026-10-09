from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone

import azure.functions as func

from src.order_logic import ValidationError, normalize_order


app = func.FunctionApp()


def json_response(payload: dict, status_code: int) -> func.HttpResponse:
    return func.HttpResponse(
        body=json.dumps(payload),
        status_code=status_code,
        mimetype="application/json",
    )


@app.function_name(name="Health")
@app.route(route="health", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def health(req: func.HttpRequest) -> func.HttpResponse:
    """Small HTTP trigger that does not require Azurite."""
    logging.info("Health endpoint called.")
    return json_response({"status": "ok", "mode": "local"}, 200)


@app.function_name(name="ValidateOrder")
@app.route(
    route="orders/validate",
    methods=["POST"],
    auth_level=func.AuthLevel.ANONYMOUS,
)
def validate_order(req: func.HttpRequest) -> func.HttpResponse:
    """Validate an order and return its normalized representation."""
    try:
        payload = req.get_json()
        return json_response(normalize_order(payload), 200)
    except (ValueError, ValidationError) as exc:
        return json_response({"error": str(exc)}, 400)


@app.function_name(name="TimerHeartbeat")
@app.timer_trigger(
    schedule="0 */1 * * * *",
    arg_name="timer",
    run_on_startup=False,
    use_monitor=False,
)
def timer_heartbeat(timer: func.TimerRequest) -> None:
    """Run once per minute without persistent schedule monitoring."""
    if timer.past_due:
        logging.warning("TimerHeartbeat is past due.")
    logging.info("TimerHeartbeat ran at %s", datetime.now(timezone.utc).isoformat())


if os.getenv("ENABLE_STORAGE_FUNCTIONS", "false").lower() == "true":
    from storage_functions import storage_blueprint

    app.register_functions(storage_blueprint)

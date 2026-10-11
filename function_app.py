from __future__ import annotations  # Lets type hints be stored without resolving them immediately.

import json  # Provides JSON conversion used when building HTTP response bodies.
import logging  # Provides log messages that appear while the Functions app runs.
import os  # Reads environment settings that control optional app features.
from datetime import datetime, timezone  # Supplies the current time in UTC for the heartbeat log.

import azure.functions as func  # Gives this file the Azure Functions app, trigger, and request types.

from src.order_logic import ValidationError, normalize_order  # Connects HTTP input to reusable order-validation logic.


app = func.FunctionApp()  # Creates the app object where this file registers its functions.


def json_response(payload: dict, status_code: int) -> func.HttpResponse:  # Shares one JSON response format across HTTP handlers.
    return func.HttpResponse(  # Builds the HTTP response Azure Functions sends to the caller.
        body=json.dumps(payload),  # Converts the Python dictionary into JSON text for the response body.
        status_code=status_code,  # Uses the caller-provided HTTP result code, such as 200 or 400.
        mimetype="application/json",  # Tells the caller that the response body contains JSON.
    )  # Finishes creating and returns the response object.


@app.function_name(name="Health")  # Gives this function a stable name in the Functions host.
@app.route(route="health", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)  # Binds GET /api/health requests to the handler below.
def health(req: func.HttpRequest) -> func.HttpResponse:  # Defines the HTTP handler; Azure passes its request as req.
    """Small HTTP trigger that does not require Azurite."""  # Documents that this endpoint works without local storage.
    logging.info("Health endpoint called.")  # Records that a caller reached this endpoint.
    return json_response({"status": "ok", "mode": "local"}, 200)  # Sends a successful JSON health result through the shared helper.


@app.function_name(name="ValidateOrder")  # Gives the order-validation handler its host-visible name.
@app.route(  # Connects an HTTP route to the function defined immediately below.
    route="orders/validate",  # Sets the route path to /api/orders/validate.
    methods=["POST"],  # Accepts POST requests so the caller can send an order body.
    auth_level=func.AuthLevel.ANONYMOUS,  # Allows local callers without a function key.
)  # Completes the route binding for this handler.
def validate_order(req: func.HttpRequest) -> func.HttpResponse:  # Receives the POST request and returns an HTTP response.
    """Validate an order and return its normalized representation."""  # Describes the work performed by this handler.
    try:  # Starts handling expected input and validation failures safely.
        payload = req.get_json()  # Parses the request body as JSON for the order logic.
        return json_response(normalize_order(payload), 200)  # Validates and normalizes the order, then returns success JSON.
    except (ValueError, ValidationError) as exc:  # Catches malformed JSON or order rules reported by the shared logic.
        return json_response({"error": str(exc)}, 400)  # Turns those input problems into a clear HTTP 400 response.


@app.function_name(name="TimerHeartbeat")  # Gives the scheduled handler its host-visible name.
@app.timer_trigger(  # Binds a schedule to the function defined immediately below.
    schedule="0 */1 * * * *",  # Runs at the start of every minute using a six-part timer schedule.
    arg_name="timer",  # Tells the host to pass the timer event into the timer parameter.
    run_on_startup=False,  # Avoids running an extra time just because the host starts.
    use_monitor=False,  # Avoids persistent schedule tracking for this simple local example.
)  # Completes the timer binding for this handler.
def timer_heartbeat(timer: func.TimerRequest) -> None:  # Handles each timer event; the host supplies its schedule details.
    """Run once per minute without persistent schedule monitoring."""  # Summarizes the timer's behavior.
    if timer.past_due:  # Checks whether this timer event arrived later than its scheduled time.
        logging.warning("TimerHeartbeat is past due.")  # Warns in logs when the scheduled run was late.
    logging.info("TimerHeartbeat ran at %s", datetime.now(timezone.utc).isoformat())  # Logs the actual run time in UTC.


if os.getenv("ENABLE_STORAGE_FUNCTIONS", "false").lower() == "true":  # Enables storage functions only when the setting says true, ignoring letter case.
    from storage_functions import storage_blueprint  # Loads the optional storage handlers only when enabled.

    app.register_functions(storage_blueprint)  # Adds those handlers to the same app used by the HTTP and timer functions.

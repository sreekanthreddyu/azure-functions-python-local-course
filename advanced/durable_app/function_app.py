from __future__ import annotations  # Lets type hints be stored without resolving them immediately.

from typing import Any  # Lets the order dictionaries contain values of different types.

import azure.durable_functions as df  # Provides the Durable app, orchestration, and client types.
import azure.functions as func  # Provides HTTP request and response types for the starter endpoint.


app = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)  # Creates the app that registers HTTP, orchestration, and activity functions.


@app.route(route="orchestrations/orders", methods=["POST"])  # Binds POST /api/orchestrations/orders to the starter function below.
@app.durable_client_input(client_name="client")  # Supplies the Durable client as the starter function's client parameter.
async def start_order_orchestration(
    req: func.HttpRequest,  # Receives the HTTP request matched by the route above.
    client: df.DurableOrchestrationClient,  # Receives the orchestration client provided by the Durable input binding.
) -> func.HttpResponse:  # Returns a response that starts the workflow or reports a bad request.
    try:  # Handles a request body that is not valid JSON.
        orders = req.get_json()  # Parses the incoming request body into Python data.
    except ValueError:  # Runs when the request body cannot be parsed as JSON.
        return func.HttpResponse("Request body must be valid JSON.", status_code=400)  # Tells the caller to send valid JSON.

    if not isinstance(orders, list) or not orders:  # Requires the parsed data to be a list containing at least one order.
        return func.HttpResponse(  # Rejects the request before creating any orchestration work.
            "Request body must be a nonempty JSON array.",  # Explains the expected request shape.
            status_code=400,  # Marks the request as invalid.
        )  # Finishes and returns the validation response.

    instance_id = await client.start_new("order_orchestrator", None, orders)  # Starts the named orchestration and gives it the list of orders.
    return client.create_check_status_response(req, instance_id)  # Returns URLs the caller can use to check this workflow's status.


@app.orchestration_trigger(context_name="context")  # Binds Durable orchestration events to the context parameter below.
def order_orchestrator(context: df.DurableOrchestrationContext):  # Coordinates the activity functions for one workflow instance.
    orders = context.get_input()  # Gets the order list passed by start_order_orchestration.
    tasks = [context.call_activity("calculate_total", order) for order in orders]  # Creates one calculation activity task for each order.
    calculated = yield context.task_all(tasks)  # Waits for all calculation tasks and gathers their results.
    summary = yield context.call_activity("summarize_orders", calculated)  # Sends all calculated orders to the summary activity and waits for its result.
    return summary  # Completes the orchestration with the final summary.


@app.activity_trigger(input_name="order")  # Binds activity input data to the order parameter below.
def calculate_total(order: dict) -> dict[str, Any]:  # Calculates the total for one order in the workflow.
    quantity = int(order["quantity"])  # Reads the order quantity and makes sure it is an integer.
    unit_price_cents = int(order["unit_price_cents"])  # Reads the unit price as integer cents to avoid floating-point money.
    return {  # Sends the calculated fields back to the orchestrator.
        "order_id": str(order["order_id"]),  # Keeps the order identifier in the result.
        "total_cents": quantity * unit_price_cents,  # Multiplies quantity by unit price and keeps the amount in cents.
    }  # Finishes and returns this order's calculation result.


@app.activity_trigger(input_name="orders")  # Binds the calculated-order list to the orders parameter below.
def summarize_orders(orders: list) -> dict[str, Any]:  # Combines the activity results into one workflow summary.
    return {  # Sends the final summary back to the orchestrator.
        "order_count": len(orders),  # Counts the calculated orders.
        "grand_total_cents": sum(order["total_cents"] for order in orders),  # Adds each order total while keeping money in cents.
        "orders": orders,  # Includes each calculation so the caller can inspect the individual results.
    }  # Finishes and returns the summary dictionary.

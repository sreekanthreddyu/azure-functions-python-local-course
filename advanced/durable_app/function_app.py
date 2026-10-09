from __future__ import annotations

from typing import Any

import azure.durable_functions as df
import azure.functions as func


app = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="orchestrations/orders", methods=["POST"])
@app.durable_client_input(client_name="client")
async def start_order_orchestration(
    req: func.HttpRequest,
    client: df.DurableOrchestrationClient,
) -> func.HttpResponse:
    try:
        orders = req.get_json()
    except ValueError:
        return func.HttpResponse("Request body must be valid JSON.", status_code=400)

    if not isinstance(orders, list) or not orders:
        return func.HttpResponse(
            "Request body must be a nonempty JSON array.",
            status_code=400,
        )

    instance_id = await client.start_new("order_orchestrator", None, orders)
    return client.create_check_status_response(req, instance_id)


@app.orchestration_trigger(context_name="context")
def order_orchestrator(context: df.DurableOrchestrationContext):
    orders = context.get_input()
    tasks = [context.call_activity("calculate_total", order) for order in orders]
    calculated = yield context.task_all(tasks)
    summary = yield context.call_activity("summarize_orders", calculated)
    return summary


@app.activity_trigger(input_name="order")
def calculate_total(order: dict[str, Any]) -> dict[str, Any]:
    quantity = int(order["quantity"])
    unit_price_cents = int(order["unit_price_cents"])
    return {
        "order_id": str(order["order_id"]),
        "total_cents": quantity * unit_price_cents,
    }


@app.activity_trigger(input_name="orders")
def summarize_orders(orders: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "order_count": len(orders),
        "grand_total_cents": sum(order["total_cents"] for order in orders),
        "orders": orders,
    }

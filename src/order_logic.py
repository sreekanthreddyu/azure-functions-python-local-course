from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any


class ValidationError(ValueError):
    """Raised when an incoming order does not meet the data contract."""


REQUIRED_FIELDS = {"order_id", "quantity", "unit_price"}


def normalize_order(payload: Any) -> dict[str, Any]:
    """Validate and normalize an order without using Azure-specific types."""
    if not isinstance(payload, dict):
        raise ValidationError("The request body must be a JSON object.")

    missing = sorted(REQUIRED_FIELDS - payload.keys())
    if missing:
        raise ValidationError(f"Missing required fields: {', '.join(missing)}.")

    order_id = str(payload["order_id"]).strip()
    if not order_id:
        raise ValidationError("order_id must not be empty.")

    quantity = payload["quantity"]
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
        raise ValidationError("quantity must be a positive integer.")

    try:
        price = Decimal(str(payload["unit_price"]))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValidationError("unit_price must be a valid number.") from exc

    if not price.is_finite() or price < 0:
        raise ValidationError("unit_price must be zero or greater.")

    rounded_price = price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if rounded_price != price:
        raise ValidationError("unit_price must have no more than two decimal places.")

    unit_price_cents = int(rounded_price * 100)

    return {
        "order_id": order_id,
        "quantity": quantity,
        "unit_price_cents": unit_price_cents,
        "total_cents": quantity * unit_price_cents,
        "received_at": datetime.now(timezone.utc).isoformat(),
    }


def process_normalized_order(payload: Any) -> dict[str, Any]:
    """Create the processed representation consumed by downstream systems."""
    if not isinstance(payload, dict):
        raise ValidationError("The queue message must contain a JSON object.")

    required = {"order_id", "quantity", "unit_price_cents", "total_cents"}
    missing = sorted(required - payload.keys())
    if missing:
        raise ValidationError(f"Queue message is missing: {', '.join(missing)}.")

    result = dict(payload)
    result["status"] = "processed"
    result["processed_at"] = datetime.now(timezone.utc).isoformat()
    return result

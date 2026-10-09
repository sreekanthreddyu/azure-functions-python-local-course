from __future__ import annotations

import csv
import io
import json
from typing import Any

from src.order_logic import ValidationError, normalize_order


def normalize_csv(content: bytes) -> tuple[str, list[dict[str, Any]]]:
    """Convert CSV bytes to JSON Lines and return rejected row details."""
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValidationError("The CSV file must use UTF-8 encoding.") from exc

    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames is None:
        raise ValidationError("The CSV file must contain a header row.")

    required = {"order_id", "quantity", "unit_price"}
    missing_columns = sorted(required - set(reader.fieldnames))
    if missing_columns:
        raise ValidationError(
            f"The CSV header is missing: {', '.join(missing_columns)}."
        )

    accepted: list[str] = []
    rejected: list[dict[str, Any]] = []

    for row_number, row in enumerate(reader, start=2):
        try:
            candidate = {
                "order_id": row["order_id"],
                "quantity": int(row["quantity"]),
                "unit_price": row["unit_price"],
            }
            accepted.append(json.dumps(normalize_order(candidate), sort_keys=True))
        except (ValidationError, TypeError, ValueError) as exc:
            rejected.append(
                {"row_number": row_number, "reason": str(exc), "row": row}
            )

    jsonl = "\n".join(accepted)
    if jsonl:
        jsonl += "\n"
    return jsonl, rejected

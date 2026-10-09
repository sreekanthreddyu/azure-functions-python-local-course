import pytest

from src.order_logic import ValidationError, normalize_order, process_normalized_order


def test_normalize_order_calculates_integer_cents() -> None:
    result = normalize_order(
        {"order_id": "A1001", "quantity": 3, "unit_price": "19.95"}
    )

    assert result["unit_price_cents"] == 1995
    assert result["total_cents"] == 5985


@pytest.mark.parametrize(
    "payload",
    [
        [],
        {},
        {"order_id": "A", "quantity": 0, "unit_price": "10.00"},
        {"order_id": "A", "quantity": True, "unit_price": "10.00"},
        {"order_id": "A", "quantity": 1, "unit_price": "10.001"},
        {"order_id": "A", "quantity": 1, "unit_price": "NaN"},
    ],
)
def test_normalize_order_rejects_bad_input(payload) -> None:
    with pytest.raises(ValidationError):
        normalize_order(payload)


def test_process_normalized_order_marks_completion() -> None:
    normalized = normalize_order(
        {"order_id": "A1002", "quantity": 2, "unit_price": "4.50"}
    )
    result = process_normalized_order(normalized)

    assert result["status"] == "processed"
    assert "processed_at" in result

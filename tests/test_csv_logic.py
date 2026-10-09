import json

from src.csv_logic import normalize_csv


def test_normalize_csv_keeps_valid_rows_and_reports_bad_rows() -> None:
    content = (
        b"order_id,quantity,unit_price\n"
        b"A1001,2,12.50\n"
        b"A1002,0,5.00\n"
    )

    jsonl, rejected = normalize_csv(content)
    records = [json.loads(line) for line in jsonl.splitlines()]

    assert len(records) == 1
    assert records[0]["total_cents"] == 2500
    assert rejected[0]["row_number"] == 3

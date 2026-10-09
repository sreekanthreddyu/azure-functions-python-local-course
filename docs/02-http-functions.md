# 2. First HTTP functions

## Objective

Call Python code through a local HTTP endpoint.

Start the host:

```powershell
.\scripts\start.ps1
```

Open another PowerShell terminal.

## Call the health function

```powershell
Invoke-RestMethod http://localhost:7071/api/health
```

Expected:

```json
{"status":"ok","mode":"local"}
```

Read `health()` in `function_app.py`.

The `@app.route` decorator creates an HTTP trigger. The function accepts `func.HttpRequest` and returns `func.HttpResponse`.

## Validate an order

```powershell
$body = Get-Content .\sample_data\order.json -Raw
Invoke-RestMethod -Method Post `
  -Uri http://localhost:7071/api/orders/validate `
  -ContentType application/json `
  -Body $body
```

The response includes integer-cent values:

```json
{
  "order_id": "A1001",
  "quantity": 3,
  "unit_price_cents": 1995,
  "total_cents": 5985
}
```

The exact timestamps will differ.

## Cause a validation failure

```powershell
curl.exe -i -X POST http://localhost:7071/api/orders/validate `
  -H "Content-Type: application/json" `
  --data-binary '{"order_id":"BAD","quantity":0,"unit_price":"10.00"}'
```

Expected: HTTP `400`.

## Why business logic is in `src/`

`function_app.py` converts HTTP input and output. `src/order_logic.py` contains validation and calculations.

This separation lets you test the business logic without starting Azure Functions.

## Exercise

Add an optional `customer_id` field. Trim whitespace if it is supplied. Add a test before changing the implementation.

## Checkpoint

Explain why an HTTP trigger should return `400` for bad input rather than allowing an unhandled exception to return `500`.

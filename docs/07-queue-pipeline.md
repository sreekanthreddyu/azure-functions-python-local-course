# 7. HTTP-to-queue-to-blob pipeline

## Objective

Decouple order submission from order processing.

```mermaid
flowchart LR
    A[POST /api/orders] --> B[SubmitOrder]
    B --> C[raw-orders queue]
    C --> D[ProcessOrder]
    D --> E[processed-orders blob]
```

## Enable the functions

Start Azurite. Then set these values in `local.settings.json`:

```json
"AzureWebJobsStorage": "UseDevelopmentStorage=true",
"ENABLE_STORAGE_FUNCTIONS": "true"
```

Restart the host:

```powershell
.\scripts\start.ps1
```

## Submit an order

In another PowerShell terminal:

```powershell
$body = Get-Content .\sample_data\order.json -Raw
Invoke-RestMethod -Method Post `
  -Uri http://localhost:7071/api/orders `
  -ContentType application/json `
  -Body $body
```

Expected initial response:

```json
{"status":"accepted","order_id":"A1001"}
```

HTTP `202` means accepted for asynchronous processing. It does not mean the downstream function completed.

## Inspect the result

```powershell
.\.venv\Scripts\python.exe -m tools.storage list
```

You should see a JSON file in the `processed-orders` container.

## Understand the boundaries

`SubmitOrder` validates the request and places a small message on `raw-orders`.

`ProcessOrder` reads one message and writes a processed JSON blob. The queue isolates the HTTP response time from downstream processing time.

## Failure experiment

Stop the Functions host but leave Azurite running. Submit a queue message through the HTTP endpoint before stopping, or pause immediately after the response. Restart the host and observe that pending work is processed.

Queue triggers use at-least-once processing. A handler can receive the same logical work more than once. A real sink needs a stable idempotency key such as `order_id` plus a source version or event ID.

The project uses `maxDequeueCount: 3`. After repeated failures, Queue Storage moves a message to `raw-orders-poison`.

## Exercise

Temporarily raise an exception for order ID `FAIL-001`. Submit that order and inspect the retry logs. Remove the exception after the experiment.

## Checkpoint

Explain why an empty source queue does not prove that every order was processed successfully.

# 9. Testing and debugging

## Objective

Test business logic quickly and debug Functions adapters separately.

## Run the tests

```powershell
.\scripts\test.ps1
```

The tests do not require Azurite or a Functions host. They test pure Python code in `src/`.

## Why not test everything through HTTP

Host-based tests are slower and make failures harder to isolate. Use three test boundaries:

| Boundary | Purpose |
|---|---|
| Pure unit test | Validation and calculation behavior |
| Local integration test | Azurite bindings and event delivery |
| Cloud integration test | Identity, networking, scale and real services |

This repository covers the first two locally. It does not claim to validate cloud behavior.

## Debug in VS Code

The simplest workflow is:

1. Select `.venv\Scripts\python.exe`.
2. Open `function_app.py`.
3. Add a breakpoint inside `validate_order()`.
4. Open the **Run and Debug** view.
5. Use the Azure Functions extension to start debugging.
6. Send the sample HTTP request.

If VS Code does not create the correct configuration automatically, continue using `func start` and log structured values while learning. Avoid adding a complex custom debugger setup until the functions run normally.

## Logging guidance

Use Python's `logging` module. Include stable identifiers such as `order_id`, but do not log credentials or sensitive payloads.

A production pipeline should measure:

- Invocation success and failure
- Processing duration
- Queue age and depth
- Retry count
- Poison-message count
- Accepted and rejected row counts
- Last successful watermark

## Exercise

Add tests for:

- An empty `order_id`
- A negative price
- A price with three decimal places
- A CSV missing `unit_price`

## Checkpoint

Explain why passing unit tests does not prove that a Blob trigger is configured correctly.

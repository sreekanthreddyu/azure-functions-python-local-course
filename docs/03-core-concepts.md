# 3. Core concepts

## Function app

`app = func.FunctionApp()` is the application object. Decorators register individual functions with the host.

## Trigger

A trigger starts a function. One function has one trigger.

Examples:

- HTTP request
- Timer schedule
- Queue message
- Blob creation

## Binding

A binding connects a function to another service without requiring all connection code in the handler.

Examples in this repository:

- Queue output binding
- Blob output binding

Use an SDK when you need capabilities that the binding does not provide, such as listing blobs or controlling conditional writes.

## Local configuration

`local.settings.json` contains local settings. It is ignored by Git. The starter configuration points `AzureWebJobsStorage` and `DataStorage` to Azurite with `UseDevelopmentStorage=true`.

The decorator value:

```python
connection="DataStorage"
```

means “read the setting named `DataStorage`.” It is not a connection string itself.

## `host.json`

`host.json` configures the Functions host. This repository uses it for extension bundles, logging, and queue retry behavior.

Its value `"version": "2.0"` is the `host.json` schema version. It does not mean Functions runtime version 2. The project runs on Functions runtime 4.

## Progressive registration

The starter settings contain:

```json
"ENABLE_STORAGE_FUNCTIONS": "false"
```

When this is `false`, `function_app.py` does not register the storage blueprint. Azurite still supplies the Functions host's local storage state, but the first host output contains only the beginner functions.

Change it to `true` and restart the host when the storage lessons begin. The host then registers `SubmitOrder`, `ProcessOrder`, and `ProcessCsv` from `storage_functions.py`.

## Delivery semantics

Queue and blob triggers can run more than once for the same logical event. Production handlers must be idempotent.

Idempotent means that processing the same event again does not create an incorrect additional effect.

## Checkpoint

Identify the trigger and output binding on `SubmitOrder` in `storage_functions.py`. Then explain what `connection="DataStorage"` means.

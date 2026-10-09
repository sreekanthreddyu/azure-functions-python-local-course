# 8. CSV blob processing

## Objective

React to a CSV upload and create curated JSON Lines data.

## Enable the function

Start Azurite. In `local.settings.json`, set:

```json
"AzureWebJobsStorage": "UseDevelopmentStorage=true",
"ENABLE_STORAGE_FUNCTIONS": "true"
```

Restart the host:

```powershell
.\scripts\start.ps1
```

## Upload the sample file

In another PowerShell terminal:

```powershell
.\.venv\Scripts\python.exe -m tools.storage upload .\sample_data\orders.csv
```

The helper uploads the file through the Blob Storage API. Copying a file into Azurite's persistence directory does not create a blob event.

## Inspect the output

Wait for the polling-based Blob trigger. Then run:

```powershell
.\.venv\Scripts\python.exe -m tools.storage list
```

Expected containers include:

```text
[landing]
  orders.csv
[curated]
  orders.jsonl
```

The sample has two valid rows and one invalid row. Valid rows appear in the JSONL output. The rejected row appears in the Functions host log.

## Engineering tradeoffs

This exercise reads the entire blob into memory. Use it only for small learning files.

For large production files, consider:

- Streaming or batching
- File-size limits
- Schema versioning
- Quarantine storage
- Deterministic output names
- Duplicate delivery
- A compute service designed for large transformations

Azure Functions is not a replacement for Spark or a warehouse bulk-load engine.

## Exercise

Add a quarantine Blob output binding. Write rejected rows to `quarantine/{name}.json` instead of logging them only.

## Checkpoint

Explain the difference between invalid business data and a retryable storage connection failure.

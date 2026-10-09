# 4. Timer trigger

## Objective

Run Python code on a local schedule.

Open `local.settings.json` and change:

```json
"AzureWebJobs.TimerHeartbeat.Disabled": "false"
```

Restart the host:

```powershell
.\scripts\start.ps1
```

Watch the terminal for one minute. The function logs a UTC timestamp.

## Understand the schedule

The expression is:

```text
0 */1 * * * *
```

Azure Functions NCRONTAB uses six fields:

```text
second minute hour day month day-of-week
```

This schedule runs at second zero of every minute.

## Why `use_monitor=False` is used here

This beginner timer does not persist schedule occurrences. The Functions host still uses the Azurite instance configured during setup.

For production scheduling, use persistent schedule monitoring and configure real Azure Storage. A stopped local host does not run missed work reliably. Use a source watermark or another durable checkpoint for ingestion recovery.

## Exercise

Change the schedule to every five minutes:

```text
0 */5 * * * *
```

Then restore the one-minute setting.

## Checkpoint

Explain why a timer invocation count is not a safe incremental-ingestion checkpoint.

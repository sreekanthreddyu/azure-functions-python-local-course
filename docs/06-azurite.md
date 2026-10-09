# 6. Local storage with Azurite

## Objective

Understand the local Blob, Queue, and Table Storage emulator used throughout the course.

## Install the extension

The Windows setup lesson installed the Microsoft **Azurite** extension. Start it before every course session.

Press `Ctrl+Shift+P` and run:

```text
Azurite: Start
```

The default local endpoints are:

| Service | Endpoint |
|---|---|
| Blob | `http://127.0.0.1:10000` |
| Queue | `http://127.0.0.1:10001` |
| Table | `http://127.0.0.1:10002` |

Verify them:

```powershell
Test-NetConnection 127.0.0.1 -Port 10000
Test-NetConnection 127.0.0.1 -Port 10001
Test-NetConnection 127.0.0.1 -Port 10002
```

## Local settings

Your generated `local.settings.json` already contains:

```json
"AzureWebJobsStorage": "UseDevelopmentStorage=true"
```

Leave this value unchanged:

```json
"DataStorage": "UseDevelopmentStorage=true"
```

`AzureWebJobsStorage` is used by the Functions host. `DataStorage` is used by the tutorial's business-data triggers and bindings. Both point to the same local emulator account.

## What Azurite does not reproduce

Azurite supports Blob, Queue, and Table Storage for development. It does not reproduce:

- Managed identity and Azure RBAC
- Private endpoints
- Azure Files
- ADLS Gen2 hierarchical namespaces and ACLs
- Service Bus
- Event Hubs
- Event Grid
- Cloud scaling or performance

Keep Azurite bound to your local machine. Its development credentials are public and are not a security boundary.

## Checkpoint

Explain why `UseDevelopmentStorage=true` works locally but must not be used as production configuration.

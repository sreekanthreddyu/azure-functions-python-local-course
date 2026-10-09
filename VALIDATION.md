# Validation record

Validation date: October 9, 2026

## Completed checks

- Python 3.12 byte-code compilation succeeded for the main app, storage blueprint, pure logic, helpers, cloud-trigger examples, and Durable app.
- Nine pytest tests passed.
- The standard application imported successfully with the Azure Functions Python SDK.
- The standard application registered three beginner functions when `ENABLE_STORAGE_FUNCTIONS=false`.
- The standard application registered six functions when `ENABLE_STORAGE_FUNCTIONS=true`.
- The cloud-only trigger-pattern module imported successfully without registration.
- The Durable application imported successfully and registered four Durable functions.
- Azure Functions Core Tools 4 started the beginner application with Azurite and indexed `Health`, `ValidateOrder`, and `TimerHeartbeat`.
- Azurite 3.37 started Blob, Queue, and Table endpoints successfully.

## Environment limitation

The preparation environment did not provide Windows PowerShell, so the `.ps1` scripts were reviewed but not executed on Windows.

The complete Queue-to-Blob, Blob-to-JSONL, and Durable event-delivery scenarios must be run on the learner's Windows machine. The repository provides explicit manual checks for those scenarios. Local emulator success does not establish Azure cloud identity, networking, scale, or hosting-plan behavior.

## Learner verification

Run:

```powershell
.\scripts\setup.ps1
# Start Azurite from the VS Code Command Palette
.\scripts\start.ps1
.\scripts\test.ps1
```

Then complete lessons 7, 8, and 10 to verify the event-driven scenarios.

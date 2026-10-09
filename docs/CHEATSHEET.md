# Command cheat sheet

Run commands from the repository root unless a lesson says otherwise.

## Prepare

```powershell
.\scripts\setup.ps1
```

## Start Functions

```powershell
.\scripts\start.ps1
```

## Run tests

```powershell
.\scripts\test.ps1
```

## Health request

```powershell
Invoke-RestMethod http://localhost:7071/api/health
```

## Validate an order

```powershell
$body = Get-Content .\sample_data\order.json -Raw
Invoke-RestMethod -Method Post `
  -Uri http://localhost:7071/api/orders/validate `
  -ContentType application/json -Body $body
```

## Submit an asynchronous order

```powershell
$body = Get-Content .\sample_data\order.json -Raw
Invoke-RestMethod -Method Post `
  -Uri http://localhost:7071/api/orders `
  -ContentType application/json -Body $body
```

## Upload a CSV to Azurite

```powershell
.\.venv\Scripts\python.exe -m tools.storage upload .\sample_data\orders.csv
```

## List Azurite blobs

```powershell
.\.venv\Scripts\python.exe -m tools.storage list
```

## Check versions

```powershell
py -3.13 --version
func --version
.\.venv\Scripts\python.exe -m pip --version
```

## Stop

Press `Ctrl+C` in the Functions terminal. Run **Azurite: Close** from the VS Code Command Palette when storage is no longer needed.

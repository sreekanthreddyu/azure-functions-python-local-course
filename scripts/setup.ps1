$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw "Python Launcher (py.exe) was not found. Install Python 3.12 x64 first."
}

if (-not (Test-Path ".venv")) {
    py -3.12 -m venv .venv
}

& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r requirements-dev.txt

if (-not (Test-Path "local.settings.json")) {
    Copy-Item "local.settings.json.example" "local.settings.json"
}

Write-Host ""
Write-Host "Local Python setup is ready." -ForegroundColor Green
Write-Host "Run: .\scripts\start.ps1"

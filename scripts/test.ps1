$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    throw "The virtual environment is missing. Run .\scripts\setup.ps1 first."
}

& ".\.venv\Scripts\python.exe" -m pytest -q

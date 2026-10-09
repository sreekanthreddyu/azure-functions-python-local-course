$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw "Python Launcher (py.exe) was not found. Install Python 3.13 x64 first."
}

if (-not (Test-Path ".venv")) {
    py -3.13 -m venv .venv
} else {
    $venvPython = ".\.venv\Scripts\python.exe"
    if (-not (Test-Path $venvPython)) {
        throw "The existing .venv has no Python executable. Rename it and rerun setup."
    }

    $venvVersion = & $venvPython -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
    if ($venvVersion -ne "3.13") {
        throw "The existing .venv uses Python $venvVersion. Rename it (for example, .venv-py312) and rerun setup."
    }
}

& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r requirements-dev.txt

if (-not (Test-Path "local.settings.json")) {
    Copy-Item "local.settings.json.example" "local.settings.json"
}

Write-Host ""
Write-Host "Local Python setup is ready." -ForegroundColor Green
Write-Host "Run: .\scripts\start.ps1"

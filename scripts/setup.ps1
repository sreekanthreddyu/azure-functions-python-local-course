$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot
$requiredVersion = "3.13.15"

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw "Python Launcher (py.exe) was not found. Install Python $requiredVersion x64 first."
}

$detectedVersion = (& py -3.13 -c "import platform; print(platform.python_version())" 2>$null)
if ($LASTEXITCODE -ne 0 -or $detectedVersion -ne $requiredVersion) {
    throw "Python $requiredVersion is required. Found: $detectedVersion. Install the exact version and rerun setup."
}

if (Test-Path ".venv\Scripts\python.exe") {
    $venvVersion = & ".\.venv\Scripts\python.exe" -c "import platform; print(platform.python_version())"
    if ($LASTEXITCODE -ne 0 -or $venvVersion -ne $requiredVersion) {
        throw "Existing .venv uses Python $venvVersion; Python $requiredVersion is required. Rename your old .venv and rerun setup."
    }
} elseif (Test-Path ".venv") {
    throw "Existing .venv is incomplete. Rename it and rerun setup."
} else {
    py -3.13 -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw "Failed to create .venv." }
}

& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "pip upgrade failed." }
& ".\.venv\Scripts\python.exe" -m pip install -r requirements-dev.txt
if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed." }

if (-not (Test-Path "local.settings.json")) {
    Copy-Item "local.settings.json.example" "local.settings.json"
}

Write-Host ""
Write-Host "Local Python $requiredVersion setup is ready." -ForegroundColor Green
Write-Host "Run: .\scripts\start.ps1"

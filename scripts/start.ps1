$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$venvRoot = Join-Path $projectRoot ".venv"
$venvScripts = Join-Path $venvRoot "Scripts"

if (-not (Test-Path (Join-Path $venvScripts "python.exe"))) {
    throw "The virtual environment is missing. Run .\scripts\setup.ps1 first."
}

if (-not (Get-Command func -ErrorAction SilentlyContinue)) {
    throw "Azure Functions Core Tools 4 is missing. Follow docs/01-windows-setup.md."
}

$env:VIRTUAL_ENV = $venvRoot
$env:PATH = "$venvScripts;$env:PATH"
Set-Location $projectRoot

func start

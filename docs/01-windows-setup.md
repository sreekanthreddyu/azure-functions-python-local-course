# 1. Windows setup

## Objective

Prepare one local Python environment that can run and test Azure Functions.

## Install the software

Install:

1. [Python 3.13 x64](https://www.python.org/downloads/)
2. [Visual Studio Code](https://code.visualstudio.com/)
3. VS Code **Python** extension
4. VS Code **Azure Functions** extension
5. VS Code **Azurite** extension from Microsoft
6. [Azure Functions Core Tools 4 x64 MSI](https://learn.microsoft.com/azure/azure-functions/functions-run-local)

The MSI avoids installing Node.js only for Core Tools. If you already use Node.js, the supported alternative is:

```powershell
npm.cmd install -g azure-functions-core-tools@4 --unsafe-perm true
```

Use either MSI or npm. Do not install both.

## Verify the tools

Open a new PowerShell terminal:

```powershell
py -3.13 --version
func --version
where.exe func
```

Expected:

```text
Python 3.13.x
4.x.x
```

## Prepare this repository

From the repository root:

```powershell
.\scripts\setup.ps1
```

The script:

1. Creates `.venv` with Python 3.13.
2. Installs the runtime and test dependencies.
3. Copies `local.settings.json.example` to `local.settings.json` if needed.

It does not change your PowerShell execution policy. It calls the venv Python executable directly.

If you already have a `.venv` created with another Python version, rename it first to keep it as a backup, for example:

```powershell
Rename-Item .venv .venv-py312
```

Then rerun `setup.ps1` to create a Python 3.13 environment.

If your organization blocks `.ps1` scripts, use these commands instead:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
Copy-Item local.settings.json.example local.settings.json
```

## Select the interpreter

In VS Code:

1. Press `Ctrl+Shift+P`.
2. Run **Python: Select Interpreter**.
3. Select `.venv\Scripts\python.exe`.

## Start the host

First, press `Ctrl+Shift+P` in VS Code and run **Azurite: Start**. Keep its Blob, Queue, and Table services running.

Then start Functions:

```powershell
.\scripts\start.ps1
```

The host should list `Health` and `ValidateOrder`. Storage pipeline functions are not registered until a later lesson, but the host already uses Azurite for local storage state.

## Checkpoint

Explain the difference between:

- Python itself
- The project venv
- Azure Functions Core Tools
- The Azure Functions Python package
- Azurite

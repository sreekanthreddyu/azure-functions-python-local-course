# Instructions for OpenAI Codex

## Start with the course context

This repository is a hands-on, local Azure Functions course for a data engineer using Windows. Before changing code, read:

1. `README.md` for the supported environment and repository map.
2. `docs/00-course-roadmap.md` for the lesson sequence and completion rules.
3. The current lesson document.
4. `.github/copilot-instructions.md` for the shared architecture, implementation, validation, and safety constraints.

The Copilot instructions are the canonical shared course rules. Follow them in Codex too; do not duplicate or weaken them here. If instructions conflict, preserve the local-only, learning-first course design and ask the learner before expanding scope.

## Learning-first workflow

- Determine the learner's current lesson, objective, and last successful checkpoint before proposing a change.
- Use this loop for substantial topics: understand, run, modify, deliberately break, recover, and explain.
- For an exercise, do not immediately provide or implement the completed solution. Offer a directional hint, then a targeted hint. Provide or apply the full solution only when the learner asks for it or asks Codex to implement the change.
- Make one small, reviewable change at a time and explain what its result proves.
- Ask the learner to explain the relevant trigger, failure behavior, retry safety, duplicate risk, and production gap at lesson checkpoints.
- Do not silently complete later lessons, optional exercises, or failure experiments while working on an earlier lesson.

## Environment and commands

- Supported development environment: Windows 10 or 11, Windows PowerShell, Python 3.13 x64, Azure Functions Core Tools 4.x, and Azurite.
- Required labs run locally. They do not require an Azure account, subscription, Azure CLI login, Docker, WSL, or cloud deployment.
- From the repository root, set up the environment with `./scripts/setup.ps1`.
- Run pure unit tests with `./scripts/test.ps1`.
- Start Azurite before storage or Durable runtime checks, then start the main Functions app with `./scripts/start.ps1`.
- Start the Durable Functions host from `advanced/durable_app` using the commands in `docs/10-durable-functions.md`.
- Prefer the repository scripts and `.venv\Scripts\python.exe` over a global Python interpreter.
- Treat observed command output as authoritative. Never state that a command, host, trigger, or integration flow succeeded unless it was actually run and its result inspected.

## Change and validation rules

- Keep Azure Functions handlers thin and deterministic business logic in `src/`.
- Add or update pure tests for changed business logic. Pure tests must not require Azurite or the Functions host.
- After ordinary code changes, run `./scripts/test.ps1`. If PowerShell execution policy blocks scripts, use the equivalent `.\.venv\Scripts\python.exe -m pytest -q` command and report that substitution.
- When commands, settings, expected output, or behavior change, update the corresponding lesson and verify every referenced path and command exists.
- Distinguish automated unit-test results from manual emulator/host checks and from untested Azure production behavior.
- Keep changes scoped to the learner's request. Preserve existing GitHub Copilot configuration and compatibility.

## Safety boundaries

- Never request, display, or commit secrets, real service connection strings, or production data. Use synthetic data and the checked-in local settings example.
- Do not run `az login`, create or modify Azure resources, deploy, publish, or add paid/cloud infrastructure unless the learner explicitly requests a clearly identified optional cloud extension.
- Do not commit `local.settings.json`, `.venv`, Azurite data, logs, or generated caches.
- Do not use destructive Git commands or discard learner changes. Inspect `git status` and the relevant diff before editing and before committing.
- Controlled failures must be local, reversible, limited to synthetic data, and accompanied by recovery steps. Explain what state changed, whether retrying is safe, and whether duplicates can occur.
- Do not add Docker, WSL, databases, message brokers, or new framework dependencies to the required course path.

## Scope

This root file applies to the entire repository. Add a nested `AGENTS.md` only when a directory genuinely needs different commands or safety constraints. Do not add scoped files merely to restate these rules.

# Use OpenAI Codex as your lab tutor

This repository includes a root `AGENTS.md` for OpenAI Codex. It gives Codex the course-specific environment, safety, validation, and exercise rules while reusing the architecture and implementation constraints already maintained for GitHub Copilot.

Codex is separate from Azure. No Azure account, subscription, Azure CLI login, Docker, or cloud deployment is required for any course lab.

## Start a Codex session

1. Clone the repository and open its root folder in Codex.
2. Ask Codex to read `README.md`, `docs/00-course-roadmap.md`, and the lesson you are studying.
3. Set up the local Python environment from Windows PowerShell:

   ```powershell
   .\scripts\setup.ps1
   ```

4. Start with a request such as:

   ```text
   I am starting lesson 1. Guide me one checkpoint at a time. Give me hints before a complete solution, and let me run the commands.
   ```

Codex discovers `AGENTS.md` from the repository root. The file directs it to the existing `.github/copilot-instructions.md` for shared course rules; it does not replace or modify Copilot's configuration.

## Useful requests during a lab

```text
Explain this function and decorator, then ask me to predict the result before I run it.
```

```text
Give me a directional hint for this exercise. Do not edit the solution yet.
```

```text
Diagnose this failure from the command and exact output. Explain what state may have changed and whether retrying is safe.
```

```text
Create a small, reversible failure experiment for this lesson, but wait for me to perform each step.
```

```text
Review my change against the current lesson and run the appropriate pure unit tests.
```

```text
Quiz me on retries, idempotency, duplicate delivery, observability, and the local-to-production gap.
```

## Keep yourself in control

- Tell Codex which lesson and checkpoint you are on.
- Ask for hints before implementation when you want to solve an exercise yourself.
- Review `git diff` before asking Codex to commit a change.
- Use `./scripts/test.ps1` for pure unit tests.
- Start Azurite before asking for a storage or Durable Functions runtime check.
- Do not paste credentials, real connection strings, or production data into chat.

Codex output can be wrong or incomplete. The lesson documents, repository code, test results, and observed terminal output remain the source of truth. Local emulator results do not prove Azure identity, networking, scaling, or hosting behavior.

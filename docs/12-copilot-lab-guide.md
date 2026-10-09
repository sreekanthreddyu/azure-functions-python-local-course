# Use GitHub Copilot as your lab tutor

This repository includes a purpose-built **Azure Functions Lab Tutor** for GitHub Copilot Chat in VS Code. It knows the lesson order, local-only constraints, repository structure, Windows commands, and the difference between a hint and a complete solution.

GitHub Copilot is separate from Azure. You still do not need an Azure account or subscription for any course lab. Copilot itself must be available and signed in through your GitHub account in VS Code.

## One-time VS Code setup

1. Clone the repository and open its root folder in VS Code.
2. Trust the workspace when VS Code asks.
3. Open **Extensions** with `Ctrl+Shift+X`.
4. Install the workspace recommendations: GitHub Copilot Chat, Python, Azure Functions, and Azurite.
5. Sign in to GitHub when the Copilot extension asks. Do not run `az login`.
6. Open Copilot Chat with `Ctrl+Alt+I`.

The repository-wide instructions in `.github/copilot-instructions.md` load automatically for Copilot sessions in this workspace.

## Select the tutor

1. In Copilot Chat, open the agent picker.
2. Select **Azure Functions Lab Tutor**.
3. Start with:

   ```text
   I am starting lesson 1. Guide me one checkpoint at a time and give hints before solutions.
   ```

If the tutor is not listed, open the Command Palette with `Ctrl+Shift+P`, run **Chat: Open Customizations**, and confirm that `azure-functions-lab-tutor.agent.md` appears under workspace agents. You can also right-click the Chat view and select **Diagnostics** to inspect which customizations loaded.

## Useful requests during a lab

```text
Explain what this decorator does in the current function.
```

```text
Give me a level-1 hint for the current exercise. Do not write the solution yet.
```

```text
This command failed. Diagnose only from this command and error output: <paste both>
```

```text
Quiz me on the checkpoint before I continue.
```

```text
Relate this trigger to retries, duplicate delivery, and idempotency in a production data pipeline.
```

```text
Review my change against the current lesson, then tell me which test to run.
```

## Keep yourself in control

- Run and read each command rather than accepting a large batch of changes.
- Ask for a hint first when completing an exercise.
- Paste the exact error instead of paraphrasing it.
- Review proposed edits before accepting them.
- Use `git diff` to inspect changes and `./scripts/test.ps1` to verify application logic.
- Do not paste credentials or production data into chat.

Copilot responses are nondeterministic. The lesson documents and observed terminal output remain the source of truth.

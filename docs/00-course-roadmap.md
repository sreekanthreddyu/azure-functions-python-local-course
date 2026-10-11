# Course roadmap

## Goal

Learn how Azure Functions receives events, runs Python code, moves data between services, handles failures, and coordinates longer workflows.

No lesson requires an Azure account.

## Learning levels

| Level | Lessons | Result |
|---|---|---|
| Beginner | 1–5 | Run HTTP and timer functions and understand trigger selection |
| Intermediate | 6–9 | Build and test queue and blob pipelines with Azurite |
| Upper intermediate | 10–11 | Build Durable workflows and reason about production behavior |

## Recommended pace

| Session | Work | Approximate time |
|---|---|---:|
| 1 | Windows setup and HTTP functions | 75 minutes |
| 2 | Core concepts, timer trigger, and trigger catalog | 60 minutes |
| 3 | Azurite and queue pipeline | 90 minutes |
| 4 | Blob processing | 60 minutes |
| 5 | Testing and debugging | 60 minutes |
| 6 | Durable Functions | 90 minutes |
| 7 | Production-readiness review | 45 minutes |

Required lesson time: approximately **8 hours**.

Reserve up to **1 hour** for installation differences, package downloads, or troubleshooting. The complete course should remain below 10 hours.

Exercises labeled **Exercise** are optional. Skip them during the first pass if a session reaches its time limit.

## What runs locally

| Component | Local implementation |
|---|---|
| Functions runtime | Azure Functions Core Tools |
| Python worker | Your `.venv` interpreter |
| Blob Storage | Azurite |
| Queue Storage | Azurite |
| Durable state | Azurite Blob, Queue, and Table services |
| Tests | pytest |

Azurite is a development emulator. It does not reproduce managed identity, private networking, autoscaling, hosting-plan limits, Application Insights, ADLS Gen2, Service Bus, or Event Hubs.

## How to study each lesson

1. Read the objective.
2. Run the commands yourself.
3. Inspect the named Python function and decorator.
4. Complete the failure experiment.
5. Answer the checkpoint before continuing.

For first-pass completion, run the provided code and answer each checkpoint. You do not need to implement the optional exercises.

Azurite is part of the initial setup. Storage-backed Queue and Blob functions remain unregistered until their lessons, which keeps the first host output simple.

Do not start with Durable Functions. First understand ordinary HTTP, timer, queue, and blob triggers.

## Optional AI tutors

If GitHub Copilot Chat is available to you, select the repository's **Azure Functions Lab Tutor** to work through a lesson one checkpoint at a time. See [Use GitHub Copilot as your lab tutor](12-copilot-lab-guide.md). Copilot is optional and does not change the course time budget or require an Azure account.

If OpenAI Codex is available to you, open the repository root in Codex and ask it to guide the same checkpoint-based workflow. See [Use OpenAI Codex as your lab tutor](13-codex-lab-guide.md). Codex is also optional and does not replace the lesson documents or observed terminal output.

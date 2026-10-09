# 5. Azure Functions trigger types

## Objective

Understand the main trigger families and choose the correct trigger for a workload.

One function has one trigger. It can also have several input and output bindings.

## Trigger catalog

| Trigger | Starts when | Typical data-engineering use | Local course support |
|---|---|---|---|
| HTTP | A client sends a request | Webhook, ingestion API, control endpoint | Fully runnable |
| Timer | A schedule becomes due | Polling, cleanup, small scheduled ingestion | Fully runnable |
| Queue Storage | A queue message arrives | Decoupled background processing | Fully runnable with Azurite |
| Blob Storage | A blob is created or changed | File ingestion and validation | Fully runnable with Azurite |
| Durable orchestration | Durable runtime schedules workflow work | Fan-out/fan-in and stateful workflows | Fully runnable with Azurite |
| Event Grid | An event is delivered | Resource and business-event routing | Code pattern only |
| Event Hubs | Stream events arrive | Telemetry and high-volume event ingestion | Code pattern only |
| Service Bus | A queue or topic message arrives | Enterprise messaging and ordered workflows | Code pattern only |
| Cosmos DB | Change feed contains changes | Reactive document processing | Code pattern only |

The final four require services that Azurite does not emulate. The course includes their programming patterns without requiring accounts, credentials, Docker, or extra brokers.

## Selection guide

Choose HTTP when the caller needs an immediate response.

Choose Queue Storage for simple asynchronous work where Azure Storage messaging is sufficient.

Choose Service Bus when you need richer messaging features such as topics, sessions, dead-lettering, or advanced delivery controls.

Choose Event Hubs for high-throughput event streams and partitioned consumption.

Choose Event Grid for event routing and notifications. Event Grid is not a work queue.

Choose Blob triggers for file arrival. For high-scale or low-latency blob events in Azure, also evaluate Event Grid-based blob triggering.

Choose Cosmos DB triggers for processing the change feed, not for arbitrary Cosmos DB queries.

Choose Durable Functions when a workflow must retain state, wait, retry activities, or coordinate parallel work.

## Cloud-only code patterns

Review `examples/cloud_trigger_patterns.py`. These functions are intentionally not registered by the local app.

Each `connection` value names an application setting. It does not contain a secret directly.

Do not invent connection strings or create fake cloud accounts for this course. When you later receive an Azure subscription, you can connect these patterns to real development resources and learn identity, networking, checkpoints, partitions, sessions, and scaling separately.

## Trigger versus binding examples

In `SubmitOrder`:

- HTTP is the trigger.
- Queue Storage is the output binding.

In `ProcessOrder`:

- Queue Storage is the trigger.
- Blob Storage is the output binding.

This two-function design accepts a request quickly and performs background work separately.

## Checkpoint

Select a trigger for each case:

1. Receive a GitHub webhook.
2. Process CSV files placed in a container.
3. Consume millions of telemetry events.
4. Run a cleanup every night.
5. Coordinate five parallel validation activities and combine their results.

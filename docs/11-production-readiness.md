# 11. Production readiness

Local success proves that your code and basic bindings can work. It does not prove that the design is ready for Azure.

## Local-to-cloud differences

| Concern | Local course | Production decision |
|---|---|---|
| Identity | Development connection string | Managed identity and least privilege |
| Secrets | Local settings | Key Vault or managed application settings |
| Networking | Loopback | Public access, VNet integration or private endpoints |
| Scaling | One computer | Hosting plan and concurrency limits |
| Monitoring | Console logs | Application Insights and operational alerts |
| Storage | Azurite | Real durability, redundancy and lifecycle rules |
| Deployment | Local source | CI/CD, packages, rollback and environment promotion |

## Idempotency

Azure Storage triggers use at-least-once delivery. Design the sink so a repeated event does not create an incorrect duplicate effect.

Common patterns:

- Stable event or job ID
- Unique constraint in the destination
- Processed-event ledger
- Conditional blob creation
- Source version or CDC position
- Atomic target write and checkpoint where supported

Do not assume a database constraint exists merely because a model declares a primary key. Confirm what the destination enforces.

## Retry versus quarantine

Retry transient operational failures:

- Temporary connection failure
- Throttling
- Short service outage

Quarantine permanent business-data failures:

- Missing required column
- Invalid number
- Unsupported schema version

Repeatedly retrying invalid data wastes resources and hides the real problem.

## Incremental ingestion

A safe incremental pipeline needs:

1. A stable source ordering mechanism.
2. Fixed low and high bounds for a run.
3. An idempotent target write.
4. A checkpoint that advances only after successful processing.
5. A reconciliation process for missing handoffs.

A wall-clock timestamp is not always a safe cursor. Prefer supported CDC positions or monotonic source versions when available.

## Function suitability

Functions are well suited to event-driven, bounded work. Reconsider the design when a task needs:

- Multi-gigabyte in-memory transformation
- Long CPU-heavy computation
- Large distributed joins
- Unbounded execution time
- Strong transactions across several independent services

Use a queue to submit long work and return a status resource rather than holding an HTTP connection open.

## Before eventual deployment

When you obtain an Azure subscription, separately learn:

- Flex Consumption or another hosting plan
- Managed identity
- Azure Storage RBAC
- Key Vault references
- Application Insights
- Deployment slots or environment promotion
- Private networking
- Cost controls

Those topics intentionally remain outside this no-account course.

I’ll read the README in the poc folder and extract the current LangGraph task flow so I can produce a concrete container-apps migration plan focused only on components inside Container Apps and MCP connectivity.

Read README.md, lines 1 to 320

Solution: keep LangGraph as the orchestration core, package it as one long-running NORA Agent service plus two Container Jobs for asynchronous work, and route all external integrations through MCP adapters inside the Container Apps environment.

Plan focused only on what runs inside Container Apps:

1. Define target runtime split

NORA Agent Container App (always-on service):
Receives workflow requests
Runs LangGraph state machine
Executes NORA API fetch, RCA decomposition, decisioning
Calls MCP endpoints for Azure OpenAI, ServiceNow, Snowflake
Ticket Ingestion Container Job (scheduled or event-triggered):
Replays pending/failed ticket create flows
Retries idempotently with backoff
Ticket Update Container Job (scheduled or queue-triggered):
Applies follow-up updates to existing incidents
Synchronizes status transitions and notes

2. Refactor Python app into deployable bounded modules

Workflow core module:
Pure LangGraph orchestration and state transitions
No direct SDK calls to external systems
MCP adapter module:
One adapter per external system: Azure OpenAI, ServiceNow, Snowflake
Unified request/response envelope and error schema
Runtime shell module:
HTTP entrypoints for service mode
Job entrypoints for ingestion/update mode
Shared contracts:
Typed input/output models for NORA API, RCA result, ticket payloads, MCP tool calls

3. Map current task flow to graph nodes

Node A: NORA API fetch
Node B: RCA decomposition
Node C: OpenAI MCP call for RCA augmentation
Node D: policy decision node for ticket creation
Node E: ServiceNow MCP create issue
Node F: response composer and state persistence
Node G: compensation/retry node for recoverable errors

4. Containerization and runtime packaging

Build one image with multiple entrypoints:
Service entrypoint for NORA Agent
Job entrypoint for ingestion
Job entrypoint for update
Health and readiness:
Service health endpoint for live/readiness
Startup check validates required env vars and MCP reachability
Resource profiles:
Service: low-latency CPU baseline
Jobs: burst CPU profile for batch windows

5. Configuration and secrets model

Environment configuration by deployment profile:
Local, test, prod
Secrets injection:
ServiceNow creds, OpenAI keys, Snowflake creds via secret refs
Feature flags:
enable_live_openai
enable_live_servicenow
enable_live_snowflake
enable_stub_fallback
Timeouts/retries:
Per-MCP adapter timeout, max attempts, jitter strategy

6. Reliability and state strategy

Idempotency keys:
One workflow_run_id across all MCP calls
Retry policy:
transient error retry at node level
dead-letter path for hard failures
State store:
Short term: local or managed lightweight store for workflow status
Later: switch to durable cloud store without changing graph contracts
Observability:
Structured logs with correlation_id
Per-node latency and failure counters
Job execution summaries
7. Security boundary inside Container Apps

Network:
Private egress where possible for MCP targets
Identity:
Managed identity for Azure-native dependencies
Secret hygiene:
No secrets in logs
Rotate credentials on schedule
Input safeguards:
Validate incoming payloads before graph execution

8. Test and validation plan

Unit tests:
Graph node behavior
Policy decision matrix
Adapter request/response mapping
Contract tests:
MCP schema compatibility for OpenAI, ServiceNow, Snowflake
Integration tests:
End-to-end in stub mode
Selective live tests with gated credentials
Load test:
concurrency and queue backlog for jobs
Failure drills:
simulate MCP timeout, TLS failure, 429/5xx, malformed response

9. Delivery phases

Phase 1: Containerize current POC unchanged behavior
Phase 2: Split into service plus 2 jobs and add retries/idempotency
Phase 3: Harden observability/security and run load/failure validation
Phase 4: Cutover with canary traffic and rollback hooks

10. Acceptance criteria

NORA request completes through LangGraph in Container App with same functional output as current POC
RCA decomposition and OpenAI MCP call are traceable by correlation_id
ServiceNow issue creation works through MCP with retry and idempotency
Failed ticket operations are reprocessed by jobs without duplication
Stub/live mode toggles work by config only, no code changes
End-to-end tests pass in both stub and live-gated modes
If you want, I can convert this into an execution checklist aligned to your existing tasks, with concrete task IDs and day-by-day sequencing for implementation.


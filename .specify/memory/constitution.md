<!--
Sync Impact Report
- Version change: 1.1.0 -> 1.1.1
- Modified principles:
    - I. Spec-First and Traceability -> no title change
    - II. Test-First Engineering -> no title change
    - III. API Contract Integrity -> no title change
    - IV. Simplicity and Bounded Phase-1 Scope -> no title change
    - V. Cloud Readiness and Operational Quality -> no title change
- Added sections:
    - Phase-1 Scope and Delivery Model (boundary refinement)
- Removed sections: none
- Follow-up TODOs: none
-->

# NORA Wholesale Care Constitution

## Core Principles

### I. Spec-First and Traceability
Every Phase-1 implementation task MUST map to approved requirements and acceptance criteria
before work begins. Requirements, plans, tasks, code, tests, and validation evidence MUST
remain linked and auditable across the delivery lifecycle. Any work that cannot be traced to
an approved requirement MUST be treated as out of scope until it is formally approved.
Rationale: traceability keeps scope bounded, enables review, and preserves accountability for
Phase-1 delivery decisions.

### II. Test-First Engineering
Teams MUST write failing tests or executable validations before implementation for each
requirement slice. Unit, integration, and contract tests MUST cover changed behavior,
dependency failure conditions, and error handling for coverage diagnostics. No feature slice is
complete until the relevant tests pass locally and the evidence is recorded in the task or PR.
Rationale: test-first engineering prevents speculative code and proves the behavior required
for the approved flow.

### III. API Contract Integrity
All request and response contracts, validation rules, error models, status codes, and versioning
rules MUST be explicit and testable before release. Backward-incompatible contract changes
require explicit approval, migration notes, and a documented compatibility decision before
implementation. Rationale: stable contracts reduce integration risk and keep service behavior
reliable across local and Azure validation.

### IV. Simplicity and Bounded Phase-1 Scope
Phase-1 delivery MUST prioritize the minimum viable architecture required for the approved
Coverage Diagnostics flow. No speculative abstractions, orchestration services,
user-intent classification logic, or out-of-scope capabilities are allowed without written
approval and a later-phase plan. Rationale: bounded scope reduces delivery risk and preserves
focus on the approved business flow.

### V. Cloud Readiness and Operational Quality
The local implementation MUST validate cloud-relevant behavior before Azure deployment testing.
Structured logs, correlation IDs, actionable errors, and observability basics MUST be present
for all in-scope flows. Rationale: parity between local and cloud behaviors is required to
reduce deployment risk and make failures diagnosable.

## Phase-1 Scope and Delivery Model
Phase-1 focuses only on Coverage Diagnostics capability. The Phase-1 boundary is intentionally
narrow and MUST remain limited to the following supported functions:

- Coverage validation
- Service availability checks
- Network outage visibility
- Serving market correlation
- Roaming visibility
- Connectivity state analysis

This capability provides real-time network visibility and coverage intelligence to support
network troubleshooting and coverage validation. Its responsibilities are limited to:

- Coverage validation
- Network availability assessment
- Outage detection
- Serving market identification
- Registration analysis
- Roaming network verification
- Health status retrieval

In-scope functional areas are coverage check intake, workflow execution for coverage
diagnostics, coverage and network status assessment, RCA and recommendation generation,
response composition, Azure OpenAI-assisted reasoning, and required service integrations for
this flow. User intent classification, agent workflow orchestration, and any broader autonomous
or multi-workflow capability are explicitly out of scope for Phase-1 and MUST be deferred to
later phases unless formally approved.

Delivery MUST begin in local development and testing, with cloud deployment testing only after
local parity validation succeeds. All in-scope behavior MUST be validated for the happy path,
major error path, dependency-failure behavior, latency, failure handling, and log completeness
before phase signoff. Azure validation MUST include deployment verification, service
connectivity checks, and runtime smoke tests for in-scope endpoints only.

## Quality Gates and Review Workflow
Gate 1 (spec quality): requirements are complete, testable, and unambiguous.
Gate 2 (plan quality): architecture and constraints align with requirements and scope.
Gate 3 (task quality): tasks fully cover requirements and include test work.
Gate 4 (pre-merge): tests pass, coverage diagnostics flow works end-to-end in local validation.
Gate 5 (cloud validation): deployment smoke tests pass in Azure for Phase-1 flows only.

All implementation tasks MUST satisfy these gates before merge or phase signoff. Compliance
review is mandatory in every PR and before final Phase-1 signoff. Out-of-scope expansion
requests MUST be documented, deferred, or explicitly approved through a formal change-control
decision. Any constitution change requires documented rationale and a semver version bump.

## Governance
This constitution is the governing standard for planning, implementation, review, and amendment
for the NORA Wholesale Care Phase-1 effort. Constitution compliance is mandatory for planning,
implementation, review, and release decisions. Any deviation MUST be documented in the active
plan with the reason, scope, and follow-up action.

Amendments MUST include a rationale, a semver change decision, and a version update in this
document. MAJOR changes remove or redefine non-negotiable principles; MINOR changes add new
principles or materially expand guidance; PATCH changes clarify wording or improve precision
without changing intent. Compliance review is required in every PR and before phase signoff.

Phase-1 Definition of Done:
- All in-scope requirements implemented and validated.
- End-to-end coverage diagnostics flow validated locally and in Azure deployment testing.
- No unresolved critical defects for in-scope behavior.
- Traceability artifacts are complete and current.

**Version**: 1.1.1 | **Ratified**: 2026-09-05 | **Last Amended**: 2026-09-05

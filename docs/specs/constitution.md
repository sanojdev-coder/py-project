# Project Constitution

## Purpose
This project follows a simple spec-driven development workflow. The purpose is to keep requirements clear, implementation focused, and validation repeatable.

## Core principles
1. Define the problem before writing code.
2. Write a failing test before implementing behavior.
3. Implement the smallest change that satisfies the requirement.
4. Validate with automated tests before considering the feature complete.
5. Keep documentation aligned with the current behavior.
6. Prefer clarity and maintainability over unnecessary complexity.

## Standards
- Use Python with simple, readable code.
- Maintain one clear responsibility per module or function.
- Keep tests specific to observable behavior.
- Prefer deterministic outputs and explicit logic.
- Document assumptions and acceptance criteria for each feature.

## Quality bar
A feature is complete only when all of the following are true:
- The requirement is written in a spec
- The behavior is captured by tests
- The implementation passes those tests
- The feature matches the defined acceptance criteria
- The code remains understandable and maintainable

## Review expectations
- Review behavior against the spec, not only against implementation details.
- Do not add scope beyond the agreed acceptance criteria unless the requirement changes.
- Keep changes small, testable, and traceable.

## Definition of done
A task is done when:
- the requirement is clear
- the failing test is in place
- the implementation is complete
- the relevant tests pass
- the result is documented in the spec or plan

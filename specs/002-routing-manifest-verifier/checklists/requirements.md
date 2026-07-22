# Specification Quality Checklist: Routing Manifest Schema and Verifier

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-07-22
**Feature**: [spec.md](../spec.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic (no implementation details)
- [x] All acceptance scenarios are defined
- [x] Edge cases are identified
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification

## Notes

Each box below was checked by performing the stated check against the written
spec, not by inference from the spec having been carefully written. Constitution
Principle XXV: a check that has only ever passed carries no information.

**Issues found and fixed during validation:**

- SC-003 originally read "finishes fast enough to run on every proposed change
  without authors noticing the delay" — unmeasurable, since "noticing" has no
  threshold. Rewritten with a five-second bound.

**Implementation-detail scan (Content Quality, item 1).** The approved design
names JSON Schema draft 2020-12, Python, bash and PowerShell, exit code 1, and the
literal severity labels ERROR/WARN/INFO. Each was checked for and is absent from
the spec: FR-023 says "both major operating system families" rather than naming
the two shell languages; FR-017 says "blocking, advisory, informational" rather
than the literal labels; FR-017 says "signal failure" rather than naming an exit
code; FR-025 and the Assumptions refer to "a published, machine-readable
definition of the format" rather than naming the schema dialect. Those details
belong in plan.md.

**Re-validated after the 2026-07-22 clarification session.** Five clarifications
were integrated, adding FR-001a, FR-012a/b/c, FR-024a/b and SC-008, and extending
two edge cases and one assumption. All 16 items re-checked against the updated
spec; all still pass.

That session surfaced one requirement whose absence would have been a real defect:
without FR-024a, this project would have shipped a gate whose only input was an
empty directory — passing while verifying nothing, which is precisely the failure
mode Principle XXV exists to catch. The gate would have been green from its first
run and meaningless.

**Second borderline case, added by clarification.** FR-024b says the pass/fail
signal is carried by "the run's exit status". Exit status is arguably a technical
mechanism rather than a business outcome. It is kept because the alternative
phrasings ("the check reports failure") leave unstated *how* an automated gate
learns the verdict, and that is a contract the plan must honor rather than choose.

**One borderline case, deliberately kept.** The Assumptions section states that
the extension mechanism provides no means to intercept model selection. This is
arguably a technical fact rather than a business one, but it is the single
constraint that determines the feature's entire scope — verify rather than
execute. Omitting it would leave a reader to assume routing happens. Recorded here
as a conscious exception rather than an oversight.

**Testability spot-check.** FR-011 through FR-021 each map to at least one
acceptance scenario in User Stories 2, 3 or 4 or to a listed edge case. FR-022,
FR-025 and FR-027 are verified by inspection of the shipped artifacts rather than
by execution, which is appropriate for documentation and fixture requirements.

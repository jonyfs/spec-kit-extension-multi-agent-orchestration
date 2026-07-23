# Implementation Plan: Routing Manifest Schema and Verifier

**Feature**: 002-routing-manifest-verifier
**Spec**: [spec.md](./spec.md)
**Design**: [../../docs/superpowers/specs/2026-07-22-routing-manifest-schema-design.md](../../docs/superpowers/specs/2026-07-22-routing-manifest-schema-design.md)
**Date**: 2026-07-22

## Constitution Check

| Principle | How this plan satisfies it |
|---|---|
| XV Declarative routing | All routing facts live in `skill-{skill}.yml`; the JSON Schema is the normative form; no routing value in command prose or scripts. |
| XVI Harness agnosticism | No manifest field names a harness; `docs/HARNESSES.md` created with every row `unverified`; color declared as hex + ANSI. |
| XVII Token guardrails | Schema requires `max_total_tokens` and `action_on_limit`; validator errors on missing/zero/negative and on `truncate_context` with `writes_artifacts: true`. |
| XVIII Bounded parallelism | Validator errors on duplicate `artifacts.output` and on `max_concurrent_agents` > 1 with a non-null output. |
| XIX Model IDs as config | Manifests carry `provider_env`/`model_env`, never literal model names; example manifests use those references. |
| XX Route only real skills | Catalog parsed from the constitution's Skill Routing Catalog table; unknown stage is ERROR, uninstalled is INFO. |
| XXIII Effort normalization | Schema enum `low|medium|high|max`; `additionalProperties:false` rejects provider knobs; `docs/ROUTING.md` holds the ladder table with a verification date. |
| XXIV Graph retrieval | `context.retrieval` block; missing graphify degrades to WARN, never ERROR. |
| XXV Gate must fail | `tests/fixtures/invalid-routing/` plus `scripts/test-routing-validator.sh` assert rejection for each planted reason; a valid fixture proves it is not a blanket rejector. |
| V Script parity | `routing-check.sh` and `routing-check.ps1` are thin wrappers over one Python core. |
| VII Install-test | The `orchestration` package installs, lists, and removes cleanly; `install-test.sh` already exercises every package. |
| VIII Versioning | `template/CHANGELOG.md` gets a `2.0.0` entry (id and command surface change from `trace`); root `CHANGELOG.md` records the feature. |

No principle requires a Complexity Tracking exception. Nothing here exceeds the
upstream schema.

## Technical Approach

**Language:** Python 3.12 for the validator (matches `validate-extension.py`;
PyYAML already a CI dependency). Bash and PowerShell wrappers are thin.

**Two artifacts, split by capability (design decision A):**

1. `template/routing-manifest.schema.json` — JSON Schema draft 2020-12. Owns
   *shape*: required keys, closed enums, `additionalProperties: false`, and the
   conditional `if action_on_limit == truncate_context then require
   truncation_priority`.
2. `scripts/validate-routing.py` — owns *semantics*: everything cross-field and
   cross-file that JSON Schema cannot express, plus environment probing.

**Validator layers** (spec FR-011..FR-021):
- Layer 1 shape: validate each manifest against the schema.
- Layer 2 single-manifest semantics: catalog membership, budget sanity,
  truncate/writes conflict, parallelism/ownership conflict, ANSI presence.
- Layer 3 cross-manifest + environment: duplicate `artifacts.output`, unset
  `*_env` variables, graphify availability.

**Catalog source** (FR-012a/b): parse the `## Skill Routing Catalog` table from
`.specify/memory/constitution.md`, located by walking up from the manifest
directory. Absent or unreadable table → loud ERROR, never an empty catalog.

**Severity → exit** (FR-017): ERROR / WARN / INFO printed; exit 1 iff any ERROR.

**Discovery** (FR-001a): the validator reads `skill-*.yml` from directories passed
on the command line. The documented default for a consuming project is
`.specify/extensions/orchestration/config/`. Package templates in
`template/config/` are never read as declarations.

**Dogfooding** (FR-024a): this repository installs its own real declarations at
`.specify/extensions/orchestration/config/skill-{plan,implement}.yml` (no
`CUSTOMIZE` markers — real env-var names), and the CI routing job validates that
directory so the gate runs against real input.

## File Manifest

Created:
- `template/routing-manifest.schema.json`
- `template/config/skill-plan.yml` (template, with `CUSTOMIZE` markers)
- `template/config/skill-implement.yml` (template, with `CUSTOMIZE` markers)
- `scripts/validate-routing.py`
- `scripts/test-routing-validator.sh`
- `tests/fixtures/valid-routing/skill-plan.yml`
- `tests/fixtures/invalid-routing/` (one manifest per planted violation)
- `.specify/extensions/orchestration/config/skill-plan.yml` (real, dogfood)
- `.specify/extensions/orchestration/config/skill-implement.yml` (real, dogfood)
- `docs/ROUTING.md`
- `docs/HARNESSES.md`

Rewritten:
- `template/extension.yml` (`id: orchestration`, command `speckit.orchestration.check`)
- `template/commands/check.md`
- `template/README.md`
- `template/CHANGELOG.md`
- `README.md` (root: template project → orchestration extension)
- `CHANGELOG.md` (root: feature entry)
- `.github/workflows/ci.yml` (add routing gate)

Removed:
- `template/trace-config.yml`
- `template/scripts/bash/trace-check.sh`
- `template/scripts/powershell/trace-check.ps1`

## Testing Strategy

Per Principle XXV, the validator is proven fallible before it is trusted:
- `tests/fixtures/invalid-routing/` — manifests each violating exactly one rule:
  missing budget, `truncate_context`+`writes_artifacts`, a provider knob, two
  sharing an output, an unknown skill, `waves` without concurrency.
- `tests/fixtures/valid-routing/` — a valid set proving no blanket rejection.
- `scripts/test-routing-validator.sh` — asserts exit 1 AND that each expected
  violation string appears, mirroring `test-validator.sh`.

CI gains a `routing` job running the validator against the dogfood directory and
then `test-routing-validator.sh`.

## Out of Scope

Any executor acting on manifest values; the remaining seven catalog manifests;
`speckit.baseline` (unverified); the orchestration-state validator (Principle
XXII — separate feature).

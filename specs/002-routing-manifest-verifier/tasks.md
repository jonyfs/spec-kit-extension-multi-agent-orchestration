# Tasks: Routing Manifest Schema and Verifier

**Feature**: 002-routing-manifest-verifier
**Plan**: [plan.md](./plan.md)

Tasks are grouped by user story so each story is independently completable.
`[P]` marks tasks that touch disjoint files and may run in parallel.

## US1 — Declare how a skill should run (P1)

- [x] T001 Write `template/routing-manifest.schema.json` (JSON Schema draft
  2020-12): required keys, enums (`reasoning_effort`, `action_on_limit`,
  `parallelism_mode`, `traversal`), `additionalProperties:false`, and the
  conditional requiring `truncation_priority` when `action_on_limit` is
  `truncate_context`.
- [x] T002 [P] Write `template/config/skill-plan.yml` — read-mostly example, with
  `CUSTOMIZE` markers on the env-var names.
- [x] T003 [P] Write `template/config/skill-implement.yml` — parallel/writing
  example, with `CUSTOMIZE` markers.
- [x] T004 [P] Write the real dogfood declarations at
  `.specify/extensions/orchestration/config/skill-{plan,implement}.yml` (no
  markers; real env-var names).

## US2 — Catch a broken declaration (P1)

- [x] T005 Write `scripts/validate-routing.py`: load manifests, Layer 1 (schema),
  Layer 2 (single-manifest semantics), Layer 3 (cross-manifest + environment),
  ERROR/WARN/INFO, exit 1 iff any ERROR.
- [x] T006 Implement catalog parsing from the constitution's Skill Routing Catalog
  table, located by walking up from the manifest directory; loud ERROR on absent
  or unreadable table (FR-012a/b).
- [x] T007 Implement the distinct handling of unknown (ERROR) vs uninstalled
  (INFO) stages (FR-012c, FR-019).

## US3 — Run anywhere without false alarms (P2)

- [x] T008 In the validator, classify missing graphify, unset `*_env` variables,
  and unverified harness as WARN, and inactive (uninstalled) manifests as INFO;
  confirm exit stays 0 when only WARN/INFO present (FR-018, FR-019).
- [x] T009 Report "no declarations found" distinctly from success (FR-021).

## US4 — Prove the check can fail (P2)

- [x] T010 [P] Create `tests/fixtures/valid-routing/skill-plan.yml`.
- [x] T011 [P] Create `tests/fixtures/invalid-routing/` — one manifest per planted
  violation (missing budget; truncate+writes; provider knob; duplicate output;
  unknown skill; waves without concurrency).
- [x] T012 Write `scripts/test-routing-validator.sh` asserting exit 1 and each
  expected violation string, plus a pass on the valid fixture.

## Extension packaging (US1/US2 delivery surface)

- [x] T013 Rewrite `template/extension.yml` to `id: orchestration`, command
  `speckit.orchestration.check`, config entries for the two manifest templates and
  the schema.
- [x] T014 Rewrite `template/commands/check.md` for `speckit.orchestration.check`.
- [x] T015 [P] Write `template/scripts/bash/routing-check.sh` (thin wrapper).
- [x] T016 [P] Write `template/scripts/powershell/routing-check.ps1` (thin wrapper).
- [x] T017 Remove `template/trace-config.yml` and the two `trace-check` scripts.

## Documentation and gates

- [x] T018 [P] Write `docs/ROUTING.md`: every field, the effort ladder mapped per
  provider with a verification date, the severity model, the stated non-coverage.
- [x] T019 [P] Write `docs/HARNESSES.md`: five categories, every engine row
  `unverified`, graphify-availability column.
- [x] T020 Add the `routing` job to `.github/workflows/ci.yml`.
- [x] T021 [P] Rewrite root `README.md` (template project → orchestration extension).
- [x] T022 [P] Rewrite `template/README.md` and `template/CHANGELOG.md`.
- [x] T023 Add root `CHANGELOG.md` entry for feature 002.

## Verification

- [x] T024 Run `validate-routing.py` on the dogfood dir → passes;
  `test-routing-validator.sh` → passes; `validate-extension.py template` → OK;
  `check-placeholders.sh` → clean. Record decisive output.

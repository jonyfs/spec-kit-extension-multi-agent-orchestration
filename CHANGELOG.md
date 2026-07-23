# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Full routing-manifest coverage.** This project now declares all nine
  installed workflow stages in `.specify/extensions/orchestration/config/`
  (constitution, specify, clarify, plan, checklist, tasks, analyze, implement,
  converge), so the CI routing gate verifies the whole catalog rather than two
  examples. Amending stages (clarify, converge), the read-only stage (analyze),
  and implement own no single artifact (`output: null`), which is what keeps
  specify/clarify and tasks/converge from colliding on one file under Principle
  XVIII. `speckit.converge` surfaces as INFO "in catalog but not installed",
  exercising the unknown-vs-uninstalled distinction on a real case.
- **Two harness rows verified** in `docs/HARNESSES.md` (2026-07-23), each scoped
  to what a real run exercised: Claude Code CLI (verifier run against the working
  tree, graphify on PATH) and GitHub Actions (CI routing job reading manifests
  from the checkout; env injection of routing variables not yet exercised).

- **Multi-agent orchestration scope.** This repository is now the routing
  orchestration extension itself. The constitution advanced from 1.6.0 to 2.3.0
  across four amendments, adding Principles XV–XX (declarative routing, harness
  agnosticism, fail-closed token guardrails, bounded parallelism, model IDs as
  configuration, route-only-verified-skills), XXI–XXIII (worktree-isolated
  macro-parallelism, auditable non-authoritative orchestration state, normalized
  reasoning effort), XXIV (graph-backed retrieval), and adopting the upstream
  template's "A Check That Cannot Fail Is Not a Check" as XXV.
- **`orchestration` extension** in `template/`: a routing-manifest verifier.
  `speckit.orchestration.check` reads per-skill `skill-{skill}.yml` declarations
  and reports blocking / advisory / informational findings, failing only on a
  blocking one. Ships `routing-manifest.schema.json` (JSON Schema draft 2020-12),
  two manifest templates, a Python verifier, and paired bash/PowerShell wrappers.
- `template/scripts/python/validate-routing.py` — three-layer verifier (shape,
  single-manifest semantics, cross-manifest + environment). The stage catalog is
  parsed from the constitution rather than copied, so code and governance cannot
  diverge (Principle XX).
- `scripts/test-routing-validator.sh` and `tests/fixtures/{valid,invalid}-routing/`
  — assert the routing verifier rejects a broken manifest set for each planted
  reason and passes a valid one (Principle XXV). CI gains a `routing` job running
  both against this project's own dogfood declarations in
  `.specify/extensions/orchestration/config/`.
- `docs/ROUTING.md` (manifest field reference, effort ladder, severity model,
  stated non-coverage) and `docs/HARNESSES.md` (harness capability matrix, every
  row `unverified`).
- Feature artifacts under `specs/002-routing-manifest-verifier/`
  (spec, plan, tasks, checklist) and the approved design under
  `docs/superpowers/specs/`.

### Removed

- The `trace` reference extension that previously occupied `template/`, superseded
  by `orchestration`. Its history remains on the `upstream` template.

- `scripts/test-validator.sh` and `tests/fixtures/invalid-extension/` — assert that
  the manifest validator rejects a package violating six rules, and rejects it for the
  right reasons. Constitution Principle XV: a gate that has only ever passed carries no
  information, because passing and being unreachable produce identical output.

### Fixed

- `scripts/install-test.sh` could not pass on macOS for any package. The extension id
  was extracted with sed's `\s`, a GNU extension BSD sed silently ignores; and
  `specify extension list | grep -q` under `set -o pipefail` reported the *matching*
  case as a failure, because `grep -q` exits at first match and `specify` takes SIGPIPE.
  Both were invisible while the repository had no extension to test.
- `.specify/bridge-events.jsonl` was tracked in git despite being gitignored — adding a
  path to `.gitignore` does not untrack a file already committed. It is a runtime audit
  log the bridge extension appends to on every run.

- `sdd-master` skill (`.claude/skills/sdd-master/`) — proactive expertise on
  spec-driven development and Spec Kit. A router holding the four-band effort
  classification and signal table, plus four references loaded on demand and split
  by source of truth: `workflow.md`, `craft.md`, `recovery.md`, `ecosystem.md`.
  Its guidance is deliberately proportionate — the documented failure of
  spec-driven development is applying it uniformly, not skipping it. Evaluated
  against a no-skill baseline on three behavioral cases (17 of 17 assertions) and
  a 20-query trigger set.

- Project constitution (`.specify/memory/constitution.md`) defining thirteen
  principles for authoring Spec Kit extensions.
- `docs/HOOKS.md` — reference for both hook layers: Spec Kit lifecycle hooks
  declared in `extension.yml`, and harness hooks that execute shell commands.
- `docs/PACKAGING.md` — reference for all four distribution forms the `specify`
  CLI supports, verified against specify-cli 0.11.3.
- `scripts/validate-extension.py` — manifest, command-namespacing, hook, and
  script-parity validation.
- `scripts/check-placeholders.sh` — guards against template placeholders
  surviving into a release.
- `scripts/install-test.sh` — the install → list → info → remove cycle.
- GitHub Actions CI running lint, manifest validation, the placeholder guard,
  and the install-test cycle on every pull request.
- Vendored `caveman` skill from `juliusbrussee/caveman` (MIT) with provenance.
- Six community Spec Kit extensions installed as the project baseline:
  `worktrees`, `ship`, `critique`, `staff-review`,
  `speckit-superpowers-bridge`, and `onboard`.

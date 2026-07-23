---
description: Verify the project's routing manifests against the routing principles, reporting blocking, advisory, and informational findings.
scripts:
  sh: scripts/bash/routing-check.sh
  ps: scripts/powershell/routing-check.ps1
---

# Routing manifest check

Verify every routing manifest declared for this project. A routing manifest
(`skill-{skill}.yml`) states how one workflow stage should run: its provider and
model by environment reference, reasoning effort, token budget and the action
taken when it is reached, parallelism, graph retrieval, and which artifact the
stage owns exclusively.

This command **verifies** those declarations. It does not route anything: the
Spec Kit extension mechanism cannot intercept which model a stage actually runs
under.

## What it does

Run the platform script (`scripts/bash/routing-check.sh` or
`scripts/powershell/routing-check.ps1`), passing the manifest directory. With no
argument it reads this project's own configuration directory,
`.specify/extensions/orchestration/config/`. The shipped files under the
package's `config/` are templates to copy from, never read as declarations.

The verifier reports findings at three levels and exits non-zero only when a
blocking finding exists:

- **ERROR** (blocking): a manifest breaks a rule — invalid shape, a provider's
  own reasoning knob, a missing or non-positive token budget, a writing stage set
  to drop context on exhaustion, two stages claiming the same output, a stage not
  in the catalog, or a parallel stage claiming a single owned file.
- **WARN** (advisory): an environment gap that changes behavior without breaking
  a rule — an unset provider/model variable, or graph retrieval enabled while the
  retrieval tool is absent.
- **INFO**: a manifest for a catalog stage not installed here, or the aggregate
  declared budget.

The catalog of valid stages is read from the Skill Routing Catalog table in
`.specify/memory/constitution.md`, so this check and governance cannot diverge.

## Not covered

The verifier does not check whether a configured model is available to the caller
or is the one the current session uses; both require an authenticated provider
call a gate cannot make. See `docs/ROUTING.md` for the full field reference, the
reasoning-effort ladder per provider, and the severity model.

`$ARGUMENTS` — an optional manifest directory to check instead of the default.

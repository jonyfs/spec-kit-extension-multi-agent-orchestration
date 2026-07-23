# Routing Manifests

A routing manifest declares how one workflow stage should run. This document is
the field reference required by Constitution Principle XV, the reasoning-effort
ladder required by Principle XXIII, and the severity model the verifier applies.

The extension **verifies** manifests; it does not route. The Spec Kit extension
mechanism cannot intercept which model a stage runs under, so a manifest is a
declared contract a reviewer and a CI gate can check, not an instruction the
runtime obeys. See `specs/002-routing-manifest-verifier/spec.md`.

## Location

One file per stage, named `skill-{skill}.yml`, in the consuming project's own
configuration directory: `.specify/extensions/orchestration/config/`. The files
shipped inside the package under `config/` are templates to copy from — the
verifier never reads them as a project's declarations (spec FR-001a).

The normative schema is `routing-manifest.schema.json` (JSON Schema draft
2020-12). Point your editor at it for completion and inline validation.

## Fields

| Path | Required | Type | Meaning |
|---|---|---|---|
| `schema_version` | yes | `"1.0"` | Manifest format version. |
| `skill` | yes | `speckit.<name>` | The stage this governs. Must be in the Skill Routing Catalog. |
| `routing.provider_env` | yes | string | Name of the env var carrying the provider. Never a literal provider name (XIX). |
| `routing.model_env` | yes | string | Name of the env var carrying the model. Never a literal model id (XIX). |
| `routing.reasoning_effort` | yes | `low\|medium\|high\|max` | Effort on the closed ladder. No provider-native knob permitted (XXIII). |
| `routing.ui_render.color` | yes | `#RRGGBB` | 24-bit log color. |
| `routing.ui_render.terminal_ansi` | yes | ANSI SGR code | Plain-terminal fallback; a harness without 24-bit color still renders the stage (XVI). |
| `governance.token_guardrails.max_total_tokens` | yes | integer > 0 | Spending ceiling. Absent, zero, or negative aborts the stage (XVII). |
| `governance.token_guardrails.action_on_limit` | yes | `halt\|checkpoint_and_halt\|truncate_context` | Behavior at the ceiling. |
| `governance.token_guardrails.truncation_priority` | conditional | string[] | Context sources to drop, lowest first. Required exactly when `action_on_limit` is `truncate_context`. |
| `execution_strategy.parallelism_mode` | when present | `serial\|waves` | Concurrency model for the stage. |
| `execution_strategy.max_concurrent_agents` | conditional | integer > 0 | Concurrency cap. Required when mode is `waves` (XVIII). |
| `context.retrieval.enabled` | when present | boolean | Whether the stage retrieves from the graphify graph (XXIV). |
| `context.retrieval.query_budget_tokens` | conditional | integer > 0 | Retrieval budget. Required when `enabled` is true. |
| `context.retrieval.traversal` | conditional | `bfs\|dfs` | Traversal strategy. Required when `enabled` is true. |
| `artifacts.output` | yes | string or null | The single file the stage owns, or null when it owns none (XVIII). |
| `artifacts.writes_artifacts` | yes | boolean | Whether the stage writes at all. A writing stage may not use `truncate_context` (XVII). |

`additionalProperties` is false at every level: any key not listed above is a
shape error. This is what mechanizes Principle XXIII — a provider's own effort
parameter (for example a thinking-token budget) cannot appear in a manifest.

## Reasoning-effort ladder

Manifests declare effort only as `low | medium | high | max`. Translation to each
provider's own parameter belongs here, not in a manifest. Principle XIX requires
every provider mapping to carry the date it was confirmed against that provider's
current documentation.

> **Verification status: UNVERIFIED as of 2026-07-22.** The mappings below are the
> intended shape, not confirmed against live provider documentation in this
> change. Each MUST be confirmed and dated before the extension is released, per
> Principle XIX. Until then, treat every row as provisional. A rung with no
> provider equivalent is a documented no-op, never a silent substitution.

| Ladder rung | Provider effort parameter (shape) | Status |
|---|---|---|
| `low` | minimal / lowest effort setting the provider exposes | unverified |
| `medium` | mid effort setting | unverified |
| `high` | high effort setting | unverified |
| `max` | maximum effort the provider exposes | unverified |

A provider that exposes no effort control at all is still routable: the rung
becomes a documented no-op for that provider, and the stage runs at the provider's
default. The manifest does not change.

## Severity model

The verifier reports every finding across every manifest in one run and derives
its exit status solely from whether any blocking finding exists (spec FR-017,
FR-020).

| Level | Fails the build? | Examples |
|---|---|---|
| ERROR | yes (exit 1) | invalid shape; provider knob present; missing/zero/negative budget; `truncate_context` on a writing stage; duplicate `artifacts.output`; unknown stage; `waves` claiming a single output |
| WARN | no | unset `provider_env`/`model_env`; retrieval enabled but graphify absent; `truncation_priority` set without `truncate_context` |
| INFO | no | a manifest for a cataloged but uninstalled stage; the aggregate declared budget |

Exiting non-zero only on ERROR is what lets the same gate run on a CI runner that
legitimately lacks graphify and the model environment variables without false
alarms, which Principles XVI, XX and XXIV require.

An empty manifest directory is reported distinctly and is **not** success: a check
with nothing to examine has not passed (Principle XXV lineage; spec FR-021).

## The catalog

Valid stages are parsed at run time from the Skill Routing Catalog table in
`.specify/memory/constitution.md`. Code holds no copy, so adding a stage to
governance makes declarations for it valid without any code change (spec SC-008).
A row whose Source column is `unknown` — currently `speckit.baseline` — is not
routable and ships no manifest. An absent or unreadable catalog table halts the
verifier with an explicit failure rather than proceeding against an empty catalog.

## Not covered

The verifier does not check whether a configured model is available to the caller,
nor whether it is the model the current session uses. Both require an
authenticated call to a provider, and a gate running on a pull request from
outside the project cannot make one. This is a stated boundary, not an oversight.

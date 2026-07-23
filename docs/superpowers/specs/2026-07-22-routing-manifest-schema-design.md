# Routing Manifest Schema and Verifier — Design

**Date:** 2026-07-22
**Status:** Approved
**Governs:** Constitution v2.3.0, Principles XV, XVI, XVII, XVIII, XIX, XX, XXIII, XXIV, XXV

## Problem

Constitution v2.3.0 requires that every routing decision live in a declarative
YAML manifest, one per skill (Principle XV), and that a schema and validator for
those manifests exist and run as a CI gate. Neither exists. Six other principles
(XVII, XVIII, XIX, XX, XXIII, XXIV) impose rules on manifest content that are
currently unenforceable prose. This design defines the manifest format, the
artifacts that validate it, and the boundary of what validation can honestly
claim.

## Scope boundary: contract and verifier, not executor

A Spec Kit extension provides commands (Markdown that becomes an agent prompt)
and lifecycle hooks. It cannot intercept model selection: Claude Code runs the
session's model, and a CI runner runs whatever its workflow invokes. No API
exists through which a manifest could reroute `/speckit.plan` to a different
provider.

The manifest is therefore a **declared contract**, and this extension is its
**verifier**. It reports whether the current environment matches what the
manifests declare. It routes nothing. Any future executor is a separate piece of
work, outside this design.

This boundary is stated in the extension README so no user infers routing
behavior that does not exist.

## Package layout

The repository's `template/` directory becomes this extension's package,
replacing the inherited `trace` reference extension.

```text
template/
├── extension.yml                      # id: orchestration
├── routing-manifest.schema.json       # normative, JSON Schema draft 2020-12
├── config/
│   ├── skill-plan.yml                 # example: read-mostly skill
│   └── skill-implement.yml            # example: parallel, writing skill
├── commands/
│   └── check.md                       # speckit.orchestration.check
├── scripts/
│   ├── bash/routing-check.sh
│   └── powershell/routing-check.ps1
├── README.md
├── CHANGELOG.md
└── LICENSE
```

The semantic validator lives at `scripts/validate-routing.py`, in the repository
root alongside the other CI gates, because it is this project's gate rather than
code a user installs. The two packaged scripts are thin wrappers that locate the
manifests and invoke it.

**Known consequence:** upstream continues to evolve `template/`. Every future
upstream merge touching that directory will conflict. This is a recurring cost
accepted deliberately, not a one-time one.

**Principle V trade-off:** behavioral parity between the bash and PowerShell
variants is achieved by making both thin wrappers over one Python implementation,
rather than reimplementing the logic twice. Duplicated logic in two languages
diverges over time; a shared core cannot. Python becomes a declared dependency of
the extension.

**`check-placeholders.sh` line 14** hardcodes `./template/` as an allowed
placeholder prefix and must be updated when the package identity changes.

## Manifest format

One file per skill at `config/skill-{skill}.yml`. Example, `skill-implement.yml`:

```yaml
schema_version: "1.0"
skill: "speckit.implement"

routing:
  # CUSTOMIZE: name the environment variables your setup defines.
  provider_env: "SPECKIT_IMPLEMENT_PROVIDER"
  model_env: "SPECKIT_IMPLEMENT_MODEL"
  reasoning_effort: "medium"        # low | medium | high | max
  ui_render:
    color: "#2196F3"
    terminal_ansi: "92"

governance:
  token_guardrails:
    max_total_tokens: 1500000
    action_on_limit: "checkpoint_and_halt"
    # truncation_priority is required only when action_on_limit is
    # truncate_context; it lists context sources lowest-priority first.

execution_strategy:
  parallelism_mode: "waves"         # serial | waves
  max_concurrent_agents: 4

context:
  retrieval:
    enabled: true
    query_budget_tokens: 8000
    traversal: "bfs"                # bfs | dfs

artifacts:
  output: null
  writes_artifacts: true
```

### Field decisions and their sources

**`provider_env` / `model_env` rather than `provider` / `model`.** Principle XIX
forbids a hardcoded model identifier, and Principle XV requires environment-
varying values to be referenced by variable name rather than written as literals.
The manifest names the variable; the value lives outside it. A manifest therefore
does not expire when a provider deprecates a model.

**`reasoning_effort` on a closed ladder, with no provider-native knob.**
`additionalProperties: false` throughout the schema is what mechanizes Principle
XXIII: a manifest containing `thinking_budget` or `openai_reasoning_effort` is
rejected. The ladder-to-provider mapping lives in the `docs/ROUTING.md` table,
not in any manifest.

**`writes_artifacts` stated explicitly.** Principle XVII permits
`truncate_context` only for skills that do not write artifacts. The explicit flag
lets the validator apply that rule without inferring intent from the skill name.

**`artifacts.output` is nullable but required to be present.** `null` means the
skill owns no single file (`implement`, `analyze`). A path means exclusive
ownership, and it is across this field that the validator detects collisions
between manifests under Principle XVIII.

**`truncation_priority` is conditionally required.** Principle XVII permits
`truncate_context` only when the manifest declares the truncation order. The
field is an ordered list of context source names, lowest priority first, and the
schema requires it exactly when `action_on_limit` is `truncate_context` — a JSON
Schema `if`/`then` clause, not a semantic check.

**`agent_harness` is deliberately absent.** Binding a manifest to a named harness
contradicts Principle XVI directly. The harness is environment, not skill
configuration.

## Verifier behavior

Three layers, run in order. An ERROR in one layer does not stop later layers: the
report is always complete, because an author fixing manifests wants every problem
at once.

### Layer 1 — shape (JSON Schema)

Missing required field, value outside an enum, wrong type, unknown property. All
ERROR. Principle XXIII's forbidden provider knobs die here via
`additionalProperties: false`.

### Layer 2 — single-manifest semantics

| Check | Principle | Level |
|---|---|---|
| `skill` appears in the Skill Routing Catalog | XX | ERROR |
| `max_total_tokens` missing, zero, or negative | XVII | ERROR |
| `truncate_context` with `writes_artifacts: true` | XVII | ERROR |
| `parallelism_mode: waves` without `max_concurrent_agents` | XVIII | ERROR |
| `max_concurrent_agents` > 1 with non-null `artifacts.output` | XVIII | ERROR |
| `truncation_priority` present while `action_on_limit` is not `truncate_context` | XVII | WARN |
| `ui_render` carrying a hex value but no `terminal_ansi` | XVI | ERROR |
| A catalog skill with no corresponding manifest | XX | INFO |
| A manifest for a skill not installed in this project | XX | INFO |

### Layer 3 — cross-manifest and environment

| Check | Principle | Level |
|---|---|---|
| Two manifests declaring the same `artifacts.output` | XVIII | ERROR |
| Variable named by `provider_env` / `model_env` unset | XV | WARN |
| `retrieval.enabled: true` but `graphify` absent from PATH | XXIV | WARN |
| `graphify-out/` absent while retrieval is enabled | XXIV | WARN |
| Aggregate budget across concurrent skills | XVII, XXI | INFO |

### Exit codes

Exit 1 only when at least one ERROR is present. WARN and INFO are reported and
exit 0. This is what lets the gate run on a CI runner that legitimately has
neither graphify nor the model environment variables set, without breaking
anyone's build — which Principles XVI, XX and XXIV all require.

### Stated non-coverage

The verifier does not check whether a configured model is available to the
caller, nor whether it is the model the current session is actually using. Both
would require an authenticated provider call, and a gate needing a credential
cannot run on a third-party pull request. The report states this explicitly
rather than leaving the omission to be inferred.

## Testing

Principle XXV requires that every gate be observed failing before it is trusted.
Mirroring the pattern upstream established in `tests/fixtures/invalid-extension/`:

- `tests/fixtures/invalid-routing/` — manifests each violating one rule from a
  different layer: one missing `max_total_tokens`, one pairing
  `truncate_context` with `writes_artifacts: true`, one carrying a provider-native
  knob, two contending for the same `artifacts.output`, one naming a skill outside
  the catalog.
- `tests/fixtures/valid-routing/` — a valid set, proving the validator is not a
  blanket rejector.
- `scripts/test-routing-validator.sh` — asserts the validator exits 1 **and**
  reports exactly the expected violations. A validator exiting 1 for the wrong
  reason passes a loose test; this one asserts the list.

CI gains a fifth job invoking both fixtures.

## Documentation

`docs/ROUTING.md` documents every manifest field, the reasoning-effort ladder
mapped to each provider's parameter with a recorded verification date per
Principle XIX, the severity model, and the stated non-coverage above.

## Out of scope

- Any executor that acts on manifest values
- Manifests for the remaining seven catalog skills — the format is proven on two
  first
- `docs/HARNESSES.md`, `README.md` rewrite, `CHANGELOG.md` entries — tracked
  separately as constitution follow-ups
- `speckit.baseline`, which remains unverified under
  `TODO(SKILL_CATALOG_VERIFICATION)` and ships no manifest

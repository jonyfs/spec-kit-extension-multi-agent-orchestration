# orchestration — Multi-Agent Routing Verifier

A Spec Kit extension that verifies per-skill **routing manifests** against a
project's governance. A routing manifest (`skill-{skill}.yml`) declares how one
workflow stage should run — its provider and model by environment reference,
reasoning effort, token budget and the action taken at the ceiling, parallelism,
graph retrieval, and which artifact the stage owns exclusively.

It **verifies** declarations; it does not route. The Spec Kit extension mechanism
cannot intercept which model a stage actually runs under, so a manifest is a
declared contract a reviewer and a CI gate can check, not an instruction the
runtime obeys.

## What it checks

The verifier reports findings at three levels and fails only on a blocking one:

| Level | Fails? | Examples |
|---|---|---|
| ERROR | yes | invalid shape; a provider's own reasoning knob; missing/zero/negative token budget; a writing stage set to drop context; two stages claiming the same output; an unknown stage; a parallel stage claiming a single owned file |
| WARN | no | an unset provider/model variable; retrieval enabled while graphify is absent; dead truncation config |
| INFO | no | a manifest for a cataloged but uninstalled stage; the aggregate declared budget |

Exiting non-zero only on ERROR is what lets the same check run on a developer's
machine and on a CI runner lacking the optional tooling without false alarms.

The catalog of valid stages is read from the Skill Routing Catalog table in the
project's `.specify/memory/constitution.md`, so the check and governance cannot
diverge.

## Install

From a local directory:

```bash
specify extension add --dev /path/to/template
specify extension list
```

Removal:

```bash
specify extension remove orchestration --force
```

### Supported distribution forms

| Form | Supported |
|---|---|
| Local directory (`--dev`) | Yes |
| Custom URL (`--from`) | Yes |
| Catalog (`specify extension add orchestration`) | No — not submitted to a catalog |
| Bundled in the CLI | No — bundling is reserved for core extensions |

## Usage

```text
/speckit.orchestration.check
/speckit.orchestration.check .specify/extensions/orchestration/config
```

`speckit.orchestration.verify` is registered as an alias. The scripts can be run
directly, which is how CI uses them:

```bash
.specify/extensions/orchestration/scripts/bash/routing-check.sh
```

```powershell
.specify/extensions/orchestration/scripts/powershell/routing-check.ps1
```

With no argument they read the project's own configuration directory,
`.specify/extensions/orchestration/config/`. Exit codes:

| Code | Meaning |
|---|---|
| `0` | No blocking findings (advisories and notes may still be present) |
| `1` | At least one blocking finding, or no manifests found |

Both variants delegate to the same `scripts/python/validate-routing.py`, so their
behavior is identical by construction (Principle V).

## Where manifests live

Declarations live in the consuming project's own configuration directory,
`.specify/extensions/orchestration/config/`. The files shipped in this package
under `config/` are **templates**: copy them, resolve every `CUSTOMIZE` marker,
and place them in that directory. The verifier never reads the package templates
as a project's declarations.

Point your editor at `routing-manifest.schema.json` for completion and inline
validation while editing a manifest.

## Configuration

The extension has no config file of its own; the routing manifests it checks are
the configuration. See
[`docs/ROUTING.md`](https://github.com/jonyfs/spec-kit-extension-multi-agent-orchestration/blob/main/docs/ROUTING.md)
for the full field reference and the reasoning-effort ladder.

## Requirements

`specify` `>=0.2.0`, Python 3 with `pyyaml` and `jsonschema`. The verifier is
Python; the bash and PowerShell entry points are thin wrappers over it.

## What it deliberately does not do

It does not check whether a configured model is available to the caller or is the
one the current session uses — both need an authenticated provider call a gate
cannot make — and it does not act on manifest values at execution time.

## License

MIT — see [LICENSE](LICENSE).

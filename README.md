# Spec Kit Multi-Agent Orchestration

A [GitHub Spec Kit](https://github.com/github/spec-kit) extension that governs how
the spec-driven workflow's stages run across agents and execution harnesses. Each
stage declares — in YAML, outside any command prose — which provider and model
handle it, at what reasoning effort, under what token budget, with what
parallelism, and how its output is rendered. The extension **verifies** those
declarations against the project's governance; it does not route, because the
Spec Kit extension mechanism cannot intercept which model a stage runs under.

This repository was seeded from
[`spec-kit-extension-template`](https://github.com/jonyfs/spec-kit-extension-template),
which remains its `upstream` remote.

## What it does

A **routing manifest** (`skill-{skill}.yml`) is one workflow stage's declared
execution contract. The extension ships a normative JSON Schema for the format and
a verifier that reports findings at three levels — blocking, advisory,
informational — and fails a build only on a blocking one. That severity split is
what lets the same check run on a developer's machine and on a CI runner lacking
the optional tooling without false alarms.

```bash
specify extension add --dev /path/to/template   # installs the orchestration extension
/speckit.orchestration.check                     # verifies this project's manifests
```

See [`docs/ROUTING.md`](docs/ROUTING.md) for the manifest field reference, the
reasoning-effort ladder, and the severity model.

## The extension

[`template/`](template/) holds the `orchestration` extension: the schema
(`routing-manifest.schema.json`), two manifest templates under `config/`, the
`speckit.orchestration.check` command, and paired bash/PowerShell wrappers over a
single Python verifier. It installs, runs, and removes as a real Spec Kit
extension.

This project also dogfoods it: [`.specify/extensions/orchestration/config/`](.specify/extensions/orchestration/config/)
holds this repository's own real routing declarations, and CI verifies them, so
the gate runs against genuine input rather than an empty directory.

## Documentation

| Document | What it answers |
|---|---|
| [`.specify/memory/constitution.md`](.specify/memory/constitution.md) | The non-negotiable rules — 25 principles governing routing, harnesses, budgets, parallelism, retrieval, and gates. |
| [`docs/ROUTING.md`](docs/ROUTING.md) | Every manifest field, the effort ladder per provider, the severity model, and what verification does not cover. |
| [`docs/HARNESSES.md`](docs/HARNESSES.md) | How manifest values reach a run on each harness, and which capabilities each provides. |
| [`docs/HOOKS.md`](docs/HOOKS.md) | The two hook layers and how to avoid confusing them. |
| [`docs/PACKAGING.md`](docs/PACKAGING.md) | How an extension reaches a user, and the package layout each path needs. |

## What is deliberately not here

- **No executor.** The extension verifies contracts. Acting on manifest values at
  execution time, if ever built, is separate work.
- **No live model check.** Verification never asks a provider whether a configured
  model exists or is in use; that needs a credential a gate on an outside pull
  request cannot hold.
- **No unverified claims.** A harness row is `unverified` until a real run is
  recorded against it — two are verified so far, the rest are not; and
  `speckit.baseline` ships no manifest until its existence is confirmed.

## Validation tooling

| Script | Enforces |
|---|---|
| `scripts/validate-extension.py` | Manifest shape, command namespacing, hook events, script parity |
| `template/scripts/python/validate-routing.py` | Routing manifests against the routing principles |
| `scripts/test-routing-validator.sh` | That the routing verifier actually rejects a broken set — Principle XXV |
| `scripts/test-validator.sh` | That the extension validator actually rejects a broken package |
| `scripts/check-placeholders.sh` | No `CUSTOMIZE:` markers survive into a package |
| `scripts/install-test.sh` | The install → list → info → remove cycle |

All run in CI on every pull request.

## The sdd-master skill

[`.claude/skills/sdd-master/`](.claude/skills/sdd-master/) is a Claude Code skill,
inherited from the template, that decides how much process a piece of work
warrants and routes accordingly. It is how this repository is built, not part of
the shipped extension.

## Contributing

Work happens on feature branches and lands on `main` through a pull request; CI
must be green before merge. See the constitution's "Development Workflow & Quality
Gates" section for the full sequence.

## License

MIT — see [LICENSE](LICENSE).

Spec Kit is a project of GitHub, Inc. This extension is not affiliated with or
endorsed by GitHub, Inc.

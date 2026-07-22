<!--
SYNC IMPACT REPORT (v2.2.0)
Version change: 2.1.0 → 2.2.0
Rationale: MINOR — one principle added governing how the orchestrator uses a
knowledge graph (graphify) as a retrieval substrate for skill context. No
existing principle removed or redefined.

Added principles:
- XXIV. Knowledge Graph Retrieval Is Declared, Budgeted, and Non-Authoritative

Verified for this amendment:
- `graphify` resolves on PATH at /Users/jony/.local/bin/graphify (2026-07-22)
- Skill contract read from ~/.claude/skills/graphify/SKILL.md: builds into
  `graphify-out/`, exposes `query` / `path` / `explain`, supports `--update`
  incremental rebuild, `--watch` (no LLM), `--mcp` stdio server, and labels every
  edge EXTRACTED / INFERRED / AMBIGUOUS

Templates requiring updates:
- ✅ .specify/templates/plan-template.md (constitution-driven gate; no edit)
- ✅ .specify/templates/spec-template.md (no constitution-specific slots)
- ✅ .specify/templates/tasks-template.md (no constitution-specific slots)
- ✅ .specify/templates/checklist-template.md (no constitution-specific slots)
- ✅ .gitignore (now ignores `graphify-out/` per Principle XXIV)
- ⚠ docs/ROUTING.md (must document the `context.retrieval` manifest block)
- ⚠ docs/HARNESSES.md (each row must record whether graphify is available)
- ⚠ README.md / CHANGELOG.md (carried from v2.0.0 and v2.1.0)
- ✅ docs/HOOKS.md, docs/PACKAGING.md (unchanged; still accurate)

Follow-up TODOs:
- TODO(SKILL_CATALOG_VERIFICATION): carried unresolved — `speckit.baseline`
  remains unverified and ships no manifest.
- TODO(HARNESS_VERIFICATION): carried unresolved — all 20 named harness engines
  remain unverified.

--- PREVIOUS REPORT (v2.1.0) ---
Version change: 2.0.0 → 2.1.0
Rationale: MINOR — the source proposal was extended with three subjects v2.0.0 did
not govern: cross-feature (macro) parallelism over git worktrees, orchestration
telemetry persisted to a state file, and normalization of reasoning effort across
providers. Three principles added, one section materially expanded. No existing
principle removed or redefined.

Added principles:
- XXI. Macro-Parallelism Is Worktree-Isolated
- XXII. Orchestration State Is Auditable and Non-Authoritative
- XXIII. Reasoning Effort Is Normalized, Never Passed Through

Materially expanded sections:
- Harness Capability Matrix (now enumerates the five proposed harness categories
  and their named engines, every one marked unverified pending Principle XVI
  evidence)

Corrections carried from the source proposal into governance rather than code:
- The proposed guardrail check compared the user's balance against the skill's
  budget and fired when the balance was merely *lower than the ceiling*. Principle
  XVII already requires firing on projected consumption; XXII adds the
  reconciliation record that makes the distinction auditable.
- The proposed router dispatched via `subprocess.run(..., shell=True)` with an
  interpolated command string. Principle XXIII's dispatch rule forbids shell
  string interpolation in any reference implementation this project ships.

Templates requiring updates:
- ✅ .specify/templates/plan-template.md (constitution-driven gate; no edit)
- ✅ .specify/templates/spec-template.md (no constitution-specific slots)
- ✅ .specify/templates/tasks-template.md (no constitution-specific slots)
- ✅ .specify/templates/checklist-template.md (no constitution-specific slots)
- ⚠ README.md (still describes the template project; carried from v2.0.0)
- ⚠ CHANGELOG.md (needs a 2.0.0 and a 2.1.0 entry per Principle VIII)
- ⚠ docs/ROUTING.md (required by Principle XV; must now also document the
  telemetry schema required by Principle XXII and the effort ladder of XXIII)
- ⚠ docs/HARNESSES.md (required by Principle XVI; the 20 named engines start as
  unverified rows)
- ✅ docs/HOOKS.md, docs/PACKAGING.md (unchanged; still accurate)

Follow-up TODOs:
- TODO(SKILL_CATALOG_VERIFICATION): carried unresolved from v2.0.0 —
  `speckit.baseline` remains unverified and ships no manifest.
- TODO(HARNESS_VERIFICATION): all 20 named harness engines are unverified. Each
  becomes supported only when Principle XVI evidence is recorded.

--- PREVIOUS REPORT (v2.0.0) ---
Version change: 1.6.0 → 2.0.0
Rationale: MAJOR — the project identity is redefined. This repository is no longer
a generic "template for creating Spec Kit extensions"; it is the multi-agent
orchestration extension itself, which routes each Spec Kit skill to a configured
provider/model under declarative YAML, across harnesses. Principle XIV is
redefined (new repository URL and trunk), and the document title, preamble, and
Development Workflow are rewritten around the new scope. Six principles added.

Redefined:
- Document title and preamble: template project → multi-agent orchestration extension
- XIV. Trunk-Based Delivery Through Pull Requests (repository URL now
  https://github.com/jonyfs/spec-kit-extension-multi-agent-orchestration)

Added principles:
- XV. Declarative Routing Is the Only Control Surface
- XVI. Harness Agnosticism With a Declared Capability Floor
- XVII. Token Guardrails Fail Closed
- XVIII. Bounded Parallelism With Exclusive Artifact Ownership
- XIX. Model Identifiers Are Configuration, Never Defaults
- XX. Route Only Skills Proven to Exist

Added sections:
- Skill Routing Catalog
- Harness Capability Matrix

Retained unchanged: Principles I–XIII, Continuous Integration Gates, Installed
Extension Baseline, Vendored Third-Party Assets, Upstream Compatibility
Constraints, Governance. Principles I–XII continue to bind this extension, which
is itself a Spec Kit extension and therefore its own first consumer.

Templates requiring updates:
- ✅ .specify/templates/plan-template.md (constitution-driven gate; no edit)
- ✅ .specify/templates/spec-template.md (no constitution-specific slots)
- ✅ .specify/templates/tasks-template.md (no constitution-specific slots)
- ✅ .specify/templates/checklist-template.md (no constitution-specific slots)
- ⚠ README.md (still describes the template project; must be rewritten for the
  new scope before the first release)
- ⚠ CHANGELOG.md (needs a 2.0.0 entry per Principle VIII)
- ⚠ docs/ROUTING.md (does not exist yet; required by Principle XV)
- ⚠ docs/HARNESSES.md (does not exist yet; required by Principle XVI)
- ✅ docs/HOOKS.md, docs/PACKAGING.md (unchanged; still accurate)

Follow-up TODOs:
- TODO(SKILL_CATALOG_VERIFICATION): the source proposal lists ten skills including
  `speckit.baseline`, which is not present in the installed Spec Kit surface of
  this repository. Principle XX governs the resolution; the Skill Routing Catalog
  marks it unverified rather than asserting it.

--- PREVIOUS REPORT (v1.6.0) ---
Version change: 1.5.0 → 1.6.0
Rationale: MINOR — added one new principle (XIV. Trunk-Based Delivery Through
Pull Requests) and one new section (Continuous Integration Gates). No existing
principle removed or redefined.

Added principles:
- XIV. Trunk-Based Delivery Through Pull Requests

Added sections:
- Continuous Integration Gates

Repository state established this amendment:
- git initialized on `main`; remote https://github.com/jonyfs/spec-kit-extension-template (public)
- .github/workflows/ci.yml with four jobs: lint, validate, placeholders, install-test
- .github/pull_request_template.md carrying the per-principle checklist
- scripts/validate-extension.py, scripts/check-placeholders.sh, scripts/install-test.sh

Templates requiring updates:
- ✅ .specify/templates/plan-template.md (constitution-driven gate; no edit)
- ✅ .specify/templates/spec-template.md (no constitution-specific slots)
- ✅ .specify/templates/tasks-template.md (no constitution-specific slots)
- ✅ .specify/templates/checklist-template.md (no constitution-specific slots)
- ✅ README.md (created; documents the workflow and validation tooling)
- ✅ CHANGELOG.md (created; Keep a Changelog format per Principle VIII)
- ✅ LICENSE (created; MIT)
- ✅ docs/HOOKS.md, docs/PACKAGING.md (unchanged; still accurate)

Resolved from v1.0.0: README.md, CHANGELOG.md, and LICENSE now exist.
Follow-up TODOs: none deferred.

--- PREVIOUS REPORT (v1.5.0) ---
Version change: 1.4.0 → 1.5.0
Rationale: MINOR — added one new principle (XIII. Proactive Use of Installed
Extensions) and one new section (Installed Extension Baseline). No existing
principle removed or redefined.

Added principles:
- XIII. Proactive Use of Installed Extensions

Added sections:
- Installed Extension Baseline

Installed this amendment (all via `specify extension add --from`, source "local"):
- worktrees 1.3.2, ship 1.0.0, critique 1.0.0, staff-review 1.0.0,
  speckit-superpowers-bridge 1.1.0, onboard 2.1.0

Templates requiring updates:
- ✅ .specify/templates/plan-template.md (constitution-driven gate; no edit)
- ✅ .specify/templates/spec-template.md (no constitution-specific slots)
- ✅ .specify/templates/tasks-template.md (no constitution-specific slots)
- ✅ .specify/templates/checklist-template.md (no constitution-specific slots)
- ✅ docs/HOOKS.md, docs/PACKAGING.md (unchanged; still accurate)
- ⚠ README.md / CHANGELOG.md / LICENSE still pending from v1.0.0
- ⚠ Six hooks are registered `optional: false` (auto-executing) by worktrees and
  speckit-superpowers-bridge — accepted as third-party behavior, see Principle
  XIII; Principle IV continues to bind extensions THIS project authors.

Follow-up TODOs: none deferred.

--- PREVIOUS REPORT (v1.4.0) ---
Version change: 1.3.0 → 1.4.0
Rationale: MINOR — added one new principle (XII. Every Distribution Form,
Verified). No existing principle removed or redefined; Principle VII's install
gate is extended by reference, not redefined.

Added principles:
- XII. Every Distribution Form, Verified

Added artifacts:
- docs/PACKAGING.md (the maintained distribution matrix required by Principle XII)

Templates requiring updates:
- ✅ .specify/templates/plan-template.md (constitution-driven gate; no edit)
- ✅ .specify/templates/spec-template.md (no constitution-specific slots)
- ✅ .specify/templates/tasks-template.md (no constitution-specific slots)
- ✅ .specify/templates/checklist-template.md (no constitution-specific slots)
- ✅ docs/PACKAGING.md (created; verified against specify-cli 0.11.3)
- ✅ docs/HOOKS.md (unchanged; still accurate)
- ⚠ README.md / CHANGELOG.md / LICENSE still pending from v1.0.0

Follow-up TODOs: none deferred.

--- PREVIOUS REPORT (v1.3.0) ---
Version change: 1.2.0 → 1.3.0
Rationale: MINOR — added one new principle (XI. Hook Literacy Across Harnesses)
and materially expanded the hook guidance already present in Principle IV by
reference. No existing principle removed or redefined.

Added principles:
- XI. Hook Literacy Across Harnesses

Added artifacts:
- docs/HOOKS.md (the maintained hook matrix required by Principle XI)

Templates requiring updates:
- ✅ .specify/templates/plan-template.md (constitution-driven gate; no edit)
- ✅ .specify/templates/spec-template.md (no constitution-specific slots)
- ✅ .specify/templates/tasks-template.md (no constitution-specific slots)
- ✅ .specify/templates/checklist-template.md (no constitution-specific slots)
- ✅ docs/HOOKS.md (created; documents both hook layers)
- ⚠ README.md / CHANGELOG.md / LICENSE still pending from v1.0.0

Follow-up TODOs: none deferred.

--- PREVIOUS REPORT (v1.2.0) ---
Version change: 1.1.0 → 1.2.0
Rationale: MINOR — added one new principle (X. Compressed Communication,
Uncompressed Artifacts) and one new governance-adjacent section (Vendored
Third-Party Assets). No existing principle removed or redefined.

Added principles:
- X. Compressed Communication, Uncompressed Artifacts

Added sections:
- Vendored Third-Party Assets

Templates requiring updates:
- ✅ .specify/templates/plan-template.md (constitution-driven gate; no edit)
- ✅ .specify/templates/spec-template.md (no constitution-specific slots)
- ✅ .specify/templates/tasks-template.md (no constitution-specific slots)
- ✅ .specify/templates/checklist-template.md (no constitution-specific slots)
- ✅ .claude/skills/caveman/ (vendored from juliusbrussee/caveman @ 0d95a81,
  MIT, with PROVENANCE.md — compliant with the new section)
- ⚠ README.md / CHANGELOG.md / LICENSE still pending from v1.0.0

Follow-up TODOs: none deferred.

--- PREVIOUS REPORT (v1.1.0) ---
Version change: 1.0.0 → 1.1.0
Rationale: MINOR — added one new principle (IX. English Artifacts, Native
Conversation). No existing principle removed or redefined.

Added principles:
- IX. English Artifacts, Native Conversation

Templates requiring updates:
- ✅ .specify/templates/plan-template.md (constitution-driven gate; no edit)
- ✅ .specify/templates/spec-template.md (no constitution-specific slots)
- ✅ .specify/templates/tasks-template.md (no constitution-specific slots)
- ✅ .specify/templates/checklist-template.md (no constitution-specific slots)
- ⚠ README.md / CHANGELOG.md / LICENSE still pending from v1.0.0

Follow-up TODOs: none deferred.

--- PREVIOUS REPORT (v1.0.0) ---
Version change: (unversioned template) → 1.0.0
Rationale: First ratification. All placeholder tokens replaced with concrete,
testable governance for a Spec Kit extension template project.

Modified principles:
- [PRINCIPLE_1_NAME] → I. Manifest Is the Contract
- [PRINCIPLE_2_NAME] → II. Namespaced Commands (NON-NEGOTIABLE)
- [PRINCIPLE_3_NAME] → III. Template Placeholders Must Be Obvious
- [PRINCIPLE_4_NAME] → IV. Hooks Are Opt-In by Default
- [PRINCIPLE_5_NAME] → V. Cross-Platform Script Parity
- (added) VI. Additive, Non-Destructive Project Changes
- (added) VII. Install-Test Before Publish
- (added) VIII. Semantic Versioning & Changelog

Added sections:
- Upstream Compatibility Constraints (replaces [SECTION_2_NAME])
- Development Workflow & Quality Gates (replaces [SECTION_3_NAME])

Removed sections: none

Templates requiring updates:
- ✅ .specify/templates/plan-template.md (Constitution Check gate is
  constitution-driven and generic; no edit required)
- ✅ .specify/templates/spec-template.md (no constitution-specific slots)
- ✅ .specify/templates/tasks-template.md (no constitution-specific slots)
- ✅ .specify/templates/checklist-template.md (no constitution-specific slots)
- ✅ .specify/extensions/agent-context/* (already compliant with I, II, IV, V)
- ⚠ README.md (does not exist yet; must be created per Principle VII)
- ⚠ CHANGELOG.md (does not exist yet; must be created per Principle VIII)
- ⚠ LICENSE (does not exist yet; required for publishing per Principle VII)

Follow-up TODOs: none deferred.
-->

# Spec Kit Multi-Agent Orchestration Extension Constitution

This project is a **GitHub Spec Kit extension that orchestrates multiple agents
across the spec-driven development lifecycle**. It does not add a new workflow; it
governs how the existing Spec Kit skills execute. For each skill it declares — in
YAML, outside any command prose — which provider and model handle it, at what
reasoning effort, under what token budget, with what parallelism, and how its
output is rendered. The same declarations MUST produce the same routing decisions
on every supported execution harness, from a local coding agent to an ephemeral
CI runner.

It is itself an extension package installed via `specify extension add`, so
Principles I through XIII bind it as strictly as they bind anything generated from
its ancestor template. Upstream reference: `github/spec-kit`, directory
`extensions/` (`EXTENSION-API-REFERENCE.md`, `EXTENSION-DEVELOPMENT-GUIDE.md`,
`EXTENSION-PUBLISHING-GUIDE.md`).

## Core Principles

### I. Manifest Is the Contract

Every extension produced from this template MUST ship a valid `extension.yml` with
`schema_version: "1.0"` and complete `extension` metadata (`id`, `name`, `version`,
`description`, `author`, `repository`, `license`). `extension.id` MUST match
`^[a-z0-9-]+$`. `requires.speckit_version` MUST be a version specifier with no
spaces (for example `>=0.2.0` or `>=0.2.0,<2.0.0`) — never a bare version, never
`latest`. Every file referenced by `provides.commands[].file`,
`provides.config[].template`, and any script path MUST exist in the package.

Rationale: The manifest is what the CLI validates, hashes into `.registry`, and uses
to register commands. A manifest that lies about its files fails at install time on
the user's machine, not ours.

### II. Namespaced Commands (NON-NEGOTIABLE)

Every command name and alias MUST match `^speckit\.[a-z0-9-]+\.[a-z0-9-]+$` and the
middle segment MUST equal `extension.id`. Commands MUST NOT shadow a core Spec Kit
command (`speckit.specify`, `speckit.plan`, `speckit.tasks`, `speckit.implement`,
`speckit.analyze`, `speckit.clarify`, `speckit.checklist`, `speckit.constitution`)
nor a command already registered by another extension.

Rationale: Command registration is a flat namespace across every installed
extension. Collisions silently overwrite a user's working workflow.

### III. Template Placeholders Must Be Obvious

Every value an author is expected to change MUST be marked in place with a
`# CUSTOMIZE:` comment (or `# REVIEW:` where the default is usually acceptable), and
MUST use an unmistakable placeholder value (`my-extension`, `Your Name`,
`https://github.com/your-org/...`). No template file may ship a plausible-looking
real value that an author could leave in by accident. A generated extension MUST NOT
be publishable until every `CUSTOMIZE` marker is resolved.

Rationale: The single biggest failure mode of a template is shipping the template's
own identity to a registry. Placeholders that look wrong get fixed.

### IV. Hooks Are Opt-In by Default

Hooks declared under `hooks:` MUST default to `optional: true` and MUST supply a
`prompt` and a `description`. `optional: false` (auto-execute) is permitted ONLY for
read-only hooks or hooks whose writes are confined to files the extension itself
owns, and the justification MUST be recorded in the extension README. Where an event
carries multiple hooks, each entry MUST declare an explicit integer `priority` (≥ 1,
lower runs first) rather than relying on the default of 10. Hook `condition`
expressions MUST NOT be evaluated by command prose — condition handling belongs to
the HookExecutor.

Rationale: A hook fires inside someone else's project on someone else's branch.
Silent, mandatory side effects are how extensions get uninstalled.

### V. Cross-Platform Script Parity

If an extension provides scripts, it MUST provide behaviorally equivalent `bash`
(`scripts/bash/*.sh`) and `powershell` (`scripts/powershell/*.ps1`) implementations,
and command frontmatter MUST reference both via `scripts.sh` and `scripts.ps`. Adding
a `scripts/python/` variant is permitted but never a substitute for the other two.
Shipping one platform only is a release blocker.

Rationale: Spec Kit resolves the script variant from the host platform. A missing
variant makes the extension simply not work for half of its users.

### VI. Additive, Non-Destructive Project Changes

An extension MUST confine its writes to `.specify/extensions/{extension-id}/`, to
files it created, and to explicitly delimited managed regions (marker-fenced blocks)
inside shared files such as agent context files. It MUST NOT rewrite or reorder
content outside its markers, MUST NOT delete user content, and MUST NOT commit,
push, or otherwise alter git history unless that is the extension's stated purpose
and the user invoked it directly.

Rationale: Extensions run against real repositories with uncommitted work. Anything
outside a managed region belongs to the user.

### VII. Install-Test Before Publish

No extension may be tagged for release until it has been installed into a real Spec
Kit project via `specify extension add --dev <path>`, appeared correctly under
`specify extension list`, had **every** declared command and hook executed at least
once, and been cleanly removed. The package MUST additionally contain a `README.md`
with install and usage instructions, and a `LICENSE` file.

Rationale: Manifest validation proves the YAML parses. Only an install-run-remove
cycle proves the extension works.

### VIII. Semantic Versioning & Changelog

`extension.version` MUST follow `X.Y.Z` with no prefix and no pre-release suffix.
MAJOR for a removed or renamed command/alias, a removed hook event, or a raised
`requires.speckit_version` floor; MINOR for a new command, hook, or config key;
PATCH for prose, fixes, and non-behavioral changes. Every version bump MUST land a
matching `CHANGELOG.md` entry in the same change, and the GitHub release tag MUST be
`v{version}`.

Rationale: `.specify/extensions/.registry` pins installed versions and hashes.
Users upgrade based on what the version number promises.

### IX. English Artifacts, Native Conversation

Everything written to disk MUST be in English: `extension.yml`, command Markdown,
scripts and their comments, config templates, `README.md`, `CHANGELOG.md`,
`LICENSE`, specs, plans, tasks, this constitution, commit messages, pull request
titles and bodies, and code identifiers. Interactive conversation MUST use the
language the requester used in their message; switching the conversation language
never changes the language of a file.

Rationale: The audience for a published Spec Kit extension is the upstream catalog
and its global users, so artifacts must be readable by everyone. The audience for a
conversation is one person, so it should be in their language.

### X. Compressed Communication, Uncompressed Artifacts

Interactive conversation in this project uses the compressed style defined by the
vendored `caveman` skill (`.claude/skills/caveman/SKILL.md`), default intensity
`full`. Compression applies to prose addressed to a human and to nothing else.
Artifacts MUST be written in full, conventional prose: command Markdown, `README.md`,
`CHANGELOG.md`, config templates, script comments, specs, plans, tasks, commit
messages, and pull request bodies. Compression MUST also be dropped mid-conversation
for security warnings, irreversible-action confirmations, and any sequence where
omitted articles or conjunctions could reverse the meaning of an ordered step.

Rationale: Terse prose saves tokens for the one person reading the conversation.
A published extension is read by strangers, parsed by tooling, and reviewed years
later — it gets no such benefit and pays a real comprehension cost. Principle IX
governs which language artifacts use; this principle governs their register.

### XI. Hook Literacy Across Harnesses

Two distinct hook layers exist and MUST never be conflated: **Spec Kit lifecycle
hooks**, declared in `extension.yml` and aggregated into `.specify/extensions.yml`,
which invoke slash commands as agent prompts; and **harness hooks**, declared in a
harness's own configuration (for example `.claude/settings.json`,
`.codex/hooks.json`), which execute real shell processes and can block tool calls.

This project MUST maintain `docs/HOOKS.md` as an evidence-backed matrix of both
layers, recording for every documented harness: the config file path, the event
names, the payload contract, the exit-code and blocking semantics, and the matcher
syntax. An entry MAY be added only after being read from that harness's current
documentation or verified against a real config; recalled-from-memory contracts are
forbidden, and an unverified harness MUST be listed explicitly as unverified rather
than omitted or guessed.

An extension MUST NOT install, modify, or remove a harness hook without the user
explicitly requesting that specific change; suggesting a snippet the user installs
themselves is the supported path. Any harness hook this project authors or
recommends MUST declare an explicit timeout, quote all interpolated paths, use
project-local tooling rather than remote one-off package execution, exit zero when
not applicable, and confine its writes to paths the extension owns. Blocking hooks
MUST additionally document their exact failure mode in the extension README.

Rationale: Layer 1 is a suggestion the agent may act on; Layer 2 is code running on
someone's machine with their credentials, able to veto their tools. Treating the two
as interchangeable produces either hooks that never fire or hooks that break a user's
session in a way they cannot trace back to the extension.

### XII. Every Distribution Form, Verified

The `specify` CLI can install an extension in four distinct forms: a local directory
(`extension add --dev <path>`), a custom URL (`extension add <id> --from <url>`), a
catalog entry resolving to a downloadable ZIP, and bundling inside the CLI package
itself. This project MUST maintain `docs/PACKAGING.md` documenting all of them,
recording for each: the exact command and its options, the required package layout,
the resulting `.registry` `source` value, and the resulting on-disk project state.

The matrix MUST be evidence-backed and MUST name the `specify` version it was
verified against. Every entry MUST come from the CLI's own `--help` output, its
source, or an executed command — never from recall. Every CLI upgrade obliges a
re-verification pass, and any form that could not be re-verified MUST be marked as
unverified rather than silently carried forward.

An extension MUST be installable in every form it claims to support, and a release
MUST be proven in the **published** artifact, not only the working tree: the built
ZIP MUST be installed into a clean project via its release URL before the catalog
entry is submitted or updated. Any distribution form the extension does not support
MUST be stated as unsupported in its README.

Rationale: `--dev` succeeding proves the working tree is valid. It does not prove the
ZIP has the manifest at the right depth, that the release asset URL resolves, or that
the catalog entry's `download_url` points anywhere real — and those are the only
paths a stranger will ever use.

### XIII. Proactive Use of Installed Extensions

The extensions listed under "Installed Extension Baseline" are part of this
project's working method, not optional decoration. When a task matches a listed
trigger, the corresponding command MUST be offered or invoked without waiting for
the user to name it — an installed capability that goes unused is indistinguishable
from an uninstalled one.

Proactive invocation is bounded by three rules. First, read-only commands
(`critique`, `staff-review`, `onboard.*`) MAY be invoked directly; commands that
write outside their own directory, create branches, push, or open pull requests
(`ship.run`, `worktrees.create`, `worktrees.clean`) MUST be proposed and confirmed
before running. Second, an extension MUST NOT be invoked when its precondition is
absent — `worktrees.*` requires a git repository, `ship.run` requires a remote and a
clean tree — and the missing precondition MUST be stated rather than worked around.
Third, an extension's failure MUST NOT be silently absorbed: report what failed and
continue, never present a skipped step as completed.

Adding or removing an entry from the baseline is a constitution amendment. Third-
party extensions in the baseline are governed by their own authors, so their hooks
MAY be registered `optional: false`; Principle IV binds extensions **this project
authors**, and the divergence MUST be recorded in the baseline table rather than
silently tolerated.

Rationale: Installing seven extensions and then never routing work to them is worse
than not installing them — it adds surface area, hook noise, and supply-chain
exposure with no return.

### XIV. Trunk-Based Delivery Through Pull Requests

This project lives at
`https://github.com/jonyfs/spec-kit-extension-multi-agent-orchestration`. It was
seeded from `jonyfs/spec-kit-extension-template`, which remains configured as the
`upstream` remote; upstream changes are merged into a branch and land through a
pull request like any other change, never pushed straight to trunk.
`main` is the trunk and is never committed to directly. Every change — feature,
fix, or documentation — lands through a pull request that targets `main` from a
short-lived branch, and every pull request MUST have all CI gates green before
merge. A branch whose CI is red is not ready for review.

When an implementation completes successfully, opening the pull request is part of
finishing the work, not a separate optional step. The installed `ship` extension
(`speckit.ship.run`, offered by the `after_implement` hook) is the supported path:
it runs pre-flight readiness checks, syncs the branch, generates the changelog
entry, verifies CI, and creates the PR. Its confirmations default to **no** by
design — a push and a PR creation are each authorized separately, and that
default MUST NOT be worked around.

A pull request MUST state what changed and why, link the Spec Kit artifacts it
implements when the work was spec-driven, and carry the constitution checklist from
`.github/pull_request_template.md` with every applicable row honestly checked. A
checkbox ticked without the corresponding check having been run is a false
statement about the change, and is worse than an unchecked box.

Rationale: The gates only mean something if they run before the code is trunk, and
a PR is the only artifact where a human, the CI, and the review extensions all look
at the same diff at the same time.

### XV. Declarative Routing Is the Only Control Surface

Every routing decision — provider, model, reasoning effort, token budget,
parallelism, context injection, output artifact path, and log color — MUST be
expressed in a YAML manifest under this extension's own configuration directory,
one file per skill, named `skill-{skill}.yml`. Command Markdown, scripts, and
harness configuration MUST read those values and MUST NOT restate, override, or
hardcode them. A routing change that requires editing anything other than a YAML
manifest is a defect in the design, not a change to be merged.

Each manifest MUST carry `schema_version`, the skill it routes, and explicit
values for every governed field; there are no implicit fallbacks. Unknown keys and
missing required keys are both validation failures. Values that vary by
environment (API keys, endpoints, organization identifiers) MUST be referenced as
environment variable names, never as literals — Principle VI's secrets rule applies
unchanged. This extension MUST ship a schema and a validator for these manifests,
run as a CI gate, and MUST document every field in `docs/ROUTING.md`.

Rationale: The whole value of the extension is that an organization can change
which model performs planning without reading a single line of prose. The moment
one routing fact lives in a command file, the manifests stop being authoritative
and every reader has to check two places to know what will actually run.

### XVI. Harness Agnosticism With a Declared Capability Floor

No skill's routing behavior may depend on which harness executes it. The manifests
are the input; the harness supplies only process, environment, and I/O. This
extension MUST NOT require a harness-specific feature in order to function, and
MUST NOT write to a harness's own configuration (see Principle XI).

Harnesses differ in what they can honor — an ephemeral CI runner cannot prompt a
human, a plain build console may not render 24-bit color, a hosted agent may not
expose a local filesystem. This project MUST therefore maintain `docs/HARNESSES.md`
as an evidence-backed matrix recording, for every supported harness: how manifest
values reach the process, whether interactive confirmation is available, the color
depth supported, and the concurrency model. Where a capability is absent, the
behavior MUST degrade to a documented, deterministic fallback — never to silence.
Colors in particular MUST be declared as both a hex value and an ANSI code so a
harness can pick what it can render, and a harness with no color support MUST still
emit the skill name in plain text.

An entry MAY be added only after being verified against that harness's current
documentation or a real executed run. Unverified harnesses MUST be listed as
unverified rather than omitted or assumed.

Rationale: "Runs anywhere" is a claim that decays silently. A matrix with a
verification date turns portability from a marketing sentence into something a
reviewer can check.

### XVII. Token Guardrails Fail Closed

Every skill manifest MUST declare a token budget and the action taken when the
budget is exhausted. The permitted actions are exactly: `halt` (stop before
exceeding the budget), `checkpoint_and_halt` (persist recoverable state, then
stop), and `truncate_context` (drop the lowest-priority context and continue).
`truncate_context` is permitted ONLY for read-only analysis skills, and the
manifest MUST declare the truncation priority order; a skill that writes artifacts
MUST NOT silently continue on a truncated context.

Budget accounting MUST cover every agent a skill spawns, not only the primary
call, and MUST be checked before dispatching additional work rather than after
spending it. A missing, unparseable, or non-positive budget MUST abort the skill —
never default to unlimited. Whenever a guardrail fires, the extension MUST report
the skill, the budget, the consumed amount, and the action taken; a budget event
MUST NOT be reported as a normal completion.

Rationale: Orchestration multiplies spend by the number of agents. The one failure
mode a user cannot recover from is discovering the ceiling on an invoice, so the
safe direction on any ambiguity is to stop.

### XVIII. Bounded Parallelism With Exclusive Artifact Ownership

Concurrency MUST be bounded by an explicit `max_concurrent_agents` in the manifest;
unbounded fan-out is forbidden. Two concurrent agents MUST NOT be able to write the
same file: every parallel unit of work MUST own its output path exclusively, and
merging their results is the orchestrator's job, performed after the units
complete. Shared state between concurrent agents MUST be append-only or absent.

Parallel execution MUST be deterministic in its outcome: the final artifact set
MUST NOT depend on which agent finished first. An agent's failure MUST NOT be
absorbed by its siblings' success — a partially failed wave is reported as
partially failed, with the failed unit named, and MUST NOT advance the workflow to
the next skill as though it had completed.

Rationale: Parallelism buys wall-clock time and pays for it in nondeterminism.
Exclusive ownership is what keeps the second cost from arriving as corrupted
artifacts nobody can reproduce.

### XIX. Model Identifiers Are Configuration, Never Defaults

Provider and model identifiers are volatile: models are renamed, deprecated, and
superseded on the provider's schedule, not this project's. This extension MUST NOT
hardcode a model identifier anywhere in code, command prose, or documentation
examples presented as recommended values. Shipped manifests MUST use placeholder
identifiers marked per Principle III's `# CUSTOMIZE:` convention, and MUST resolve
the real identifier from the user's configuration or environment.

Any model identifier that does appear — in a test fixture, a README example, or the
routing catalog — MUST be verified against the provider's current documentation and
MUST carry the date it was verified. This extension MUST fail with a clear,
actionable error when a configured model is unavailable to the caller, and MUST NOT
silently substitute a different model: a substitution changes cost, capability, and
output quality without the user's knowledge.

Rationale: A template that ships a model name from the year it was written sends
every future user to a deprecated endpoint. Verified-with-a-date is the only
honest way to publish a value that expires.

### XX. Route Only Skills Proven to Exist

A routing manifest MAY be shipped only for a skill that actually exists in the
Spec Kit surface this extension targets, verified against upstream's command set or
an installed extension's manifest — never from recall or from a design document.
The Skill Routing Catalog below records each routed skill, the artifact it owns,
and the evidence for its existence.

A skill named in a proposal but not found MUST be recorded as unverified and MUST
NOT ship a manifest until confirmed. If a skill is provided by an extension rather
than by core Spec Kit, the catalog MUST name that extension, and this extension
MUST tolerate its absence: a manifest for a skill that is not installed is inert,
never an error, and MUST NOT block the skills that are installed.

Rationale: Routing configuration for a command nobody can invoke is dead weight
that reads as a supported feature. Worse, it teaches users a workflow step that
does not exist.

### XXI. Macro-Parallelism Is Worktree-Isolated

Principle XVIII governs concurrency *inside* one skill. This principle governs
concurrency *across* features. Two features MUST NOT be orchestrated concurrently
in the same working directory: each concurrent feature pipeline MUST own a
distinct git worktree with a distinct branch, created through the installed
`worktrees` extension under the confirmation rules of Principle XIII.

Macro-parallelism is permitted only where the harness provides real filesystem
isolation. A harness that shares one checkout across concurrent jobs MUST fall
back to serial execution rather than interleaving features in one tree, and the
fallback MUST be recorded in `docs/HARNESSES.md`. Where a harness has no git
available at all, feature-level concurrency MUST be refused, not simulated.

Concurrency here is bounded by the same accounting as everything else: the token
budget of Principle XVII is enforced across every concurrently running feature,
not per feature. Five pipelines do not get five budgets. A pipeline that fails
MUST NOT abort its siblings, MUST NOT be reported as skipped, and MUST leave its
worktree intact for inspection rather than being cleaned up automatically.

Rationale: Running features in parallel is the whole point of the extension, and
a shared checkout turns that into two agents editing each other's files. The
worktree is what makes the parallelism real instead of a race.

### XXII. Orchestration State Is Auditable and Non-Authoritative

The orchestrator MUST persist its state — the active skill, the harness it is
running under, the extension version, the skills already completed, the token
budget with the amount consumed and remaining, and the currently executing agents
with the task each owns — to a machine-readable file under this extension's own
directory. Its schema MUST be versioned and documented in `docs/ROUTING.md`, and
it MUST be updated when a wave starts, when a wave ends, and whenever a guardrail
fires.

That file is a record, never a source of truth. The orchestrator MUST NOT resume,
skip a skill, or authorize spending on the basis of state it cannot re-derive
from the repository and the provider's own usage reporting; a stale or corrupt
state file MUST cause a re-derivation, never a silent continuation. Token counts
in it MUST be reconciled against provider-reported usage rather than estimated,
and any divergence MUST be surfaced, because an under-counted estimate is how a
budget gets exceeded while the record still claims headroom.

The file MUST NOT contain credentials, prompt bodies, or source content — it
carries identifiers, counts, and status only — and it MUST be written atomically,
since concurrent waves update it.

Rationale: Multi-agent orchestration is opaque while it runs and unreproducible
afterwards unless something wrote down what happened. Making that record
non-authoritative is what stops a corrupted file from becoming a corrupted run.

### XXIII. Reasoning Effort Is Normalized, Never Passed Through

Manifests declare reasoning effort on one closed ladder — `low`, `medium`, `high`,
`max` — and the extension MUST translate that ladder into whatever each provider
actually accepts. Provider-native effort parameters, thinking-token budgets, and
their environment variable names MUST NOT appear in a manifest; a manifest that
names a provider-specific knob is a validation failure under Principle XV.

Every mapping from a ladder rung to a provider parameter MUST live in one
documented table in `docs/ROUTING.md`, MUST be verified against that provider's
current documentation with a recorded date per Principle XIX, and MUST degrade
explicitly: where a provider offers no equivalent, the mapping MUST state that the
rung is a no-op rather than inventing a substitute. Providers that expose no
effort control at all MUST still be routable.

Any reference implementation this project ships MUST pass configuration to a
subprocess as an argument list with the environment supplied explicitly. Building
a command string and executing it through a shell is forbidden: manifest values
are attacker-influenced input the moment a manifest is shared, and shell
interpolation turns a routing file into arbitrary code execution on a runner
holding the organization's API keys.

Rationale: Provider effort controls are the least stable part of any model API.
Normalizing them is what keeps a manifest written today from being wrong next
quarter, and keeps a routing change from becoming a code change.

### XXIV. Knowledge Graph Retrieval Is Declared, Budgeted, and Non-Authoritative

A knowledge graph built by `graphify` over the repository is this extension's
supported retrieval substrate: instead of feeding a skill whole directories, the
orchestrator queries the graph and injects the answer. Which skills retrieve, and
how much, is a routing decision and therefore belongs in the manifest — a
`context.retrieval` block declaring whether retrieval is enabled, the query
budget, and the traversal mode. Command prose MUST NOT decide to retrieve on its
own, per Principle XV.

**Optional, never required.** Graphify is an external tool that may be absent, and
its absence MUST degrade to the skill's declared non-graph context path with a
recorded notice — never an error, never a silent context gap, never a skill that
appears to have read the repository when it did not. Harness rows in
`docs/HARNESSES.md` MUST record graphify availability, since a CI runner will
usually not have it.

**Budgeted like everything else.** Building or refreshing a graph consumes model
tokens and MUST be accounted against Principle XVII's budget for the skill that
triggered it. A build MUST NOT be started inside a parallel wave: the graph is
shared read-only state, so it MUST be built or refreshed — with `--update` where
a graph already exists — before agents are dispatched, and MUST be treated as
immutable for the duration of that wave. Two agents MUST NOT rebuild it
concurrently, and its output directory belongs to graphify alone, is ignored by
git, and is never an artifact any skill owns under Principle XVIII.

**Non-authoritative, with provenance intact.** Graphify labels every edge
`EXTRACTED`, `INFERRED`, or `AMBIGUOUS`. That label MUST survive into anything the
orchestrator writes: an `INFERRED` or `AMBIGUOUS` relationship MUST NOT be stated
as fact in a spec, plan, task, or review, and any claim a skill takes from the
graph and then asserts about the code MUST be confirmed against the file itself
before it lands in an artifact. A stale graph is a normal condition, not a
failure — the repository is the source of truth and the graph is an index over it,
exactly as Principle XXII treats orchestration state.

Rationale: The dominant cost in multi-agent orchestration is shipping the same
context to every agent. A graph makes retrieval cheap enough that parallelism pays
off — but an index that is trusted like a source turns a confident inference into
a specification, and nobody reviewing the spec can see where the claim came from.

## Skill Routing Catalog

The skills this extension routes. `Verified` records how the skill's existence was
confirmed; `Owns` is the artifact the skill writes, which under Principle XVIII no
other concurrent unit may write.

| Skill | Owns | Source | Verified |
|---|---|---|---|
| `speckit.constitution` | `.specify/memory/constitution.md` | core | installed command |
| `speckit.specify` | feature `spec.md` | core | installed command |
| `speckit.clarify` | feature `spec.md` (in place) | core | installed command |
| `speckit.plan` | feature `plan.md` | core | installed command |
| `speckit.checklist` | `checklists/requirements.md` | core | installed command |
| `speckit.tasks` | feature `tasks.md` | core | installed command |
| `speckit.analyze` | nothing (read-only) | core | installed command |
| `speckit.implement` | source tree and tests | core | installed command |
| `speckit.converge` | feature `tasks.md` (append) | core | installed command |
| `speckit.baseline` | — | unknown | TODO(SKILL_CATALOG_VERIFICATION): named in the source proposal, not found in this project's installed command set; no manifest until confirmed |

Adding a row is a MINOR amendment; removing one is MAJOR, because a removed row
means a shipped manifest stops being honored.

## Harness Capability Matrix

`docs/HARNESSES.md` is the maintained artifact required by Principle XVI. It MUST
cover at minimum these categories, and MUST state for each named harness whether it
has been verified or not:

Each row MUST additionally record whether `graphify` is available in that harness,
per Principle XXIV; where it is not, the declared non-graph context path applies.

| Category | Named engines | How manifest values reach the run | Log rendering | Status |
|---|---|---|---|---|
| Traditional CI/CD | GitHub Actions, GitLab CI, CircleCI, Travis CI, Azure Pipelines | Step-level environment injection into an ephemeral runner | ANSI escapes in the build console | unverified |
| Cloud-native orchestrators | Argo Workflows, Tekton, Kubernetes Jobs, Apache Airflow, Temporal | Pod/worker environment plus a mounted volume per worktree | Hex value consumed by a web dashboard | unverified |
| Enterprise clouds | AWS CodePipeline, Google Cloud Build, Jenkins | A container image carrying the extension, configured by environment | Structured JSON on stdout | unverified |
| IDE and dev environments | GitHub Codespaces, local Docker Compose, Nomad | Shared local filesystem, environment from the container | ANSI in the integrated terminal | unverified |
| Terminal AI agents | Claude Code CLI, GitHub Copilot CLI, Cursor, local routers | Read directly from the working tree by the resident agent | ANSI streamed as tokens arrive | unverified |

Every row above is `unverified` and MUST remain so until Principle XVI evidence —
a real executed run or that harness's current documentation — is recorded in
`docs/HARNESSES.md` with a date. Counting engines is not the same as supporting
them; the README MUST NOT claim a harness this table has not verified.

Two constraints cut across the categories. Filesystem isolation determines whether
Principle XXI's macro-parallelism is available at all, so each row MUST record
whether the harness gives each concurrent job its own checkout. And log rendering
degrades in a fixed order — 24-bit hex where available, then the declared ANSI
code, then plain text — never to no output.

Interactive confirmation is unavailable in non-interactive harnesses. Any skill
whose manifest requests confirmation MUST, in such a harness, take the declared
non-interactive fallback — which for a write, a push, or a pull request MUST be to
refuse, matching Principle XIV's confirm-by-default posture. An unverified harness
MUST NOT be listed as supported in the README.

## Continuous Integration Gates

CI is defined in `.github/workflows/ci.yml` and runs on every push to `main`, every
pull request targeting `main`, and on manual dispatch. Four jobs, each mechanizing a
principle that is otherwise only aspirational:

| Job | Enforces | Implementation |
|---|---|---|
| Lint Markdown and YAML | Readability of hand-authored files | `yamllint`, `markdownlint-cli2` |
| Validate extension manifests | Principles I, II, IV, V, VIII | `scripts/validate-extension.py` |
| Guard template placeholders | Principle III | `scripts/check-placeholders.sh` |
| Install-test cycle | Principle VII | `scripts/install-test.sh` |
| Validate routing manifests | Principles XV, XVII, XVIII, XIX, XX, XXIII, XXIV | routing-manifest schema validator (⚠ to be added) |
| Validate orchestration state | Principle XXII | state-file schema validator (⚠ to be added) |

Two scoping rules keep the gates honest. Vendored third-party extensions under
`.specify/extensions/` are excluded from every job: they belong to their upstream
authors, and this repository does not get to fail its own build over someone else's
manifest. Machine-generated state under `.specify/` is likewise excluded from
linting, because a file the `specify` CLI rewrites on every install cannot be held
to this project's formatting.

A gate MUST NOT be weakened to make a red build green. Either the change is wrong,
or the gate's scope is wrong — and if it is the gate, the scope change is itself a
reviewable pull request explaining why, not a quiet edit bundled into unrelated work.

## Installed Extension Baseline

Verified with `specify extension list` against specify-cli 0.11.3. All six
third-party entries were installed via `specify extension add --from <release-zip>`
and are recorded in `.specify/extensions/.registry` with `"source": "local"`.

| Extension | Version | Use it when | Effect |
|---|---|---|---|
| `agent-context` (bundled) | 1.0.0 | After spec or plan changes, to refresh the agent context file | read-write, own markers |
| `critique` | 1.0.0 | A spec and plan exist and implementation has not started | read-only |
| `staff-review` | 1.0.0 | Implementation changes exist and need review against the spec | read-only |
| `onboard` | 2.1.0 | Someone needs a feature, dependency map, or SDD concept explained | read-only |
| `worktrees` | 1.3.2 | Parallel feature work needs isolation; **requires a git repository** | read-write, creates worktrees |
| `ship` | 1.0.0 | A feature is implemented and reviewed and is ready to release | read-write, branches/CI/PR |
| `speckit-superpowers-bridge` | 1.1.0 | Handing a `tasks.md` from Spec Kit design to Superpowers implementation | read-write, handoff state |

### Auto-executing hooks in this baseline

Six hooks are registered `optional: false` and run without prompting:

| Extension | Command | Event |
|---|---|---|
| `worktrees` | `speckit.worktrees.create` | `after_specify` |
| `speckit-superpowers-bridge` | `...bridge.guard` | four command events |
| `speckit-superpowers-bridge` | `...bridge.handoff` | one command event |

`worktrees.create` firing on `after_specify` in a directory that is not a git
repository will fail. Either initialize git before running `/speckit.specify`, or
disable the extension (`specify extension disable worktrees`). Do not silence the
failure.

## Vendored Third-Party Assets

Third-party skills, agents, commands, or scripts copied into this repository MUST be
vendored unmodified and accompanied by a `PROVENANCE.md` recording the upstream URL,
the exact source path, the pinned commit SHA, the vendoring date, and the license.
The upstream `LICENSE` file MUST be copied alongside the asset. Local edits to a
vendored file are forbidden; a needed change is either upstreamed or the asset is
forked under a distinct name with the fork documented. Updating a vendored asset
means re-copying from upstream and updating the recorded commit SHA in the same
change.

Rationale: Vendored files silently drift from upstream and lose their license trail.
A pinned SHA makes an update a diffable, auditable operation instead of guesswork.

## Upstream Compatibility Constraints

- The authoritative schema is upstream `extensions/EXTENSION-API-REFERENCE.md`
  (`schema_version: "1.0"`). This project tracks it; it does not extend it. Fields
  not defined upstream MUST NOT be invented in `extension.yml`.
- Supported hook events are the upstream lifecycle set only:
  `before_specify`/`after_specify`, `before_plan`/`after_plan`,
  `before_tasks`/`after_tasks`, `before_implement`/`after_implement`,
  `before_analyze`/`after_analyze`, and `before_constitution`/`after_constitution`.
  An unrecognized event name is a validation failure, not a no-op.
- Command files are Markdown with YAML frontmatter (`description`, optional `tools`,
  optional `scripts.sh`/`scripts.ps`) and receive user input via `$ARGUMENTS`.
- Extension configuration is read from
  `.specify/extensions/{extension-id}/{config-name}` and MUST tolerate a missing
  file when `required: false`.
- When upstream changes the schema, this template's own version MUST be bumped per
  Principle VIII and the drift documented in `CHANGELOG.md`.

## Development Workflow & Quality Gates

1. **Research first.** Before adding or changing template structure, read the
   current upstream `extensions/` guides. Copying a stale pattern is a defect.
2. **Spec-driven.** Non-trivial changes go through `/speckit.specify` →
   `/speckit.plan` → `/speckit.tasks` → `/speckit.implement`. The Constitution Check
   gate in `plan-template.md` is evaluated against the principles above.
3. **Validation gate.** Every change MUST leave `extension.yml` parseable, every
   referenced path resolvable, every command name matching Principle II, and every
   script pair complete per Principle V.
4. **Install gate.** Principle VII's install-run-remove cycle MUST pass before any
   release commit.
5. **Documentation gate.** A new command requires a README usage entry; a new config
   key requires a documented default in `config-template.yml`; a new hook requires
   its rationale in the README.
6. **Secrets.** No credentials, tokens, or personal URLs in any template, config,
   command, or script — placeholders only.
7. **Routing gate.** Every routing manifest MUST validate against the shipped
   schema, declare a token budget and a limit action per Principle XVII, declare
   `max_concurrent_agents` where it permits parallelism per Principle XVIII, and
   name only a skill present in the Skill Routing Catalog per Principle XX.
8. **Harness gate.** A change that alters how manifest values reach a run MUST be
   re-verified on at least one harness per category in the Harness Capability
   Matrix, and `docs/HARNESSES.md` MUST record the new verification date.

Commits follow `<type>: <description>` (`feat`, `fix`, `refactor`, `docs`, `test`,
`chore`, `perf`, `ci`).

## Governance

This constitution supersedes all other conventions in this repository. Where a
general guideline and a principle here conflict, the principle wins.

**Amendments** MUST be proposed as a pull request that states the principle added,
modified, or removed, the rationale, and the migration impact on extensions already
generated from this template. Amendments take effect on merge.

**Versioning** of this document follows semantic versioning: MAJOR for removing or
redefining a principle in a backward-incompatible way, MINOR for adding a principle
or materially expanding guidance, PATCH for clarifications and wording.

**Compliance review** is required on every pull request. Reviewers MUST verify each
principle explicitly; a PR that violates a principle without an approved amendment
MUST be blocked. Principle II violations and Principle VII gate failures are
non-negotiable blockers. Complexity beyond upstream schema MUST be justified in the
plan's Complexity Tracking section or removed.

Runtime development guidance lives in `CLAUDE.md` and the active feature's
`plan.md`; neither may contradict this constitution.

**Version**: 2.2.0 | **Ratified**: 2026-07-21 | **Last Amended**: 2026-07-22

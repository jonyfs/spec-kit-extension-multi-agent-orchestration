# Changelog

All notable changes to the `orchestration` extension are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-07-22

### Added

- `speckit.orchestration.check` command (alias `speckit.orchestration.verify`): a
  read-only verifier for a project's routing manifests. Reports findings at three
  levels — ERROR (blocking), WARN (advisory), INFO — and exits non-zero only on a
  blocking finding.
- `routing-manifest.schema.json`: the normative JSON Schema (draft 2020-12) for a
  routing manifest. `additionalProperties: false` at every level, so a provider's
  own reasoning knob is a shape error (constitution Principle XXIII).
- Manifest templates `config/skill-plan.yml` (read-mostly) and
  `config/skill-implement.yml` (parallel, writing), carrying `CUSTOMIZE` markers.
- `scripts/python/validate-routing.py`: the three-layer verifier — shape against
  the schema, single-manifest semantics, and cross-manifest plus environment
  checks. The catalog of valid stages is parsed from the project's constitution
  rather than copied, so code and governance cannot diverge (Principle XX).
- Paired `scripts/bash/routing-check.sh` and
  `scripts/powershell/routing-check.ps1`, both thin wrappers over the Python
  verifier so their behavior is identical by construction (Principle V).

### Notes

- This extension verifies declared contracts; it does not route. The Spec Kit
  extension mechanism cannot intercept model selection.
- Supersedes the `trace` reference extension that previously occupied `template/`.

[Unreleased]: https://github.com/jonyfs/spec-kit-extension-multi-agent-orchestration/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/jonyfs/spec-kit-extension-multi-agent-orchestration/releases/tag/v1.0.0

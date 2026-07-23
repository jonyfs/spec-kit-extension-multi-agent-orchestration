#!/usr/bin/env python3
"""Verify routing manifests against the constitution's routing principles.

A routing manifest (skill-{skill}.yml) is a declared contract for how one
workflow stage should run. This tool VERIFIES those declarations; it does not
route anything, because the Spec Kit extension API provides no means to intercept
model selection (see specs/002-routing-manifest-verifier/spec.md).

Three layers, run in order; every finding across every manifest is reported in a
single run (no stop-at-first-error):

  Layer 1  shape        - each manifest against routing-manifest.schema.json
  Layer 2  semantics    - per-manifest rules JSON Schema cannot express
  Layer 3  cross+env    - duplicate outputs, unset env vars, graphify presence

Findings are ERROR / WARN / INFO. Exit status is 1 iff at least one ERROR exists
(Principle XVII fails closed); WARN and INFO never fail the build, so the gate
runs on a CI runner lacking graphify or the model environment variables without
false alarms (Principles XVI, XX, XXIV).

The catalog of valid stages is parsed from the Skill Routing Catalog table in
.specify/memory/constitution.md — never copied here — so governance and code
cannot silently diverge (Principle XX). An unreadable catalog is a loud failure,
never an empty list.

Usage:
    validate-routing.py <manifest-dir> [<manifest-dir> ...]

The documented default location in a consuming project is
.specify/extensions/orchestration/config/. Package templates under
template/config/ are examples, never read as a project's declarations.

NOT verified: whether a configured model is available to the caller or in use by
the current session. Both need an authenticated provider call, which a gate on an
outside pull request cannot make.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: pip install pyyaml")

try:
    import json
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    sys.exit("jsonschema is required: pip install jsonschema")

# The core Spec Kit commands, always installed. Used to distinguish a stage that
# is uninstalled (in the catalog, absent here → INFO) from one that is unknown
# (absent from the catalog → ERROR). Mirrors CORE_COMMANDS in validate-extension.py.
CORE_INSTALLED = {
    "speckit.constitution",
    "speckit.specify",
    "speckit.clarify",
    "speckit.plan",
    "speckit.tasks",
    "speckit.analyze",
    "speckit.checklist",
    "speckit.implement",
}


class Report:
    """Collects findings across every manifest and prints them once."""

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.infos: list[str] = []

    def error(self, where: str, message: str) -> None:
        self.errors.append(f"{where}: {message}")

    def warn(self, where: str, message: str) -> None:
        self.warnings.append(f"{where}: {message}")

    def info(self, where: str, message: str) -> None:
        self.infos.append(f"{where}: {message}")

    def print_and_exit_code(self) -> int:
        for message in self.errors:
            print(f"  ERROR  {message}")
        for message in self.warnings:
            print(f"  WARN   {message}")
        for message in self.infos:
            print(f"  INFO   {message}")
        total = len(self.errors) + len(self.warnings) + len(self.infos)
        if total == 0:
            print("No findings.")
        print(
            f"\n{len(self.errors)} error(s), {len(self.warnings)} warning(s), "
            f"{len(self.infos)} note(s)."
        )
        return 1 if self.errors else 0


def find_constitution(start: Path) -> Path | None:
    """Walk up from start looking for .specify/memory/constitution.md."""
    for directory in [start, *start.parents]:
        candidate = directory / ".specify" / "memory" / "constitution.md"
        if candidate.is_file():
            return candidate
    return None


def parse_catalog(constitution: Path) -> set[str]:
    """Extract routable stages from the Skill Routing Catalog table.

    A row counts as a routable stage only when its Source column is not
    'unknown' — an unverified stage (speckit.baseline) is in the table but must
    ship no manifest, per Principle XX. Raises on a missing or unreadable table
    rather than returning an empty set (FR-012b).
    """
    text = constitution.read_text(encoding="utf-8")
    match = re.search(
        r"^## Skill Routing Catalog\s*$(.*?)^## ", text, re.MULTILINE | re.DOTALL
    )
    if not match:
        raise ValueError(
            "Skill Routing Catalog section not found in the constitution — "
            "cannot determine which stages are routable"
        )
    section = match.group(1)
    stages: set[str] = set()
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        skill_cell = cells[0]
        source_cell = cells[2].lower()
        m = re.match(r"^`(speckit\.[a-z0-9-]+)`$", skill_cell)
        if not m:
            continue  # header row, separator, or malformed
        if source_cell == "unknown":
            continue  # unverified — not routable until confirmed
        stages.add(m.group(1))
    if not stages:
        raise ValueError(
            "Skill Routing Catalog table found but no routable stages parsed — "
            "the table format may have changed"
        )
    return stages


def load_manifests(dirs: list[Path], report: Report) -> list[tuple[Path, dict]]:
    """Load every skill-*.yml under the given directories."""
    manifests: list[tuple[Path, dict]] = []
    for directory in dirs:
        if not directory.is_dir():
            report.error(str(directory), "manifest directory does not exist")
            continue
        for path in sorted(directory.glob("skill-*.yml")):
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
            except yaml.YAMLError as exc:
                report.error(str(path), f"not valid YAML: {exc}")
                continue
            if not isinstance(data, dict):
                report.error(str(path), "manifest is not a mapping")
                continue
            manifests.append((path, data))
    return manifests


def layer1_shape(path: Path, data: dict, validator: Draft202012Validator, report: Report) -> bool:
    """Validate one manifest against the JSON Schema. Returns True when shape is OK."""
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    for err in errors:
        location = "/".join(str(p) for p in err.path) or "(root)"
        report.error(str(path), f"schema: {location}: {err.message}")
    return not errors


def layer2_semantics(path: Path, data: dict, catalog: set[str], report: Report) -> None:
    """Per-manifest rules JSON Schema cannot express."""
    where = str(path)
    skill = data.get("skill", "")

    # Principle XX: the stage must be routable.
    if skill not in catalog:
        report.error(where, f"skill {skill!r} is not a routable stage in the catalog")
    elif skill not in CORE_INSTALLED:
        report.info(where, f"skill {skill!r} is in the catalog but not installed here (inactive)")

    guardrails = (data.get("governance") or {}).get("token_guardrails") or {}
    action = guardrails.get("action_on_limit")
    artifacts = data.get("artifacts") or {}
    writes = artifacts.get("writes_artifacts")
    output = artifacts.get("output")

    # Principle XVII: a writing stage may not drop context to continue.
    if action == "truncate_context" and writes is True:
        report.error(
            where,
            "action_on_limit is truncate_context but writes_artifacts is true; "
            "a writing stage must not silently continue on a truncated context",
        )

    # Principle XVII: truncation_priority is dead config when not truncating.
    if action != "truncate_context" and "truncation_priority" in guardrails:
        report.warn(
            where,
            "truncation_priority is set but action_on_limit is not truncate_context; "
            "this configuration is never used",
        )

    # Principle XVIII: a parallel stage cannot own a single file.
    strategy = data.get("execution_strategy") or {}
    concurrency = strategy.get("max_concurrent_agents")
    if strategy.get("parallelism_mode") == "waves" and isinstance(concurrency, int) and concurrency > 1:
        if output is not None:
            report.error(
                where,
                f"runs {concurrency} concurrent agents while claiming a single owned "
                f"output {output!r}; concurrent units must not share one file",
            )


def layer3_cross_and_env(manifests: list[tuple[Path, dict]], report: Report) -> None:
    """Cross-manifest ownership and environment probing."""
    # Principle XVIII: no two stages may declare the same output.
    outputs: dict[str, list[str]] = {}
    for path, data in manifests:
        output = (data.get("artifacts") or {}).get("output")
        if output:
            outputs.setdefault(output, []).append(str(path))
    for output, owners in sorted(outputs.items()):
        if len(owners) > 1:
            report.error(
                "cross-manifest",
                f"output {output!r} is claimed by more than one manifest: "
                + ", ".join(owners),
            )

    # Principle XV: referenced environment variables should be defined.
    for path, data in manifests:
        routing = data.get("routing") or {}
        for key in ("provider_env", "model_env"):
            var = routing.get(key)
            if var and var not in os.environ:
                report.warn(str(path), f"{key} names {var!r}, which is not set in the environment")

    # Principle XXIV: retrieval declared but graphify unavailable.
    any_retrieval = any(
        ((data.get("context") or {}).get("retrieval") or {}).get("enabled")
        for _, data in manifests
    )
    if any_retrieval:
        if shutil.which("graphify") is None:
            report.warn(
                "environment",
                "retrieval is enabled in at least one manifest but 'graphify' is not on "
                "PATH; those stages fall back to their non-graph context path",
            )
        elif not Path("graphify-out").is_dir():
            report.warn(
                "environment",
                "retrieval is enabled but graphify-out/ is absent; the graph has not "
                "been built yet",
            )

    # Principle XVII/XXI: aggregate budget across all declared stages (informational).
    total = 0
    for _, data in manifests:
        budget = ((data.get("governance") or {}).get("token_guardrails") or {}).get("max_total_tokens")
        if isinstance(budget, int):
            total += budget
    if total:
        report.info("aggregate", f"declared token budget across all manifests: {total}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("dirs", nargs="+", type=Path, help="Directories holding skill-*.yml manifests")
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path(__file__).resolve().parent.parent.parent / "routing-manifest.schema.json",
        help="Path to routing-manifest.schema.json",
    )
    args = parser.parse_args()

    report = Report()

    if not args.schema.is_file():
        print(f"Schema not found: {args.schema}", file=sys.stderr)
        return 1
    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    constitution = find_constitution(args.dirs[0].resolve())
    if constitution is None:
        print("Could not locate .specify/memory/constitution.md — cannot load the stage catalog", file=sys.stderr)
        return 1
    try:
        catalog = parse_catalog(constitution)
    except ValueError as exc:
        print(f"Catalog error: {exc}", file=sys.stderr)
        return 1

    manifests = load_manifests(args.dirs, report)

    # FR-021: no declarations is reported distinctly, and is not success.
    if not manifests and not report.errors:
        report.error(
            "  ".join(str(d) for d in args.dirs),
            "no routing manifests (skill-*.yml) found; a check with nothing to "
            "examine has not passed",
        )
        return report.print_and_exit_code()

    for path, data in manifests:
        if layer1_shape(path, data, validator, report):
            layer2_semantics(path, data, catalog, report)
    layer3_cross_and_env(manifests, report)

    print(f"Verified {len(manifests)} routing manifest(s) against catalog of {len(catalog)} stage(s)")
    return report.print_and_exit_code()


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env bash
# Thin wrapper: locate the routing manifests and hand them to the Python verifier.
# Behavioral parity with routing-check.ps1 comes from both delegating to the same
# validate-routing.py, rather than reimplementing the logic twice (Principle V).
#
# Usage: routing-check.sh [manifest-dir]
# Default manifest-dir is the consuming project's own configuration directory.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VALIDATOR="$SCRIPT_DIR/../python/validate-routing.py"
PYTHON="${PYTHON:-python3}"

MANIFEST_DIR="${1:-.specify/extensions/orchestration/config}"

exec "$PYTHON" "$VALIDATOR" "$MANIFEST_DIR"

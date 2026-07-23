#!/usr/bin/env bash
# Constitution Principle XXV: a check that cannot fail is not a check.
#
# scripts/validate-routing.py is a CI gate over routing manifests. Until it has
# been observed rejecting something — and rejecting it for the right reason — its
# green tells us nothing, because passing and being unreachable look identical.
# This asserts it fails on a deliberately broken set, names each planted
# violation, and still passes a valid set (so it is not a blanket rejector).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INVALID="$REPO_ROOT/tests/fixtures/invalid-routing"
VALID="$REPO_ROOT/tests/fixtures/valid-routing"
VALIDATOR="$REPO_ROOT/template/scripts/python/validate-routing.py"
PYTHON="${PYTHON:-python3}"

failures=0
fail() {
  echo "FAIL: $1"
  failures=$((failures + 1))
}

echo "Asserting the routing validator rejects a deliberately broken manifest set"
output="$("$PYTHON" "$VALIDATOR" "$INVALID" 2>&1)" && rc=0 || rc=$?

if [ "$rc" -eq 0 ]; then
  echo "$output"
  fail "validator exited 0 on a manifest set that violates six rules"
  exit 1
fi

# Each planted violation, and the principle it enforces. A bare non-zero exit
# would not tell us which rule stopped firing; this does.
declare -a expectations=(
  "'max_total_tokens' is a required property|XVII: token budget required"
  "truncate_context but writes_artifacts is true|XVII: no silent truncation while writing"
  "Additional properties are not allowed .'reasoning_budget'|XXIII: no provider-native knobs"
  "is not a routable stage in the catalog|XX: route only cataloged stages"
  "'max_concurrent_agents' is a required property|XVIII: waves must cap concurrency"
  "is claimed by more than one manifest|XVIII: exclusive artifact ownership"
)

for expectation in "${expectations[@]}"; do
  pattern="${expectation%%|*}"
  label="${expectation#*|}"
  if ! grep -qE "$pattern" <<< "$output"; then
    fail "validator did not report — $label"
  fi
done

echo "Asserting the routing validator passes a valid manifest set"
valid_output="$("$PYTHON" "$VALIDATOR" "$VALID" 2>&1)" && vrc=0 || vrc=$?
if [ "$vrc" -ne 0 ]; then
  echo "$valid_output"
  fail "validator exited $vrc on a valid manifest set (blanket rejector)"
fi

if [ "$failures" -gt 0 ]; then
  echo
  echo "Invalid-set output was:"
  echo "$output"
  exit 1
fi

echo "OK: rejected the broken set for all six reasons, and passed the valid set"

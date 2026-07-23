#!/usr/bin/env pwsh
# Thin wrapper: locate the routing manifests and hand them to the Python verifier.
# Behavioral parity with routing-check.sh comes from both delegating to the same
# validate-routing.py, rather than reimplementing the logic twice (Principle V).
#
# Usage: routing-check.ps1 [-ManifestDir <path>]
# Default -ManifestDir is the consuming project's own configuration directory.

[CmdletBinding()]
param(
    [string]$ManifestDir = ".specify/extensions/orchestration/config"
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$validator = Join-Path $scriptDir "../python/validate-routing.py"
$python = if ($env:PYTHON) { $env:PYTHON } else { "python3" }

& $python $validator $ManifestDir
exit $LASTEXITCODE

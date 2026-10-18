#!/usr/bin/env bash
# ==============================================================================
# Enterprise Software Company — Verification Script
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔍 Running Acceptance Criteria verification..."
python3 "$SCRIPT_DIR/tests/test_acceptance_criteria.py"

echo ""
echo "🔍 Running E2E Test Suite..."
python3 "$SCRIPT_DIR/tests/test_e2e_suite.py"

echo ""
echo "✅ All verification checks PASSED!"

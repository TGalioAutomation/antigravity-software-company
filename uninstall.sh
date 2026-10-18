#!/usr/bin/env bash
# ==============================================================================
# Enterprise Software Company — Uninstaller
# ==============================================================================
set -euo pipefail

DEST_GLOBAL="$HOME/.gemini/config/plugins/software-company"

echo "🗑️ Removing Enterprise Software Company Plugin..."
rm -rf "$DEST_GLOBAL"
echo "✓ Removed $DEST_GLOBAL"

if [ -n "${ANTIGRAVITY_LS_ADDRESS:-}" ] && [ -n "${ANTIGRAVITY_CSRF_TOKEN:-}" ]; then
  curl -sS -X POST \
    "http://${ANTIGRAVITY_LS_ADDRESS}/exa.language_server_pb.LanguageServerService/DeletePlugin" \
    -H "Content-Type: application/json" \
    -H "x-codeium-csrf-token: ${ANTIGRAVITY_CSRF_TOKEN}" \
    -d '{"pluginId":"software-company"}' >/dev/null 2>&1 || true
  echo "✓ Unregistered from Antigravity Language Server"
fi

echo "🎉 Plugin uninstalled successfully."

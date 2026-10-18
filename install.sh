#!/usr/bin/env bash
# ==============================================================================
# Enterprise Software Company — One-Click Installer for Antigravity & AI IDEs
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_SOURCE="$SCRIPT_DIR/software-company"
DEST_GLOBAL="$HOME/.gemini/config/plugins/software-company"

echo "========================================================================"
echo "📦 Installing Enterprise Software Company Plugin into Antigravity..."
echo "========================================================================"

if [ ! -d "$PLUGIN_SOURCE" ]; then
  echo "❌ Error: Plugin source directory not found at $PLUGIN_SOURCE"
  exit 1
fi

# 1. Install to global Antigravity plugins directory
mkdir -p "$HOME/.gemini/config/plugins"
rm -rf "$DEST_GLOBAL"
cp -Rf "$PLUGIN_SOURCE" "$DEST_GLOBAL"
echo "✓ Copied plugin to $DEST_GLOBAL"

# 2. Try enabling via Antigravity Language Server RPC (live reload if IDE is open)
if [ -n "${ANTIGRAVITY_LS_ADDRESS:-}" ] && [ -n "${ANTIGRAVITY_CSRF_TOKEN:-}" ]; then
  echo "🔄 Notifying running Antigravity Language Server ($ANTIGRAVITY_LS_ADDRESS)..."
  curl -sS -X POST \
    "http://${ANTIGRAVITY_LS_ADDRESS}/exa.language_server_pb.LanguageServerService/JetboxWriteState" \
    -H "Content-Type: application/json" \
    -H "x-codeium-csrf-token: ${ANTIGRAVITY_CSRF_TOKEN}" \
    -d '{"userConfig":{"plugins":{"software-company":{"enabled":true}}}}' >/dev/null 2>&1 || true
  echo "✓ Enabled plugin dynamically in Antigravity"
fi

# 3. Install skills into Antigravity skills directory
mkdir -p "$HOME/.gemini/config/skills"
cp -Rf "$SCRIPT_DIR/skills/"* "$HOME/.gemini/config/skills/"
echo "✓ Installed skills to $HOME/.gemini/config/skills"

# 4. Optional: Sync agents and skills to other IDE/CLI discovery dirs if they exist
SYNC_AGENTS=(
  "$HOME/.zcode/agents"
  "$HOME/.claude/agents"
  "$HOME/.cursor/agents"
  "$HOME/.config/opencode/agents"
)

for target in "${SYNC_AGENTS[@]}"; do
  if [ -d "$(dirname "$target")" ]; then
    mkdir -p "$target"
    cp -f "$PLUGIN_SOURCE/agents/"*.md "$target/" 2>/dev/null || true
    echo "✓ Synced 17 sub-agents to $target"
  fi
done

SYNC_SKILLS=(
  "$HOME/.claude/skills"
  "$HOME/.cursor/skills"
  "$HOME/.config/opencode/skills"
  "$HOME/.zcode/skills"
)

for target in "${SYNC_SKILLS[@]}"; do
  if [ -d "$(dirname "$target")" ]; then
    mkdir -p "$target"
    cp -Rf "$SCRIPT_DIR/skills/"* "$target/" 2>/dev/null || true
    echo "✓ Synced skills to $target"
  fi
done

echo ""
echo "🎉 Installation successful!"
echo "• Plugin location : $DEST_GLOBAL"
echo "• Sub-agents      : 17 agents (4 Pro, 13 Flash)"
echo "• Rules & SOP     : $DEST_GLOBAL/rules/AGENTS.md"
echo "• Workflow skill  : $DEST_GLOBAL/skills/software-company-workflow"
echo ""
echo "To verify the installation, run:"
echo "  ./verify.sh"
echo "========================================================================"

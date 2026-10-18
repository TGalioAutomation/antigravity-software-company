#!/usr/bin/env bash
# ==============================================================================
# Enterprise Software Company — Full Standalone Installer for Antigravity & IDEs
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_SOURCE="$SCRIPT_DIR/software-company"
DEST_GLOBAL="$HOME/.gemini/config/plugins/software-company"

echo "========================================================================"
echo "📦 Installing Enterprise Software Company Plugin & Full Asset Library..."
echo "========================================================================"

if [ ! -d "$PLUGIN_SOURCE" ]; then
  echo "❌ Error: Plugin source directory not found at $PLUGIN_SOURCE"
  exit 1
fi

# 1. Install plugin (17 sub-agents + 26 core preloaded skills + rules/AGENTS.md)
mkdir -p "$HOME/.gemini/config/plugins"
rm -rf "$DEST_GLOBAL"
cp -Rf "$PLUGIN_SOURCE" "$DEST_GLOBAL"
echo "✓ Installed Antigravity Plugin (17 agents + 26 core skills) → $DEST_GLOBAL"

# 2. Ensure Priority-3 Antigravity skills (prompt-master, clean-room) and Priority-5 full library (314 skills)
mkdir -p "$HOME/.gemini/config/skills"
cp -Rf "$SCRIPT_DIR/skills/prompt-master" "$HOME/.gemini/config/skills/"
cp -Rf "$SCRIPT_DIR/skills/clean-room" "$HOME/.gemini/config/skills/"
echo "✓ Installed Priority-3 skills (prompt-master, clean-room) → $HOME/.gemini/config/skills"

mkdir -p "$HOME/.agents/skills"
cp -Rf "$SCRIPT_DIR/skills/"* "$HOME/.agents/skills/"
cat > "$HOME/.gemini/config/skills.json" <<EOF
{
  "skills": [
    {
      "path": "$HOME/.agents/skills"
    }
  ]
}
EOF
echo "✓ Installed full 314-skill library → $HOME/.agents/skills (linked via skills.json)"

# 3. Install rules (22 language/common rule modules) & commands (97 workflows)
mkdir -p "$HOME/.agents/rules" "$HOME/.agents/commands"
cp -Rf "$SCRIPT_DIR/rules/"* "$HOME/.agents/rules/" 2>/dev/null || true
cp -Rf "$SCRIPT_DIR/commands/"* "$HOME/.agents/commands/" 2>/dev/null || true
echo "✓ Installed 22 rule modules → $HOME/.agents/rules & 97 commands → $HOME/.agents/commands"

# 4. Notify running Antigravity Language Server (live reload if IDE is open)
if [ -n "${ANTIGRAVITY_LS_ADDRESS:-}" ] && [ -n "${ANTIGRAVITY_CSRF_TOKEN:-}" ]; then
  echo "🔄 Notifying running Antigravity Language Server ($ANTIGRAVITY_LS_ADDRESS)..."
  curl -sS -X POST \
    "http://${ANTIGRAVITY_LS_ADDRESS}/exa.language_server_pb.LanguageServerService/JetboxWriteState" \
    -H "Content-Type: application/json" \
    -H "x-codeium-csrf-token: ${ANTIGRAVITY_CSRF_TOKEN}" \
    -d '{"userConfig":{"plugins":{"software-company":{"enabled":true}}}}' >/dev/null 2>&1 || true
  echo "✓ Enabled plugin dynamically in Antigravity"
fi

# 5. Optional: Sync agents and commands to other IDE/CLI discovery dirs if they exist
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
    echo "✓ Synced 17 sub-agents → $target"
  fi
done

echo ""
echo "🎉 Installation successful!"
echo "• Antigravity Plugin : $DEST_GLOBAL"
echo "• Core Sub-Agents    : 17 cost-optimized agents (4 Pro / 13 Flash)"
echo "• Core Plugin Skills : 26 preloaded engineering skills inside plugin"
echo "• Full Skill Library : 314 standalone skills in $HOME/.agents/skills"
echo "• Engineering Rules  : 22 language/common rule sets in $HOME/.agents/rules"
echo "• Workflow Commands  : 97 commands in $HOME/.agents/commands"
echo "• Extra Agent Catalog: 71 specialized agents in $SCRIPT_DIR/agents-catalog"
echo "========================================================================"

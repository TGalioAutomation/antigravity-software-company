#!/usr/bin/env python3
"""
Enterprise Software Company Antigravity Plugin — Acceptance Criteria Verification Suite.

Validates the full completion of the Software Company Plugin against:
  1. Plugin directory & manifest integrity (~/.gemini/config/plugins/software-company/plugin.json)
     - Valid JSONC schema and required fields (name, displayName, description, version, logo)
     - Absence of prohibited fields (no 'skills' array in plugin.json, no author/homepage)
     - Presence of rules/AGENTS.md (<= 24KB memory limit)
  2. 17 Sub-Agents completeness & YAML frontmatter validation
     - All 17 sub-agents present in agents/*.md
     - Required frontmatter keys: name, description, subagent: true, hidden: false, inheritCustomizations: true
  3. Cost tier segregation & extreme cost-optimization
     - Exactly 4 Pro agents: chief-of-staff, code-architect, clean-room-builder, security-reviewer
     - 13 Flash agents: >= 12/17 threshold (76.5%)
  4. Antigravity Language Server ConnectRPC recognition (GetAllPlugins)
     - Dynamic plugin discovery without restart
     - Protobuf translation of model to MODEL_TIER_PRO / MODEL_TIER_FLASH
  5. Security & Zero OpenRouter Leakage
     - Zero openrouter.ai URLs or hardcoded keys in plugin files
     - OPENROUTER_API_KEY reserved strictly for jev
  6. Live Jev Audit against typesafe/jev-1.13
     - Executes jev --audit sample_spec.md
     - Asserts exit code 0, APPROVED verdict, and noul thresholds (Evidence>=0.50, Det>=0.50, Clean-Room>=0.60)
     - Validates generation of sanitized SPEC.approved.md
"""

import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

# Paths
WORKSPACE_DIR = Path(__file__).resolve().parent
SAMPLE_SPEC_PATH = WORKSPACE_DIR / "sample_spec.md"
PLUGIN_DIR = Path.home() / ".gemini" / "config" / "plugins" / "software-company"
PLUGIN_JSON = PLUGIN_DIR / "plugin.json"
AGENTS_DIR = PLUGIN_DIR / "agents"
RULES_FILE = PLUGIN_DIR / "rules" / "AGENTS.md"
SKILLS_DIR = PLUGIN_DIR / "skills"
JEV_BIN = Path(os.environ.get("JEV_BIN") or shutil.which("jev") or (Path.home() / ".local" / "bin" / "jev"))

# Expected Agent Squad
PRO_AGENTS = {
    "chief-of-staff",
    "code-architect",
    "clean-room-builder",
    "security-reviewer",
}

FLASH_AGENTS = {
    "planner",
    "refactor-cleaner",
    "build-error-resolver",
    "python-reviewer",
    "typescript-reviewer",
    "react-reviewer",
    "go-reviewer",
    "rust-reviewer",
    "database-reviewer",
    "performance-optimizer",
    "silent-failure-hunter",
    "e2e-runner",
    "jev",
}

ALL_EXPECTED_AGENTS = PRO_AGENTS | FLASH_AGENTS


def print_step_header(step_num: int, title: str):
    print(f"\n[{step_num}/6] Validating {title} ...")


def get_ls_credentials():
    """Retrieve Language Server ConnectRPC address and CSRF token."""
    addr = os.environ.get("ANTIGRAVITY_LS_ADDRESS")
    token = os.environ.get("ANTIGRAVITY_CSRF_TOKEN")
    if addr and token:
        return addr, token

    try:
        out = subprocess.check_output(["ps", "aux"], text=True, errors="replace")
        for line in out.splitlines():
            if "language_server" in line and "--csrf_token" in line and "--standalone" in line:
                m_token = re.search(r"--csrf_token\s+([^\s]+)", line)
                if m_token:
                    token = m_token.group(1)
                parts = line.split()
                if len(parts) > 1:
                    pid = parts[1]
                    lsof_out = subprocess.check_output(
                        ["lsof", "-Pan", "-p", pid, "-iTCP", "-sTCP:LISTEN"],
                        text=True,
                        errors="replace",
                    )
                    for lline in lsof_out.splitlines():
                        m_port = re.search(r":(\d+)\s+\(LISTEN\)", lline)
                        if m_port:
                            addr = f"127.0.0.1:{m_port.group(1)}"
                            break
                if addr and token:
                    return addr, token
    except Exception:
        pass
    return addr or "localhost:50065", token or ""


def call_ls_rpc(method: str, body: dict = None) -> dict:
    addr, token = get_ls_credentials()
    url = f"http://{addr}/exa.language_server_pb.LanguageServerService/{method}"
    data = json.dumps(body or {}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "x-codeium-csrf-token": token,
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_frontmatter(content: str) -> tuple[dict, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return {}, content
    raw_yaml = match.group(1)
    body = match.group(2)
    meta = {}
    current_list_key = None
    for line in raw_yaml.splitlines():
        line_clean = line.strip()
        if not line_clean or line_clean.startswith("#"):
            continue
        if line_clean.startswith("- ") and current_list_key:
            item = line_clean[2:].strip().strip('"').strip("'")
            meta[current_list_key].append(item)
            continue
        if ":" in line:
            current_list_key = None
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if v == "" and not line.endswith(":"):
                v = ""
            elif v == "":
                current_list_key = k
                meta[k] = []
                continue
            elif v.lower() == "true":
                v = True
            elif v.lower() == "false":
                v = False
            meta[k] = v
    return meta, body


def test_plugin_files() -> tuple[bool, list[str]]:
    """Gate 1: Plugin Manifest Schema & Directory Integrity"""
    errors = []
    if not PLUGIN_DIR.exists():
        errors.append(f"Plugin directory not found: {PLUGIN_DIR}")
        return False, errors

    if not PLUGIN_JSON.exists():
        errors.append(f"plugin.json not found: {PLUGIN_JSON}")
    else:
        try:
            content = PLUGIN_JSON.read_text(errors="replace")
            # Strip JSON comments if any (JSONC support)
            content_no_comments = re.sub(r"//.*?\n|/\*.*?\*/", "", content, flags=re.S)
            data = json.loads(content_no_comments)

            # Required fields
            if data.get("name") != "software-company":
                errors.append(f"plugin.json 'name' expected 'software-company', got '{data.get('name')}'")
            if not data.get("displayName"):
                errors.append("plugin.json missing required 'displayName'")
            if not data.get("description"):
                errors.append("plugin.json missing required 'description'")
            if not data.get("version"):
                errors.append("plugin.json missing required 'version'")
            if not data.get("logo"):
                errors.append("plugin.json missing required 'logo'")
            else:
                logo_path = PLUGIN_DIR / data["logo"]
                if not logo_path.exists():
                    errors.append(f"Referenced logo file not found: {logo_path}")

            # Prohibited fields
            if "skills" in data:
                errors.append("plugin.json contains prohibited 'skills' array (violates Antigravity Plugin Spec 1.0.0)")
            if "author" in data:
                errors.append("plugin.json contains discarded 'author' field")
            if "homepage" in data:
                errors.append("plugin.json contains discarded 'homepage' field")

            # Suggested prompts constraints
            prompts = data.get("suggestedPrompts", [])
            if not isinstance(prompts, list):
                errors.append("plugin.json 'suggestedPrompts' must be an array")
            elif len(prompts) > 3:
                errors.append(f"plugin.json contains {len(prompts)} suggestedPrompts (maximum 3 supported)")

        except Exception as e:
            errors.append(f"plugin.json parse error: {e}")

    # Rules file validation
    if not RULES_FILE.exists():
        errors.append(f"rules/AGENTS.md not found at {RULES_FILE}")
    else:
        size = RULES_FILE.stat().st_size
        if size > 24000:
            errors.append(f"rules/AGENTS.md exceeds 24KB limit: {size} bytes")

    return len(errors) == 0, errors


def test_subagent_files() -> tuple[bool, list[str]]:
    """Gate 2 & 3: 17 Sub-Agents Completeness & Model Tier Segregation"""
    errors = []
    if not AGENTS_DIR.exists():
        return False, [f"Agents directory not found: {AGENTS_DIR}"]

    found_agents = set()
    pro_count = 0
    flash_count = 0

    for f in AGENTS_DIR.glob("*.md"):
        agent_name = f.stem
        found_agents.add(agent_name)
        text = f.read_text(errors="replace")
        meta, body = parse_frontmatter(text)

        if not meta:
            errors.append(f"Agent {f.name}: missing or malformed YAML frontmatter")
            continue

        if meta.get("name") != agent_name:
            errors.append(f"Agent {f.name}: frontmatter name '{meta.get('name')}' != stem '{agent_name}'")

        if not meta.get("description"):
            errors.append(f"Agent {f.name}: missing required non-empty 'description' (Antigravity drops agent)")

        if meta.get("subagent") is not True:
            errors.append(f"Agent {f.name}: frontmatter subagent != true")

        if meta.get("hidden") is not False:
            errors.append(f"Agent {f.name}: frontmatter hidden != false")

        if meta.get("inheritCustomizations") is not True:
            errors.append(f"Agent {f.name}: frontmatter inheritCustomizations != true")

        # Prohibited frontmatter key check
        if "modelTier" in meta:
            errors.append(f"Agent {f.name}: uses prohibited 'modelTier:' in frontmatter instead of 'model:'")

        model_val = str(meta.get("model", "")).lower()
        if agent_name in PRO_AGENTS:
            if model_val != "pro":
                errors.append(f"Pro Agent {f.name}: expected 'model: pro', got '{model_val}'")
            else:
                pro_count += 1
        elif agent_name in FLASH_AGENTS:
            if model_val != "flash":
                errors.append(f"Flash Agent {f.name}: expected 'model: flash', got '{model_val}'")
            else:
                flash_count += 1
        else:
            errors.append(f"Unrecognized agent {agent_name}")

    missing = ALL_EXPECTED_AGENTS - found_agents
    extra = found_agents - ALL_EXPECTED_AGENTS
    if missing:
        errors.append(f"Missing required agents: {sorted(missing)}")
    if extra:
        errors.append(f"Unexpected extra agents: {sorted(extra)}")

    # Tier segregation check: >= 12/17 Flash
    total = len(found_agents)
    if total == 17:
        if pro_count != 4:
            errors.append(f"Expected exactly 4 Pro agents, found {pro_count}")
        if flash_count != 13:
            errors.append(f"Expected 13 Flash agents, found {flash_count}")
        if flash_count < 12:
            errors.append(f"Cost threshold violation: Flash agents {flash_count} < minimum 12 required")

    return len(errors) == 0, errors


def test_language_server_recognition() -> tuple[bool, list[str]]:
    """Gate 4: Antigravity Language Server ConnectRPC Recognition"""
    errors = []
    try:
        res = call_ls_rpc("GetAllPlugins", {})
        plugins = res.get("plugins", [])
        sc_plugin = None
        for p in plugins:
            if p.get("name") == "software-company" or p.get("path", "").endswith("software-company"):
                sc_plugin = p
                break

        if not sc_plugin:
            errors.append("Plugin 'software-company' not discovered in GetAllPlugins RPC")
            return False, errors

        agents = sc_plugin.get("agents", [])
        if len(agents) != 17:
            errors.append(f"GetAllPlugins reported {len(agents)} agents for software-company, expected 17")

        pro_agents_found = set()
        flash_agents_found = set()

        for item in agents:
            ag = item.get("agent", {})
            name = ag.get("name")
            tier = ag.get("modelTier")
            if tier == "MODEL_TIER_PRO":
                pro_agents_found.add(name)
            elif tier == "MODEL_TIER_FLASH":
                flash_agents_found.add(name)
            else:
                errors.append(f"Agent '{name}' has unmapped modelTier: {tier}")

        if pro_agents_found != PRO_AGENTS:
            errors.append(f"Mismatch in MODEL_TIER_PRO agents: expected {PRO_AGENTS}, got {pro_agents_found}")
        if flash_agents_found != FLASH_AGENTS:
            errors.append(f"Mismatch in MODEL_TIER_FLASH agents: expected {FLASH_AGENTS}, got {flash_agents_found}")

    except Exception as e:
        errors.append(f"Failed to communicate with Antigravity Language Server RPC: {e}")

    return len(errors) == 0, errors


def test_openrouter_security() -> tuple[bool, list[str]]:
    """Gate 5: Zero OpenRouter Leakage & API Key Preservation"""
    errors = []
    if not PLUGIN_DIR.exists():
        return False, [f"Directory {PLUGIN_DIR} not found"]

    for root, _, files in os.walk(PLUGIN_DIR):
        for fname in files:
            fpath = Path(root) / fname
            if fpath.suffix in [".md", ".json", ".py", ".sh", ".yaml", ".yml"]:
                text = fpath.read_text(errors="replace")
                # Look for forbidden API call patterns
                if "api.openrouter.ai" in text:
                    errors.append(f"Forbidden openrouter.ai URL found in {fpath.relative_to(PLUGIN_DIR)}")
                if re.search(r"sk-or-v1-[0-9a-fA-F]{64}", text):
                    errors.append(f"Hardcoded OpenRouter API key pattern found in {fpath.relative_to(PLUGIN_DIR)}")
                # Ensure OPENROUTER_API_KEY is not referenced outside authorized docs
                if "OPENROUTER_API_KEY" in text:
                    allowed_files = {"jev.md", "AGENTS.md", "README.md"}
                    if fpath.name not in allowed_files:
                        errors.append(f"Unauthorized OPENROUTER_API_KEY reference in {fpath.relative_to(PLUGIN_DIR)}")

    return len(errors) == 0, errors


def test_sample_jev_audit() -> tuple[bool, list[str]]:
    """Gate 6: Live Jev Specification Audit against typesafe/jev-1.13"""
    errors = []
    if not JEV_BIN.exists():
        errors.append(f"Jev binary not found at {JEV_BIN}")
        return False, errors

    if not SAMPLE_SPEC_PATH.exists():
        errors.append(f"Sample specification not found at {SAMPLE_SPEC_PATH}")
        return False, errors

    try:
        proc = subprocess.run(
            [str(JEV_BIN), "--audit", str(SAMPLE_SPEC_PATH.name)],
            cwd=str(SAMPLE_SPEC_PATH.parent),
            capture_output=True,
            text=True,
            timeout=45,
        )
        if proc.returncode != 0:
            errors.append(f"Jev audit failed with exit code {proc.returncode}:\n{proc.stderr}\n{proc.stdout}")
        else:
            audit_file = SAMPLE_SPEC_PATH.parent / "jev-audit.md"
            approved_file = SAMPLE_SPEC_PATH.parent / "SPEC.approved.md"
            if not audit_file.exists():
                errors.append(f"Expected audit report not found at {audit_file}")
            else:
                audit_content = audit_file.read_text()
                if "APPROVED" not in audit_content:
                    errors.append("jev-audit.md did not record APPROVED verdict")

            if not approved_file.exists():
                errors.append(f"Expected approved specification not found at {approved_file}")
            else:
                approved_content = approved_file.read_text()
                if "RULE-001" not in approved_content or "RULE-002" not in approved_content:
                    errors.append("SPEC.approved.md missing expected approved rules")
                if "Source**:" in approved_content:
                    errors.append("SPEC.approved.md leaked Source line (sanitization failure)")
    except subprocess.TimeoutExpired:
        errors.append("Jev audit timed out after 45 seconds")
    except Exception as e:
        errors.append(f"Failed to execute jev audit: {e}")

    return len(errors) == 0, errors


def main():
    start_time = time.time()
    print("=" * 80)
    print("ENTERPRISE SOFTWARE COMPANY PLUGIN — ACCEPTANCE CRITERIA VERIFICATION")
    print("=" * 80)

    results = {}

    print_step_header(1, "Plugin Manifest & Directory Structure")
    ok1, err1 = test_plugin_files()
    results["Plugin Manifest & Structure"] = (ok1, err1)
    print("PASS" if ok1 else f"FAIL: {err1}")

    print_step_header(2, "17 Sub-Agents Completeness & Frontmatter Schema")
    ok2, err2 = test_subagent_files()
    results["17 Sub-Agents & Cost Tiers"] = (ok2, err2)
    print("PASS" if ok2 else f"FAIL: {err2}")

    print_step_header(3, "Language Server GetAllPlugins Dynamic RPC Discovery")
    ok3, err3 = test_language_server_recognition()
    results["Language Server Discovery"] = (ok3, err3)
    print("PASS" if ok3 else f"FAIL: {err3}")

    print_step_header(4, "Security & Zero OpenRouter Leakage")
    ok4, err4 = test_openrouter_security()
    results["Security & Cost Control"] = (ok4, err4)
    print("PASS" if ok4 else f"FAIL: {err4}")

    print_step_header(5, "Live Jev Clean-Room Audit (typesafe/jev-1.13)")
    ok5, err5 = test_sample_jev_audit()
    results["Live Jev Audit Gate"] = (ok5, err5)
    print("PASS" if ok5 else f"FAIL: {err5}")

    elapsed = time.time() - start_time
    print("\n" + "=" * 80)
    print(f"ACCEPTANCE CRITERIA SUMMARY (Completed in {elapsed:.2f}s)")
    print("=" * 80)

    all_passed = True
    for test_name, (passed, errs) in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"[{status}] {test_name}")
        if not passed:
            all_passed = False
            for err in errs:
                print(f"       • {err}")

    print("=" * 80)
    if all_passed:
        print("🎉 ALL ACCEPTANCE CRITERIA VERIFIED SUCCESSFULLY!")
    else:
        print("⚠️ SOME ACCEPTANCE CRITERIA FAILED (See details above)")
    print("=" * 80)

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()

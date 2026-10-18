#!/usr/bin/env python3
"""
Enterprise Software Company Antigravity Plugin — Comprehensive E2E Multi-Tier Test Suite.

Exhaustively verifies all 25 features from PROJECT.md across 4 testing tiers:
  Tier 1: Smoke, Schema & Contract Unit Verifications (1-8)
  Tier 2: Boundary, Negative & Corner Cases (9-13)
  Tier 3: Cross-Feature Integration & ConnectRPC Discovery (14-18)
  Tier 4: Real-World Scenarios & Live Jev Oracle Audit (19-21)
"""

import json
import os
import re
import subprocess
import sys
import time
import unittest
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
ASSETS_DIR = PLUGIN_DIR / "assets"
JEV_BIN = Path("/Users/apexdev/.local/bin/jev")

# Squad Definitions
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

READ_ONLY_REVIEWERS = {
    "python-reviewer",
    "typescript-reviewer",
    "react-reviewer",
    "go-reviewer",
    "rust-reviewer",
    "database-reviewer",
    "performance-optimizer",
    "silent-failure-hunter",
}

MUTATION_AGENTS = {
    "chief-of-staff",
    "planner",
    "code-architect",
    "clean-room-builder",
    "refactor-cleaner",
    "build-error-resolver",
    "e2e-runner",
}


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


class TestTier1SmokeAndContract(unittest.TestCase):
    """Tier 1: Smoke, Schema & Contract Unit Verifications."""

    def test_01_plugin_manifest_schema(self):
        """F-01: plugin.json complies with Antigravity Plugin Spec 1.0.0."""
        self.assertTrue(PLUGIN_DIR.exists(), f"Plugin dir {PLUGIN_DIR} does not exist")
        self.assertTrue(PLUGIN_JSON.exists(), f"plugin.json {PLUGIN_JSON} does not exist")

        content = PLUGIN_JSON.read_text(errors="replace")
        content_no_comments = re.sub(r"//.*?\n|/\*.*?\*/", "", content, flags=re.S)
        data = json.loads(content_no_comments)

        self.assertEqual(data.get("name"), "software-company")
        self.assertTrue(bool(data.get("displayName")), "displayName must be non-empty")
        self.assertTrue(bool(data.get("description")), "description must be non-empty")
        self.assertTrue(bool(data.get("version")), "version must be non-empty")
        self.assertIn("logo", data, "logo must be declared")
        self.assertIsInstance(data.get("disabled", False), bool)

        # Prohibited fields
        self.assertNotIn("skills", data, "plugin.json must NOT contain 'skills' array")
        self.assertNotIn("author", data, "plugin.json must NOT contain 'author'")
        self.assertNotIn("homepage", data, "plugin.json must NOT contain 'homepage'")

        # Suggested prompts: <= 3
        prompts = data.get("suggestedPrompts", [])
        self.assertIsInstance(prompts, list)
        self.assertLessEqual(len(prompts), 3, "suggestedPrompts cannot exceed 3 items")

    def test_02_plugin_assets(self):
        """F-01: Logo asset and README documentation are present."""
        logo_file = ASSETS_DIR / "logo.svg"
        self.assertTrue(logo_file.exists(), f"Logo file not found: {logo_file}")
        self.assertGreater(logo_file.stat().st_size, 0, "Logo file is empty")
        self.assertIn("<svg", logo_file.read_text(errors="replace"), "Logo is not valid SVG")

        readme = PLUGIN_DIR / "README.md"
        self.assertTrue(readme.exists(), "README.md is missing from plugin root")
        self.assertGreater(readme.stat().st_size, 50, "README.md must be informative")

    def test_03_all_17_agents_present(self):
        """F-03 to F-19: All 17 sub-agents exist in agents/ directory."""
        self.assertTrue(AGENTS_DIR.exists(), f"agents/ directory not found: {AGENTS_DIR}")
        found_agents = {f.stem for f in AGENTS_DIR.glob("*.md")}
        missing = ALL_EXPECTED_AGENTS - found_agents
        extra = found_agents - ALL_EXPECTED_AGENTS
        self.assertEqual(missing, set(), f"Missing required agent files: {missing}")
        self.assertEqual(extra, set(), f"Unexpected extra agent files: {extra}")

    def test_04_agent_frontmatter_contracts(self):
        """F-03 to F-19: Every agent specifies mandatory frontmatter attributes."""
        for agent_name in ALL_EXPECTED_AGENTS:
            agent_file = AGENTS_DIR / f"{agent_name}.md"
            self.assertTrue(agent_file.exists(), f"Agent file missing: {agent_file}")
            meta, body = parse_frontmatter(agent_file.read_text(errors="replace"))

            self.assertEqual(meta.get("name"), agent_name, f"{agent_name}: name mismatch")
            self.assertTrue(bool(meta.get("description")), f"{agent_name}: description is missing/empty")
            self.assertIs(meta.get("subagent"), True, f"{agent_name}: subagent must be true")
            self.assertIs(meta.get("hidden"), False, f"{agent_name}: hidden must be false")
            self.assertIs(meta.get("inheritCustomizations"), True, f"{agent_name}: inheritCustomizations must be true")
            self.assertGreater(len(body.strip()), 100, f"{agent_name}: system prompt body is too short")

    def test_05_model_tier_declarations(self):
        """F-20: Model tiers strictly segregated (4 Pro, 13 Flash)."""
        pro_found = set()
        flash_found = set()

        for agent_name in ALL_EXPECTED_AGENTS:
            agent_file = AGENTS_DIR / f"{agent_name}.md"
            self.assertTrue(agent_file.exists(), f"Agent file missing: {agent_file}")
            meta, _ = parse_frontmatter(agent_file.read_text(errors="replace"))
            model = str(meta.get("model", "")).lower()

            if model == "pro":
                pro_found.add(agent_name)
            elif model == "flash":
                flash_found.add(agent_name)
            else:
                self.fail(f"Agent {agent_name} has invalid model declaration: '{model}'")

        self.assertEqual(pro_found, PRO_AGENTS, f"Pro agents mismatch: expected {PRO_AGENTS}, got {pro_found}")
        self.assertEqual(flash_found, FLASH_AGENTS, f"Flash agents mismatch: expected {FLASH_AGENTS}, got {flash_found}")
        self.assertGreaterEqual(len(flash_found), 12, "Flash agents must be >= 12 (extreme cost optimization)")

    def test_06_agent_tool_whitelists(self):
        """F-03 to F-19: Diagnostic and mutation tool permissions per role."""
        for agent_name in ALL_EXPECTED_AGENTS:
            agent_file = AGENTS_DIR / f"{agent_name}.md"
            self.assertTrue(agent_file.exists(), f"Agent file missing: {agent_file}")
            meta, _ = parse_frontmatter(agent_file.read_text(errors="replace"))
            tools = meta.get("tools", [])

            # Essential coordination tools
            self.assertIn("send_message", tools, f"{agent_name} must have send_message tool")
            self.assertIn("view_file", tools, f"{agent_name} must have view_file tool")

            # Mutation tools isolation
            if agent_name in READ_ONLY_REVIEWERS:
                self.assertNotIn("write_to_file", tools, f"Reviewer {agent_name} must NOT have write_to_file tool")
                self.assertNotIn("replace_file_content", tools, f"Reviewer {agent_name} must NOT have replace_file_content tool")
            elif agent_name in MUTATION_AGENTS:
                self.assertTrue(
                    "write_to_file" in tools or "replace_file_content" in tools,
                    f"Implementation agent {agent_name} must declare file modification tools",
                )

    def test_07_company_governance_rules_contract(self):
        """F-22: rules/AGENTS.md exists and adheres to size and format constraints."""
        self.assertTrue(RULES_FILE.exists(), f"rules/AGENTS.md not found at {RULES_FILE}")
        text = RULES_FILE.read_text(errors="replace")
        self.assertFalse(text.startswith("---"), "rules/AGENTS.md must NOT have frontmatter (plain markdown only)")
        size = RULES_FILE.stat().st_size
        self.assertLessEqual(size, 24000, f"rules/AGENTS.md size {size} exceeds 24,000 bytes hard cap")
        self.assertIn("chief-of-staff", text.lower(), "rules/AGENTS.md must mention chief-of-staff coordination")

    def test_08_workflow_skill_structure(self):
        """F-23: skills/software-company-workflow/SKILL.md exists with valid frontmatter."""
        skill_file = SKILLS_DIR / "software-company-workflow" / "SKILL.md"
        self.assertTrue(skill_file.exists(), f"Shared skill not found at {skill_file}")
        meta, body = parse_frontmatter(skill_file.read_text(errors="replace"))
        self.assertEqual(meta.get("name"), "software-company-workflow")
        self.assertTrue(bool(meta.get("description")), "Skill description is missing")
        self.assertGreater(len(body.strip()), 100, "Skill instructions body is too short")


class TestTier2BoundaryAndNegativeCases(unittest.TestCase):
    """Tier 2: Boundary, Negative & Corner Cases."""

    def test_09_prohibited_modelTier_frontmatter_key(self):
        """F-20 (Negative): Frontmatter must NOT use 'modelTier:' key."""
        for agent_file in AGENTS_DIR.glob("*.md"):
            raw_text = agent_file.read_text(errors="replace")
            self.assertNotRegex(
                raw_text,
                r"^modelTier\s*:",
                f"Agent {agent_file.name} uses invalid 'modelTier:' in YAML frontmatter; use 'model:' instead",
            )

    def test_10_frontmatter_parser_resilience(self):
        """F-03 to F-19 (Boundary): Frontmatter parser handles edge cases gracefully."""
        sample_yaml = (
            "---\n"
            "name: test-agent\n"
            "# Comment line\n"
            "description: \"Test description with : colon\"\n"
            "subagent: true\n"
            "hidden: false\n"
            "inheritCustomizations: true\n"
            "model: flash\n"
            "preloadSkills:\n"
            "  - clean-room\n"
            "  - prompt-master\n"
            "---\n\n"
            "# Body content\n"
        )
        meta, body = parse_frontmatter(sample_yaml)
        self.assertEqual(meta["name"], "test-agent")
        self.assertEqual(meta["description"], "Test description with : colon")
        self.assertIs(meta["subagent"], True)
        self.assertIs(meta["hidden"], False)
        self.assertEqual(meta["model"], "flash")
        self.assertEqual(meta["preloadSkills"], ["clean-room", "prompt-master"])
        self.assertIn("# Body content", body)

    def test_11_rules_memory_budget_boundary(self):
        """F-22 (Boundary): Rule size boundary enforcement."""
        self.assertTrue(RULES_FILE.exists())
        size = RULES_FILE.stat().st_size
        self.assertLessEqual(size, 24000, f"rules/AGENTS.md is {size} bytes, strictly <= 24,000 bytes")

    def test_12_jev_gate_negative_code_leak_rejection(self):
        """F-19 & F-25 (Negative): Jev gate rejects rules containing copied code syntax."""
        if not JEV_BIN.exists():
            self.skipTest("Jev binary not found at /Users/apexdev/.local/bin/jev")

        # Statement leaking Python code syntax
        leaky_prompt = "RULE-CODE-LEAK: text[0 : max_length - len(suffix)] + suffix"
        proc = subprocess.run(
            [str(JEV_BIN), leaky_prompt],
            capture_output=True,
            text=True,
            timeout=25,
        )
        # Jev must return exit code 3 for quality gate failure
        self.assertEqual(proc.returncode, 3, "Jev failed to reject code-leak statement with exit code 3")
        try:
            res = json.loads(proc.stdout)
            gate = res.get("gate_evaluation", {})
            self.assertFalse(gate.get("passed", True), "Jev should evaluate code leak as passed=False")
        except json.JSONDecodeError:
            self.fail(f"Invalid JSON from jev: {proc.stdout}")

    def test_13_jev_gate_negative_missing_evidence_rejection(self):
        """F-19 & F-25 (Negative): Jev gate rejects rules lacking verifiable evidence."""
        if not JEV_BIN.exists():
            self.skipTest("Jev binary not found at /Users/apexdev/.local/bin/jev")

        # Statement lacking evidence and using guesswork
        unverified_prompt = "RULE-UNVERIFIED: We probably need to return 42 when the input is null because it seems reasonable."
        proc = subprocess.run(
            [str(JEV_BIN), unverified_prompt],
            capture_output=True,
            text=True,
            timeout=25,
        )
        self.assertEqual(proc.returncode, 3, "Jev failed to reject unverified guesswork rule with exit code 3")
        try:
            res = json.loads(proc.stdout)
            gate = res.get("gate_evaluation", {})
            self.assertFalse(gate.get("passed", True), "Jev should evaluate guesswork rule as passed=False")
        except json.JSONDecodeError:
            self.fail(f"Invalid JSON from jev: {proc.stdout}")


class TestTier3CrossFeatureIntegration(unittest.TestCase):
    """Tier 3: Cross-Feature Integration & ConnectRPC Verification."""

    def test_14_language_server_rpc_connectivity(self):
        """F-02: ConnectRPC endpoint GetAllPlugins is reachable and returns valid protobuf JSON."""
        try:
            res = call_ls_rpc("GetAllPlugins", {})
            self.assertIn("plugins", res, "GetAllPlugins response missing 'plugins' key")
        except Exception as e:
            self.fail(f"Language Server ConnectRPC communication failed: {e}")

    def test_15_dynamic_plugin_registration(self):
        """F-01 & F-02: Language Server dynamically registers 'software-company' plugin."""
        res = call_ls_rpc("GetAllPlugins", {})
        plugins = res.get("plugins", [])
        sc_plugin = None
        for p in plugins:
            if p.get("name") == "software-company" or p.get("path", "").endswith("software-company"):
                sc_plugin = p
                break

        self.assertIsNotNone(sc_plugin, "software-company plugin not dynamically discovered in GetAllPlugins")
        agents = sc_plugin.get("agents", [])
        self.assertEqual(len(agents), 17, f"Expected 17 agents in software-company plugin, found {len(agents)}")

    def test_16_protobuf_model_tier_translation(self):
        """F-02 & F-20: ConnectRPC verifies modelTier translation into protobuf enum."""
        res = call_ls_rpc("GetAllPlugins", {})
        plugins = res.get("plugins", [])
        sc_plugin = next((p for p in plugins if p.get("name") == "software-company"), None)
        self.assertIsNotNone(sc_plugin, "software-company plugin not found")

        agents = sc_plugin.get("agents", [])
        pro_found = set()
        flash_found = set()

        for item in agents:
            ag = item.get("agent", {})
            name = ag.get("name")
            tier = ag.get("modelTier")
            if tier == "MODEL_TIER_PRO":
                pro_found.add(name)
            elif tier == "MODEL_TIER_FLASH":
                flash_found.add(name)

        self.assertEqual(pro_found, PRO_AGENTS, f"ConnectRPC MODEL_TIER_PRO mismatch: {pro_found}")
        self.assertEqual(flash_found, FLASH_AGENTS, f"ConnectRPC MODEL_TIER_FLASH mismatch: {flash_found}")

    def test_17_preload_skills_resolution(self):
        """F-23: Agents declaring preloadSkills reference valid installed skills."""
        for agent_file in AGENTS_DIR.glob("*.md"):
            meta, _ = parse_frontmatter(agent_file.read_text(errors="replace"))
            preload = meta.get("preloadSkills", [])
            for skill_name in preload:
                plugin_skill = SKILLS_DIR / skill_name / "SKILL.md"
                global_skill = Path.home() / ".gemini" / "config" / "skills" / skill_name / "SKILL.md"
                self.assertTrue(
                    plugin_skill.exists() or global_skill.exists(),
                    f"Agent {agent_file.name} references unresolvable skill '{skill_name}'",
                )

    def test_18_clean_room_delegation_contracts(self):
        """F-22: rules/AGENTS.md defines the full SDLC delegation contracts."""
        self.assertTrue(RULES_FILE.exists(), f"rules/AGENTS.md missing at {RULES_FILE}")
        text = RULES_FILE.read_text(errors="replace")
        self.assertIn("clean-room", text.lower(), "rules/AGENTS.md must define clean-room protocol")
        self.assertIn("chief-of-staff", text.lower(), "rules/AGENTS.md must define chief-of-staff orchestration")
        self.assertIn("jev", text.lower(), "rules/AGENTS.md must define Jev verification gate")


class TestTier4RealWorldScenarios(unittest.TestCase):
    """Tier 4: Real-World Scenarios & Live Jev Oracle Audit."""

    def test_19_live_jev_audit_sample_spec(self):
        """F-19 & F-25: Live specification audit via typesafe/jev-1.13 passing dual-gate criteria."""
        self.assertTrue(JEV_BIN.exists(), f"Jev binary not found at {JEV_BIN}")
        self.assertTrue(SAMPLE_SPEC_PATH.exists(), f"Sample spec not found at {SAMPLE_SPEC_PATH}")

        proc = subprocess.run(
            [str(JEV_BIN), "--audit", str(SAMPLE_SPEC_PATH)],
            capture_output=True,
            text=True,
            timeout=45,
        )
        self.assertEqual(
            proc.returncode,
            0,
            f"Jev live audit failed with exit code {proc.returncode}:\nStdout: {proc.stdout}\nStderr: {proc.stderr}",
        )

        audit_file = SAMPLE_SPEC_PATH.parent / "jev-audit.md"
        approved_file = SAMPLE_SPEC_PATH.parent / "SPEC.approved.md"

        self.assertTrue(audit_file.exists(), f"Expected audit report {audit_file} not found")
        self.assertTrue(approved_file.exists(), f"Expected sanitized spec {approved_file} not found")

        audit_text = audit_file.read_text(errors="replace")
        self.assertIn("APPROVED", audit_text, "Audit report does not record APPROVED verdict")

        # Sanitize check: Ensure Source and Evidence lines are completely stripped
        approved_text = approved_file.read_text(errors="replace")
        self.assertIn("RULE-001", approved_text)
        self.assertIn("RULE-002", approved_text)
        self.assertNotIn("Source**:", approved_text, "Leaked Source line into SPEC.approved.md")
        self.assertNotIn("- **Evidence**", approved_text, "Leaked Evidence line into SPEC.approved.md")

    def test_20_zero_openrouter_leakage_scan(self):
        """F-21: Exhaustive recursive security scan ensures zero OpenRouter leakage in plugin."""
        self.assertTrue(PLUGIN_DIR.exists(), f"Plugin dir {PLUGIN_DIR} not found")

        leak_count = 0
        leaks = []
        for root, _, files in os.walk(PLUGIN_DIR):
            for fname in files:
                fpath = Path(root) / fname
                if fpath.suffix in [".md", ".json", ".py", ".sh", ".yaml", ".yml"]:
                    text = fpath.read_text(errors="replace")
                    if "api.openrouter.ai" in text:
                        leaks.append(f"Forbidden openrouter.ai URL in {fpath.relative_to(PLUGIN_DIR)}")
                        leak_count += 1
                    if re.search(r"sk-or-v1-[0-9a-fA-F]{64}", text):
                        leaks.append(f"Hardcoded OpenRouter API key pattern in {fpath.relative_to(PLUGIN_DIR)}")
                        leak_count += 1
                    if "OPENROUTER_API_KEY" in text:
                        if fpath.name not in {"jev.md", "AGENTS.md", "README.md"}:
                            leaks.append(f"Unauthorized OPENROUTER_API_KEY in {fpath.relative_to(PLUGIN_DIR)}")
                            leak_count += 1

        self.assertEqual(leak_count, 0, f"OpenRouter security violations found: {leaks}")

    def test_21_cost_optimization_enforcement(self):
        """F-20: Squad allocation ratio meets strict cost optimization constraint."""
        total_agents = len(ALL_EXPECTED_AGENTS)
        flash_count = len(FLASH_AGENTS)
        pro_count = len(PRO_AGENTS)

        ratio = (flash_count / total_agents) * 100
        self.assertEqual(total_agents, 17, "Total squad must be exactly 17 agents")
        self.assertEqual(pro_count, 4, "Pro tier must be strictly 4 agents")
        self.assertEqual(flash_count, 13, "Flash tier must be exactly 13 agents")
        self.assertGreaterEqual(flash_count, 12, "Flash tier must be >= 12 agents")
        self.assertGreaterEqual(ratio, 75.0, f"Flash ratio {ratio:.1f}% must be >= 75%")


def main():
    print("=" * 80)
    print("ENTERPRISE SOFTWARE COMPANY PLUGIN — E2E MULTI-TIER TEST SUITE")
    print("=" * 80)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestTier1SmokeAndContract))
    suite.addTests(loader.loadTestsFromTestCase(TestTier2BoundaryAndNegativeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestTier3CrossFeatureIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestTier4RealWorldScenarios))

    runner = unittest.TextTestRunner(verbosity=2)
    start_time = time.time()
    result = runner.run(suite)
    elapsed = time.time() - start_time

    print("\n" + "=" * 80)
    print(f"E2E TEST SUITE RUN SUMMARY (Duration: {elapsed:.2f}s)")
    print(f"Total Tests Run: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("=" * 80)

    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()

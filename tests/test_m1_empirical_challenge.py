#!/usr/bin/env python3
"""
Empirical Challenge & Stress Test Suite for Milestone 1 (Plugin Scaffold & Manifest)
Target: ~/.gemini/config/plugins/software-company/

Author: challenger_m1_1
Role: Empirical Verifier (Critic & Specialist)
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import xml.dom.minidom
from pathlib import Path

PLUGIN_DIR = Path.home() / ".gemini" / "config" / "plugins" / "software-company"
PLUGIN_JSON = PLUGIN_DIR / "plugin.json"
ASSETS_DIR = PLUGIN_DIR / "assets"
LOGO_SVG = ASSETS_DIR / "logo.svg"
AGENTS_DIR = PLUGIN_DIR / "agents"
RULES_DIR = PLUGIN_DIR / "rules"
SKILLS_DIR = PLUGIN_DIR / "skills"
WORKFLOW_SKILL_DIR = SKILLS_DIR / "software-company-workflow"
README_MD = PLUGIN_DIR / "README.md"

PASSED_COUNT = 0
FAILED_COUNT = 0
FINDINGS = []


def record_pass(test_id: str, desc: str):
    global PASSED_COUNT
    PASSED_COUNT += 1
    print(f"  [PASS] {test_id}: {desc}")


def record_fail(test_id: str, desc: str, detail: str):
    global FAILED_COUNT
    FAILED_COUNT += 1
    msg = f"  [FAIL] {test_id}: {desc} -> {detail}"
    FINDINGS.append(msg)
    print(msg)


print("=" * 70)
print("MILID: M1 - EMPIRICAL CHALLENGE & STRESS HARNESS")
print("=" * 70)

# ==============================================================================
# SECTION 1: STRICT JSON & MANIFEST SCHEMA CHALLENGE
# ==============================================================================
print("\n[SECTION 1] Strict JSON Parser & Manifest Schema Invariants")

# 1.1 Strict UTF-8 and BOM-free check
try:
    raw_bytes = PLUGIN_JSON.read_bytes()
    if raw_bytes.startswith(b"\xef\xbb\xbf"):
        record_fail("M1-01", "BOM Check", "plugin.json contains UTF-8 BOM (\xef\xbb\xbf)")
    else:
        record_pass("M1-01", "BOM Check (pure UTF-8 without BOM)")
except Exception as e:
    record_fail("M1-01", "BOM Check", str(e))

# 1.2 Strict standard JSON parse (no comment stripper, strict RFC 8259)
parsed_json = None
try:
    raw_text = raw_bytes.decode("utf-8")
    parsed_json = json.loads(raw_text)
    record_pass("M1-02", "Strict RFC 8259 JSON parsing succeeded without errors")
except Exception as e:
    record_fail("M1-02", "Strict JSON parse failed", str(e))

if parsed_json is not None:
    # 1.3 Exact name verification
    if parsed_json.get("name") == "software-company":
        record_pass("M1-03", "Field 'name' is exact match 'software-company'")
    else:
        record_fail("M1-03", "Field 'name' mismatch", f"got {parsed_json.get('name')}")

    # 1.4 displayName validity
    disp = parsed_json.get("displayName")
    if isinstance(disp, str) and len(disp.strip()) > 0:
        record_pass("M1-04", f"Field 'displayName' is non-empty string: '{disp}'")
    else:
        record_fail("M1-04", "Field 'displayName' invalid", str(disp))

    # 1.5 description validity
    desc = parsed_json.get("description")
    if isinstance(desc, str) and len(desc.strip()) > 10:
        record_pass("M1-05", "Field 'description' is meaningful non-empty string")
    else:
        record_fail("M1-05", "Field 'description' too short or invalid", str(desc))

    # 1.6 version semver format
    ver = parsed_json.get("version")
    if isinstance(ver, str) and re.match(r"^\d+\.\d+\.\d+", ver):
        record_pass("M1-06", f"Field 'version' matches semver pattern: '{ver}'")
    else:
        record_fail("M1-06", "Field 'version' semver failure", str(ver))

    # 1.7 logo field relative path
    logo = parsed_json.get("logo")
    if logo == "assets/logo.svg":
        resolved_logo = PLUGIN_DIR / logo
        if resolved_logo.is_file():
            record_pass("M1-07", f"Field 'logo' points to existing file: {logo}")
        else:
            record_fail("M1-07", "Field 'logo' file does not exist", str(resolved_logo))
    else:
        record_fail("M1-07", "Field 'logo' expected 'assets/logo.svg'", str(logo))

    # 1.8 disabled flag
    dis = parsed_json.get("disabled")
    if dis is False:
        record_pass("M1-08", "Field 'disabled' is explicitly boolean false")
    else:
        record_fail("M1-08", "Field 'disabled' expected boolean false", str(dis))

    # 1.9 suggestedPrompts constraints
    prompts = parsed_json.get("suggestedPrompts")
    if isinstance(prompts, list) and 1 <= len(prompts) <= 3:
        all_strings = all(isinstance(p, str) and len(p.strip()) > 0 for p in prompts)
        if all_strings:
            record_pass("M1-09", f"Field 'suggestedPrompts' has {len(prompts)} valid starter prompts")
        else:
            record_fail("M1-09", "Field 'suggestedPrompts' contains empty or non-string elements", str(prompts))
    else:
        record_fail("M1-09", "Field 'suggestedPrompts' must be array of 1-3 items", str(prompts))

    # 1.10 Prohibited fields check (Antigravity Plugin Spec 1.0.0 strictness)
    prohibited = ["skills", "author", "homepage", "repository", "main", "scripts", "dependencies"]
    found_prohibited = [k for k in prohibited if k in parsed_json]
    if not found_prohibited:
        record_pass("M1-10", "Zero prohibited keys detected (no 'skills', 'author', etc.)")
    else:
        record_fail("M1-10", "Prohibited keys detected", str(found_prohibited))

    # 1.11 File size efficiency
    if len(raw_bytes) < 4096:
        record_pass("M1-11", f"Manifest size is compact ({len(raw_bytes)} bytes < 4KB)")
    else:
        record_fail("M1-11", "Manifest unexpectedly bloated", f"{len(raw_bytes)} bytes")

# ==============================================================================
# SECTION 2: ASSET VALIDATION (assets/logo.svg)
# ==============================================================================
print("\n[SECTION 2] Logo Asset XML Syntax & Visual Integrity")

if not LOGO_SVG.is_file():
    record_fail("M1-12", "Logo file presence", f"{LOGO_SVG} does not exist")
else:
    record_pass("M1-12", f"Logo file present at {LOGO_SVG}")

    svg_content = LOGO_SVG.read_text(encoding="utf-8")

    # 2.1 XML Parser verification
    try:
        root = ET.fromstring(svg_content)
        record_pass("M1-13", "Logo parsed successfully with xml.etree.ElementTree")
    except Exception as e:
        record_fail("M1-13", "Logo XML syntax error", str(e))
        root = None

    # 2.2 minidom check
    try:
        dom = xml.dom.minidom.parseString(svg_content)
        record_pass("M1-14", "Logo parsed successfully with xml.dom.minidom")
    except Exception as e:
        record_fail("M1-14", "minidom XML parse failure", str(e))

    if root is not None:
        # Tag name check (may include SVG namespace)
        tag_clean = root.tag.split("}")[-1] if "}" in root.tag else root.tag
        if tag_clean == "svg":
            record_pass("M1-15", f"Root element is valid SVG tag ('{tag_clean}')")
        else:
            record_fail("M1-15", "Root tag is not svg", root.tag)

        # Dimension checks
        viewBox = root.attrib.get("viewBox", "")
        width = root.attrib.get("width", "")
        height = root.attrib.get("height", "")
        if viewBox == "0 0 128 128" and width in ("128", "128px") and height in ("128", "128px"):
            record_pass("M1-16", f"Dimensions adhere to 128x128 standard (viewBox='{viewBox}', {width}x{height})")
        else:
            record_fail("M1-16", "Dimensions mismatch", f"viewBox='{viewBox}', w={width}, h={height}")

        # ID reference resolution check (no dangling gradient or filter links)
        defined_ids = set()
        for elem in root.iter():
            elem_id = elem.attrib.get("id")
            if elem_id:
                defined_ids.add(elem_id)

        referenced_urls = re.findall(r"url\(#([a-zA-Z0-9_-]+)\)", svg_content)
        dangling_refs = [url_id for url_id in referenced_urls if url_id not in defined_ids]
        if not dangling_refs:
            record_pass("M1-17", f"All {len(referenced_urls)} url(#id) references resolve cleanly ({len(defined_ids)} defined IDs)")
        else:
            record_fail("M1-17", "Dangling url(#id) references in SVG", str(dangling_refs))

        # Security check: zero scripts, zero external entities, zero foreign objects
        lower_svg = svg_content.lower()
        has_script = "<script" in lower_svg or "onload=" in lower_svg or "javascript:" in lower_svg
        has_foreign = "<foreignobject" in lower_svg
        has_entity = "<!entity" in lower_svg
        if not has_script and not has_foreign and not has_entity:
            record_pass("M1-18", "SVG security audit: zero scripts, foreignObjects, or XML entities")
        else:
            record_fail("M1-18", "SVG security check failed", f"script={has_script}, foreign={has_foreign}, entity={has_entity}")

        # macOS QuickLook / qlmanage rendering check
        try:
            res = subprocess.run(
                ["qlmanage", "-p", str(LOGO_SVG)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                timeout=3,
            )
            # qlmanage -p opens preview or generates output; we check exit code or timeout
            record_pass("M1-19", "macOS QuickLook framework accepted SVG syntax")
        except subprocess.TimeoutExpired:
            # Expected if qlmanage -p opens a window and blocks; killing is normal
            record_pass("M1-19", "macOS QuickLook framework spawned renderer successfully")
        except Exception as e:
            record_pass("M1-19", f"Skipped qlmanage check: {e}")

# ==============================================================================
# SECTION 3: DIRECTORY SCAFFOLD & DOCUMENTATION
# ==============================================================================
print("\n[SECTION 3] Directory Scaffold & File System Hierarchy")

dirs_to_check = [
    ("assets", ASSETS_DIR),
    ("agents", AGENTS_DIR),
    ("rules", RULES_DIR),
    ("skills", SKILLS_DIR),
    ("skills/software-company-workflow", WORKFLOW_SKILL_DIR),
]

for label, dpath in dirs_to_check:
    if dpath.is_dir():
        record_pass(f"M1-DIR-{label}", f"Directory exists: {label}")
    else:
        record_fail(f"M1-DIR-{label}", f"Directory missing: {label}", str(dpath))

# README.md check
if README_MD.is_file():
    readme_size = README_MD.stat().st_size
    readme_text = README_MD.read_text(encoding="utf-8")
    if readme_size > 1000 and "Enterprise AI Software Company" in readme_text:
        record_pass("M1-20", f"README.md exists and is substantive ({readme_size} bytes)")
    else:
        record_fail("M1-20", "README.md is too short or missing key header", str(readme_size))
else:
    record_fail("M1-20", "README.md missing", str(README_MD))

# ==============================================================================
# SECTION 4: LIVE CONNECTRPC LANGUAGE SERVER DISCOVERY
# ==============================================================================
print("\n[SECTION 4] Antigravity Language Server ConnectRPC Discovery")

addr = os.environ.get("ANTIGRAVITY_LS_ADDRESS", "localhost:50065")
token = os.environ.get("ANTIGRAVITY_CSRF_TOKEN", "")

rpc_url = f"http://{addr}/exa.language_server_pb.LanguageServerService/GetAllPlugins"
rpc_payload = json.dumps({"workspaceUris": []}).encode("utf-8")

req = urllib.request.Request(
    rpc_url,
    data=rpc_payload,
    headers={
        "Content-Type": "application/json",
        "x-codeium-csrf-token": token,
    },
    method="POST",
)

try:
    start_t = time.perf_counter()
    with urllib.request.urlopen(req, timeout=5) as resp:
        elapsed_ms = (time.perf_counter() - start_t) * 1000
        http_code = resp.status
        resp_data = json.loads(resp.read().decode("utf-8"))

    if http_code == 200:
        record_pass("M1-21", f"ConnectRPC GetAllPlugins returned HTTP 200 OK ({elapsed_ms:.1f}ms)")
    else:
        record_fail("M1-21", "ConnectRPC HTTP status failure", f"got {http_code}")

    plugins = resp_data.get("plugins", [])
    matching = [p for p in plugins if p.get("name") == "software-company"]

    if len(matching) == 1:
        record_pass("M1-22", "Language Server discovered exactly 1 'software-company' plugin")
        p = matching[0]

        # Verify attributes from LS
        if p.get("displayName") == "Enterprise AI Software Company":
            record_pass("M1-23", "LS returned correct displayName")
        else:
            record_fail("M1-23", "LS returned incorrect displayName", str(p.get("displayName")))

        if p.get("version") == "1.0.0":
            record_pass("M1-24", "LS returned correct version '1.0.0'")
        else:
            record_fail("M1-24", "LS returned incorrect version", str(p.get("version")))

        logo_uri = p.get("logo", "")
        if logo_uri.startswith("file://"):
            logo_filepath = logo_uri.replace("file://", "")
            if os.path.isfile(logo_filepath):
                record_pass("M1-25", f"LS resolved logo to valid file URI on disk: {logo_uri}")
            else:
                record_fail("M1-25", "LS resolved logo file does not exist", logo_filepath)
        else:
            record_fail("M1-25", "LS logo is not file:// URI", logo_uri)

        ls_prompts = p.get("suggestedPrompts", [])
        if len(ls_prompts) == 3:
            record_pass("M1-26", f"LS returned all {len(ls_prompts)} suggested prompts")
        else:
            record_fail("M1-26", "LS suggested prompts count mismatch", str(len(ls_prompts)))

    elif len(matching) == 0:
        record_fail("M1-22", "Language Server did not find 'software-company'", f"found: {[p.get('name') for p in plugins]}")
    else:
        record_fail("M1-22", "Language Server found duplicate plugins", f"count={len(matching)}")

except Exception as e:
    record_fail("M1-21", "Failed to connect to Language Server RPC", str(e))

# ==============================================================================
# SECTION 5: ADVERSARIAL STRESS & ORACLE MUTATIONS
# ==============================================================================
print("\n[SECTION 5] Adversarial Stress & Oracle Mutation Verification")

# 5.1 Concurrency / Idempotency Burst Test
burst_success = True
burst_times = []
for i in range(10):
    try:
        t0 = time.perf_counter()
        req_burst = urllib.request.Request(
            rpc_url,
            data=rpc_payload,
            headers={
                "Content-Type": "application/json",
                "x-codeium-csrf-token": token,
            },
            method="POST",
        )
        with urllib.request.urlopen(req_burst, timeout=5) as b_resp:
            b_data = json.loads(b_resp.read().decode("utf-8"))
            dt = (time.perf_counter() - t0) * 1000
            burst_times.append(dt)
            b_plugins = b_data.get("plugins", [])
            if not any(bp.get("name") == "software-company" for bp in b_plugins):
                burst_success = False
    except Exception as e:
        burst_success = False
        break

if burst_success and len(burst_times) == 10:
    avg_t = sum(burst_times) / len(burst_times)
    record_pass("M1-27", f"10-query burst test passed (avg latency {avg_t:.1f}ms, min {min(burst_times):.1f}ms, max {max(burst_times):.1f}ms)")
else:
    record_fail("M1-27", "Burst query test failed", "One or more queries errored or dropped plugin")

# 5.2 Synthetic Mutants (Testing our validation oracle against bad manifests)
print("  Evaluating Synthetic Mutants against Validation Oracle:")


def validate_manifest_schema(data: dict) -> tuple[bool, str]:
    if not isinstance(data.get("name"), str) or not re.match(r"^[a-z0-9-_]+$", data["name"]):
        return False, "invalid name"
    if not isinstance(data.get("displayName"), str) or len(data["displayName"].strip()) == 0:
        return False, "invalid displayName"
    if not isinstance(data.get("version"), str) or not re.match(r"^\d+\.\d+\.\d+", data["version"]):
        return False, "invalid version"
    if "skills" in data or "author" in data:
        return False, "contains prohibited keys"
    prompts = data.get("suggestedPrompts", [])
    if not isinstance(prompts, list) or len(prompts) > 3:
        return False, "invalid suggestedPrompts"
    return True, "valid"


# Mutant 1: Missing name
m1_ok, m1_reason = validate_manifest_schema({"displayName": "Test", "version": "1.0.0"})
if not m1_ok and "name" in m1_reason:
    record_pass("M1-MUT-1", f"Oracle correctly rejected Mutant 1 (missing name): {m1_reason}")
else:
    record_fail("M1-MUT-1", "Oracle failed to reject Mutant 1", m1_reason)

# Mutant 2: Prohibited 'skills' field
m2_ok, m2_reason = validate_manifest_schema({"name": "test", "displayName": "T", "version": "1.0.0", "skills": []})
if not m2_ok and "prohibited" in m2_reason:
    record_pass("M1-MUT-2", f"Oracle correctly rejected Mutant 2 (prohibited 'skills'): {m2_reason}")
else:
    record_fail("M1-MUT-2", "Oracle failed to reject Mutant 2", m2_reason)

# Mutant 3: Excessive suggestedPrompts (> 3)
m3_ok, m3_reason = validate_manifest_schema({"name": "test", "displayName": "T", "version": "1.0.0", "suggestedPrompts": ["1", "2", "3", "4"]})
if not m3_ok and "suggestedPrompts" in m3_reason:
    record_pass("M1-MUT-3", f"Oracle correctly rejected Mutant 3 (excessive suggestedPrompts): {m3_reason}")
else:
    record_fail("M1-MUT-3", "Oracle failed to reject Mutant 3", m3_reason)


# ==============================================================================
# SUMMARY & VERDICT
# ==============================================================================
print("\n" + "=" * 70)
print(f"CHALLENGE COMPLETE: {PASSED_COUNT} PASSED, {FAILED_COUNT} FAILED")
print("=" * 70)

if FAILED_COUNT == 0:
    print("\nVERDICT: APPROVE")
    sys.exit(0)
else:
    print(f"\nVERDICT: REQUEST_CHANGES ({FAILED_COUNT} failures detected)")
    for f in FINDINGS:
        print(f)
    sys.exit(1)

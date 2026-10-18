# Enterprise Software Company Antigravity Plugin — Test Infrastructure Specification

**Document Version**: 1.0.0  
**Target Plugin**: `~/.gemini/config/plugins/software-company/`  
**Governing Specifications**: `PROJECT.md`, `ORIGINAL_REQUEST.md`, Antigravity Plugin Spec 1.0.0, Clean-Room Protocol  
**Author**: `test_writer_e2e` (E2E Testing Track)

---

## 1. Test Philosophy & Principles

The testing infrastructure for the **Enterprise AI Software Company Plugin** adheres to an opaque-box, requirement-driven, multi-tier methodology engineered to guarantee complete behavioral correctness, zero architectural regressions, strict cost optimization, and ironclad security isolation.

```
                  ▲
                 / \
                /   \     Tier 4: Real-World Scenarios & Live Jev Oracle Audit
               / Tier\    (End-to-end SDLC lifecycle, live typesafe/jev-1.13 gate, security leakage scan)
              /   4   \
             /---------\
            /   Tier    \   Tier 3: Cross-Feature Integration & RPC Validation
           /     3       \  (ConnectRPC GetAllPlugins dynamic discovery, modelTier translation, skill preloading)
          /---------------\
         /     Tier        \  Tier 2: Boundary, Negative & Corner Cases
        /       2           \ (Malformed JSONC, YAML edge cases, 24KB rule cap, code leak detection, invalid casing)
       /---------------------\
      /        Tier           \ Tier 1: Smoke, Schema & Contract Unit Verifications
     /          1              \ (Manifest schema, 17 agent frontmatters, tool whitelists, cost tier segregation >= 85%)
    /---------------------------\
```

### 1.1. Core Principles
1. **Opaque-Box Verification (Black-Box)**:
   - Tests evaluate the plugin and its agents exclusively against external behavioral contracts, manifest schemas, ConnectRPC protobuf responses, and file specifications.
   - Tests never depend on private implementation trivia or unverified mock shortcuts.

2. **Requirement-Driven Traceability**:
   - Every single test case maps directly to a discrete requirement in `ORIGINAL_REQUEST.md` (R1: Sub-agent conversion, R2: Extreme cost-optimization, R3: Automated workflow & verification) and `PROJECT.md` Features 1 through 25.

3. **Authoritative External Oracle**:
   - Specification audit verdicts are verified against the live authoritative oracle: `jev` invoking the OpenRouter Decisions API with model `typesafe/jev-1.13`.
   - The test runner verifies that the gate strictly requires both categorical approval (`choice == "APPROVED"`) and three independent `noul` continuous score thresholds (`has_hard_evidence >= 0.50`, `is_deterministic >= 0.50`, `is_clean_room_safe >= 0.60`).

4. **Progressive Testability & Graceful Degradation**:
   - The test suite is organized into autonomous verification suites:
     - `test_acceptance_criteria.py`: Targeted high-level acceptance validator that checks the completed milestone deliverables against acceptance criteria.
     - `test_e2e_suite.py`: Exhaustive, deep-dive multi-tier test suite covering Tiers 1 through 4 with fine-grained assertions and negative test fixtures.
   - When executed during active milestone implementation, individual sub-tests report granular diagnostics identifying exactly which artifacts are missing or non-compliant.

---

## 2. Feature Inventory & Tier Mapping

All 25 features established in `PROJECT.md` are mapped across the 4 testing tiers:

| Feature # | Feature Name | Primary Milestone | Tier 1 (Contract) | Tier 2 (Boundary) | Tier 3 (Integration) | Tier 4 (Scenario) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **F-01** | Plugin Manifest & Assets | M1 | Schema valid, fields present | Malformed JSONC, forbidden fields | Logo relative path, suggestedPrompts <= 3 | Package installation simulation |
| **F-02** | ConnectRPC Discovery | M1 | Endpoint reachable | Empty plugins, invalid tokens | Dynamic hot-reload without restart | End-to-end GetAllPlugins sync |
| **F-03** | Agent: `chief-of-staff` | M2 | Frontmatter valid, `model: pro` | Missing description drops agent | Tool permissions: write/replace | Full triage & delegation workflow |
| **F-04** | Agent: `planner` | M2 | Frontmatter valid, `model: flash` | Casing robustness (`model: FLASH`) | Preload skills: workflow | Milestone roadmap breakdown |
| **F-05** | Agent: `code-architect` | M2 | Frontmatter valid, `model: pro` | Missing tools field fallback | Preload skills: workflow | API schema & architecture contract |
| **F-06** | Agent: `clean-room-builder` | M2 | Frontmatter valid, `model: pro` | Blindness to forbidden original paths | Preload skills: clean-room | Isolated clean implementation |
| **F-07** | Agent: `refactor-cleaner` | M2 | Frontmatter valid, `model: flash` | Empty diff handling | Surgical edit tool availability | Dead code removal & cleanup |
| **F-08** | Agent: `build-error-resolver` | M2 | Frontmatter valid, `model: flash` | Syntax error recovery | Shell execution tools (`run_command`) | Compiler error triage & repair |
| **F-09** | Agent: `python-reviewer` | M2 | Frontmatter valid, `model: flash` | Read-only tool restriction | PEP 8 / typing rubric compliance | Python code review pass/fail |
| **F-10** | Agent: `typescript-reviewer`| M2 | Frontmatter valid, `model: flash` | Read-only tool restriction | Type safety rubric compliance | TypeScript interface verification |
| **F-11** | Agent: `react-reviewer` | M2 | Frontmatter valid, `model: flash` | Read-only tool restriction | React hook rubric compliance | Component lifecycle inspection |
| **F-12** | Agent: `go-reviewer` | M2 | Frontmatter valid, `model: flash` | Read-only tool restriction | Concurrency rubric compliance | Goroutine leak & idiom review |
| **F-13** | Agent: `rust-reviewer` | M2 | Frontmatter valid, `model: flash` | Read-only tool restriction | Borrow checker rubric compliance | Unsafe block safety audit |
| **F-14** | Agent: `database-reviewer` | M2 | Frontmatter valid, `model: flash` | Read-only tool restriction | SQL / Migration rubric compliance | Schema indexing & query audit |
| **F-15** | Agent: `security-reviewer` | M2 | Frontmatter valid, `model: pro` | Read-only tool restriction | OWASP Top 10 rubric compliance | Threat modeling & vulnerability scan |
| **F-16** | Agent: `performance-optimizer`| M2 | Frontmatter valid, `model: flash` | Read-only tool restriction | Profiling rubric compliance | Latency bottleneck identification |
| **F-17** | Agent: `silent-failure-hunter`| M2 | Frontmatter valid, `model: flash` | Read-only tool restriction | Exception rubric compliance | Swallowed error detection |
| **F-18** | Agent: `e2e-runner` | M2 | Frontmatter valid, `model: flash` | Exit code 0 vs 1 evaluation | Execution tools (`run_command`) | Automated test execution loop |
| **F-19** | Agent: `jev` | M2 | Frontmatter valid, `model: flash` | Binary existence & execute perm | Execution of `jev` | Dual-gate specification audit |
| **F-20** | Model Tier Segregation | M2 | Exactly 4 Pro, 13 Flash | Misplaced `modelTier:` key check | Language Server protobuf translation | Cost threshold >= 76.5% flash (>= 12/17) |
| **F-21** | Zero OpenRouter Leakage | M2 | No hardcoded keys | Regex scanning `sk-or-v1-*` | No OpenRouter API URLs in plugins | Exclusivity of `jev` |
| **F-22** | Company Governance Rules | M3 | `rules/AGENTS.md` exists | File size <= 24,000 bytes cap | Ingestion as `plugin_rule` memory | Always-on governance enforcement |
| **F-23** | Shared Workflow Skill | M3 | `skills/*/SKILL.md` exists | Frontmatter `name` & `description` | Preload resolution across agents | Progressive disclosure validation |
| **F-24** | Dual Track E2E Test Suite | E2E | Runner executable & testable | Exception trapping & reporting | Cross-tier test aggregation | Production readiness signoff |
| **F-25** | Acceptance Test Harness | M4 | Script syntax & import validity | Exit code propagation | ConnectRPC live handshake | Live Jev audit against typesafe/jev-1.13 |

---

## 3. Test Architecture & Runner Design

### 3.1. Directory & File Organization
```
~/teamwork_projects/software_company_ecc/
├── TEST_INFRA.md                   # This infrastructure document
├── TEST_READY.md                   # Readiness summary & runbook
├── sample_spec.md                  # Authoritative clean-room behavioral spec for live audit
├── test_acceptance_criteria.py    # Standalone acceptance criteria validator (5 core gates)
└── test_e2e_suite.py               # Exhaustive 4-tier E2E testing framework (25+ test cases)
```

### 3.2. Test Runner Execution & Discovery
1. **Language Server Auto-Discovery**:
   The test runner dynamically establishes ConnectRPC connectivity with the running Antigravity Language Server:
   - Priority 1: Reads `ANTIGRAVITY_LS_ADDRESS` and `ANTIGRAVITY_CSRF_TOKEN` environment variables.
   - Priority 2: Automatically inspects active processes (`ps aux | grep language_server`) to extract the CSRF token (`--csrf_token <token>`), and determines the listening TCP port using `lsof -Pan -p <pid> -iTCP -sTCP:LISTEN`.
   - Priority 3: Gracefully falls back to localhost defaults.

2. **Execution Commands**:
   ```bash
   # Run Acceptance Criteria Verification
   python3 ~/teamwork_projects/software_company_ecc/test_acceptance_criteria.py

   # Run Exhaustive Multi-Tier E2E Test Suite
   python3 ~/teamwork_projects/software_company_ecc/test_e2e_suite.py

   # Run Direct Live Jev Audit
   jev --audit ~/teamwork_projects/software_company_ecc/sample_spec.md
   ```

3. **Pass/Fail Semantics**:
   - Exit code `0`: All assertions passed 100%.
   - Exit code `1`: One or more assertions failed (acceptance criteria, schema, or tier failure).
   - Exit code `2`: System, transport, or configuration error.
   - Exit code `3`: External gatekeeper (Jev) quality rejection.

---

## 4. Thresholds & Success Criteria

### 4.1. Tier 1: Smoke & Contract Tests
- **Criteria**:
  - `plugin.json` must be valid JSONC with required keys (`name`, `displayName`, `description`, `version`, `logo`, `disabled`, `suggestedPrompts`).
  - Prohibited fields must be absent (`skills` array, `author`, `homepage`).
  - All 17 sub-agents must exist as `.md` files in `agents/`.
  - Every agent must declare `subagent: true`, `hidden: false`, `inheritCustomizations: true`, non-empty `description`, and valid `model: flash` or `model: pro`.
  - Pro models must be assigned strictly to `chief-of-staff`, `code-architect`, `clean-room-builder`, `security-reviewer`.
  - Flash models must be assigned to at least 12 agents (target 13 agents = 76.5% >= 12/17).
  - Minimum assertion count: >= 5 assertions per feature.

### 4.2. Tier 2: Boundary & Corner Cases
- **Criteria**:
  - Invalid YAML frontmatter or missing frontmatter delimiters must be identified and rejected.
  - Omission of `description` must trigger agent rejection warning (Antigravity drops agents without description).
  - Casing variations in YAML must be tested.
  - `rules/AGENTS.md` file size must not exceed the hard Antigravity memory limit of 24,000 bytes.
  - Jev gate must actively reject code leaks (e.g., Python code blocks) and missing evidence citations (`Source` and `Proof`).

### 4.3. Tier 3: Cross-Feature Integration
- **Criteria**:
  - ConnectRPC `GetAllPlugins` must dynamically discover `software-company` without requiring an IDE restart.
  - The Language Server must parse YAML `model: pro` into protobuf `modelTier: "MODEL_TIER_PRO"` and `model: flash` into `modelTier: "MODEL_TIER_FLASH"`.
  - Agents with `preloadSkills` must resolve against skills in the plugin's `skills/` directory.
  - Read-only reviewers must have read-only tools whitelisted, while builders and organizers have write tools.

### 4.4. Tier 4: Real-World Application Scenarios
- **Criteria**:
  - Full clean-room specification audit must be executed using `jev --audit sample_spec.md` against OpenRouter model `typesafe/jev-1.13`.
  - Jev audit must return exit code `0` with final verdict `APPROVED`.
  - Continuous scores must satisfy `has_hard_evidence >= 0.50`, `is_deterministic >= 0.50`, and `is_clean_room_safe >= 0.60`.
  - Sanitized `SPEC.approved.md` must be generated with all `Source` and `Proof` sections stripped clean.
  - Recursive security scan across the entire plugin directory must confirm zero OpenRouter API calls, zero hardcoded keys (`sk-or-v1-*`), and zero external HTTP calls outside `jev`.

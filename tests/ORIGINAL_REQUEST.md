# Original User Request & System Specification

## Timestamp: 2026-10-18T01:45:34Z

Build an autonomous, self-operating AI software engineering company system (Enterprise Software Company System) natively integrated as an independent Antigravity Plugin at `~/.gemini/config/plugins/software-company/`. Convert and standardize 15+ specialized sub-agents from the `affaan-m/ecc` repository, configure model tiering (flash/pro) to achieve maximum cost optimization, and establish an authoritative quality verification gate using `typesafe/jev-1.13`.

- **Working Directory**: `~/teamwork_projects/software_company_ecc`
- **Integrity Mode**: `development`
- **Reference**: https://github.com/affaan-m/ecc

---

## Requirements

### R1. Curate & Standardize 15+ Core Sub-Agents into an Antigravity Native Plugin
- Package as a standardized Antigravity plugin at `~/.gemini/config/plugins/software-company/`, including `plugin.json`, `agents/` directory, `rules/AGENTS.md`, and required `skills/`.
- Convert and standardize 15+ core sub-agents from `affaan-m/ecc` into Antigravity `agent.md` format (`subagent: true`, `hidden: false`, `inheritCustomizations: true`, `preloadSkills: [...]`):
  1. `chief-of-staff`: Executive orchestrator for workflow coordination and task decomposition.
  2. `planner`: Feature milestone breakdown and delivery scheduling.
  3. `code-architect`: System topology, data models, and API schemas.
  4. `clean-room-builder`: Core implementation engineer adhering to surgical edit principles.
  5. `refactor-cleaner`: Code cleanup, dead code pruning, and consolidation.
  6. `build-error-resolver`: Automated triage and minimal-diff repair of compiler/build errors.
  7. `python-reviewer`: Code quality, PEP 8, mypy strict typing, and async safety.
  8. `typescript-reviewer`: Type soundness, null safety, and interface hygiene.
  9. `react-reviewer`: Component lifecycle, hook dependencies, RSC boundaries, and render performance.
  10. `go-reviewer`: Idiomatic Go conventions, error wrapping, and goroutine leak prevention.
  11. `rust-reviewer`: Borrow checker compliance, unsafe safety audits, and memory efficiency.
  12. `database-reviewer`: Schema design, index strategies, migration safety, and query optimization.
  13. `security-reviewer`: Vulnerability scanning (OWASP Top 10, injection, credential leaks).
  14. `performance-optimizer`: Profiling analysis, I/O bottlenecks, and resource optimization.
  15. `silent-failure-hunter`: Detection of swallowed exceptions, unhandled promises, and edge cases.
  16. `e2e-runner`: Automated authoring and execution of end-to-end user journeys.
  17. `jev`: Authoritative quality gatekeeper auditing determinism and evidence via `jev`.

### R2. Aggressive Operational Cost Optimization
- **Model Tiering Strategy**:
  - Allocate `model: flash` (`MODEL_TIER_FLASH`) to $\ge 70\%$ of sub-agents (all code reviewers, cleaners, analyzers, and test runners).
  - Allocate `model: pro` (`MODEL_TIER_PRO`) strictly to core architectural and synthesis roles (`chief-of-staff`, `code-architect`, `clean-room-builder`, `security-reviewer`).
- **Zero API Key Leakage Policy**:
  - 100% of standard sub-agents execute natively on internal Antigravity models.
  - Zero usage of `OPENROUTER_API_KEY` for prompt generation or routine sub-agent reasoning.
  - `OPENROUTER_API_KEY` is exclusively reserved for the `jev` CLI invoking model `typesafe/jev-1.13` for formal specification audits.

### R3. Automated Workflow Governance & Quality Gates
- Provide organizational operating procedures and governance rules in `rules/AGENTS.md` defining how sub-agents collaborate across closed-loop SDLC workflows.
- Integrate an authoritative gate: Before finalizing any deliverable, specifications and test criteria must be formally verified via `typesafe/jev-1.13`.

---

## Acceptance Criteria

### Plugin Integrity & Sub-Agent Configuration
- [x] The plugin directory `~/.gemini/config/plugins/software-company/` contains a valid `plugin.json` recognized dynamically by the Antigravity Language Server via ConnectRPC `GetAllPlugins`.
- [x] All 17 `agent.md` definitions exist with valid frontmatter attributes (`subagent: true`, `hidden: false`, `inheritCustomizations: true`, corresponding `modelTier`).
- [x] Model tier distribution verification: At least 12 of 17 agents configured on the `flash` tier.

### Cost Control & Jev Quality Assurance
- [x] Confirmed zero configurations or scripts in the plugin make third-party OpenRouter calls, except for the `jev` binary.
- [x] Automated test suites execute cleanly and verify a live specification audit using `jev` with model `typesafe/jev-1.13`.

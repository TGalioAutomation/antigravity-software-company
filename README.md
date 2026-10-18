# Enterprise Software Company — Antigravity Agent Plugin

An **Autonomous AI Software Engineering Organization** engineered and packaged as a **100% Standalone & Self-Contained** plugin for Google Antigravity (with cross-compatibility for Claude Code, Cursor, and OpenCode). The system bundles 17 core sub-agents and a self-contained skills library, operating with **zero runtime dependencies on external repositories or services**.

---

## 1. Architecture & Organizational Structure (17 Sub-Agents)

```
                  ┌───────────────────────────────────────────────┐
                  │       Leadership & Dispatch Squad             │
                  │  chief-of-staff (Pro)  │  planner (Flash)     │
                  └───────────────────────┬───────────────────────┘
                                          │
                  ┌───────────────────────▼───────────────────────┐
                  │             Architectural Authority           │
                  │              code-architect (Pro)             │
                  └───────────────────────┬───────────────────────┘
                                          │
                  ┌───────────────────────▼───────────────────────┐
                  │            Clean-Room Implementation          │
                  │  clean-room-builder (Pro) ──► Jev Gatekeeper  │
                  │                               (typesafe/jev)  │
                  └───────────────────────┬───────────────────────┘
                                          │
                  ┌───────────────────────▼───────────────────────┐
                  │       Quality & Language Review Gates         │
                  │  python-reviewer   │ typescript-reviewer      │
                  │  react-reviewer    │ go-reviewer              │
                  │  rust-reviewer     │ database-reviewer        │
                  │  security-reviewer │ performance-optimizer    │
                  │  silent-failure-hunter                        │
                  └───────────────────────┬───────────────────────┘
                                          │
                  ┌───────────────────────▼───────────────────────┐
                  │       Remediation & Delivery Squad            │
                  │  build-error-resolver │ refactor-cleaner      │
                  │  e2e-runner           │ jev                   │
                  └───────────────────────────────────────────────┘
```

### Sub-Agent Roster & Tier Allocation

| Sub-Agent | Model Tier | Runtime / Cost | Scope, Boundary & Review Focus |
| :--- | :---: | :---: | :--- |
| **`chief-of-staff`** | `pro` | Antigravity Native | Executive orchestrator: ingests initiatives, triages priorities, and oversees delivery milestones. |
| **`planner`** | `flash` | Antigravity Native | Task breakdown across 4 phases: Minimum Viable Slice (MVS) $\rightarrow$ Core $\rightarrow$ Resilience $\rightarrow$ Polish. |
| **`code-architect`** | `pro` | Antigravity Native | Principal system design, entity models, REST/gRPC schemas, and Architecture Decision Records (ADRs). |
| **`clean-room-builder`** | `pro` | Antigravity Native | Surgical implementation from approved specifications, isolated from legacy source code leakage. |
| **`jev`** | `flash` | **OpenRouter Gate** | Epistemic gatekeeper: executes `jev` (`typesafe/jev-1.13`) for determinism and evidence audits. |
| **`python-reviewer`** | `flash` | Antigravity Native | Enforces PEP 8, mypy strict typing, async/await correctness; bans bare `except: pass` and SQL injections. |
| **`typescript-reviewer`** | `flash` | Antigravity Native | Verifies type soundness, eliminates unjustified `any`, detects floating promises and async misuse. |
| **`react-reviewer`** | `flash` | Antigravity Native | Audits hook dependencies, Server/Client component boundaries (RSC), re-render efficiency, and XSS. |
| **`go-reviewer`** | `flash` | Antigravity Native | Verifies idiomatic Go error wrapping (`%w`), goroutine leak prevention via `context.Context`, race safety. |
| **`rust-reviewer`** | `flash` | Antigravity Native | Audits borrow-checker semantics, eliminates production `.unwrap()`, enforces `// SAFETY:` rationale on `unsafe`. |
| **`database-reviewer`** | `flash` | Antigravity Native | Reviews foreign key indexes, RLS security queries, cursor pagination, and `SKIP LOCKED` worker queues. |
| **`security-reviewer`** | `pro` | Antigravity Native | Comprehensive threat modeling: OWASP Top 10, auth bypass, path traversal, hardcoded secrets, injection. |
| **`performance-optimizer`** | `flash` | Antigravity Native | Latency profiling, memory leak detection, N+1 query elimination, bundle size budgets (<200KB JS). |
| **`silent-failure-hunter`** | `flash` | Antigravity Native | Detects swallowed exceptions, empty catch blocks, bad fallback returns (`.catch(() => [])`), missing rollbacks. |
| **`build-error-resolver`** | `flash` | Antigravity Native | Minimal-diff error repair (<5% file delta): resolves broken imports, missing dependencies, compiler errors. |
| **`refactor-cleaner`** | `flash` | Antigravity Native | Safe dead code pruning, orphaned export removal, and duplicate consolidation using static analysis. |
| **`e2e-runner`** | `flash` | Antigravity Native | Authors and executes automated user journeys; immediately quarantines flaky tests via `test.fixme()`. |

---

## 2. Cost Optimization & Security Perimeter

1. **Aggressive Model Tiering**:
   - **13 of 17 sub-agents (76.5%)** operate on `model: flash` (`MODEL_TIER_FLASH`) to maximize throughput, minimize latency, and reduce token consumption.
   - Only **4 of 17 sub-agents (23.5%)** are assigned `model: pro` (`MODEL_TIER_PRO`), strictly reserved for high-reasoning coordination, architectural synthesis, clean-room implementation, and deep security analysis.
2. **Strict Zero-OpenRouter Leakage Policy**:
   - 100% of sub-agent reasoning, code writing, and reviews execute natively on Antigravity infrastructure.
   - The `OPENROUTER_API_KEY` is **exclusively reserved for `typesafe/jev-1.13`** invoked through the `jev` CLI binary for formal specification audits.
   - No sub-agent prompt, script, or automated hook transmits data to external third-party model gateways.

---

## 3. Quickstart Guide

### 1-Click Installation (Antigravity & Supported Environments):
```bash
git clone https://github.com/TGalioAutomation/antigravity-software-company.git
cd antigravity-software-company
./install.sh
```

### Run Full System Verification:
```bash
./verify.sh
```

### Clean Uninstallation:
```bash
./uninstall.sh
```

---

## 4. Repository Layout & Asset Catalog

All high-value capabilities from `affaan-m/ecc` have been standardized, enriched, and packaged as self-contained local resources:

```text
antigravity-software-company/
├── software-company/              # 🚀 Standalone Antigravity Plugin (Spec 1.0.0)
│   ├── plugin.json                # Plugin manifest auto-discovered by Language Server
│   ├── README.md                  # Detailed plugin architectural documentation
│   ├── assets/logo.svg            # Identity branding
│   ├── agents/                    # 17 Core Sub-Agents (4 Pro / 13 Flash)
│   ├── rules/AGENTS.md            # Organizational governance rules & SDLC workflows
│   └── skills/                    # 26 Preloaded Core Engineering Skills (preloadSkills)
│       ├── api-design/            ├── golang-patterns/       ├── python-testing/
│       ├── architecture-decision-records/ ├── golang-testing/ ├── react-patterns/
│       ├── backend-patterns/      ├── postgres-patterns/     ├── rust-patterns/
│       ├── clean-room/            ├── prompt-master/         ├── rust-testing/
│       ├── coding-standards/      ├── python-patterns/       ├── security-review/
│       ├── database-migrations/   ├── e2e-testing/           ├── software-company-workflow/
│       ├── docker-patterns/       ├── eval-harness/          ├── strategic-compact/
│       ├── frontend-patterns/     ├── search-first/          ├── tdd-workflow/
│       └── continuous-learning/   └── verification-loop/
├── skills/                        # 📚 Standalone Engineering Library (314 domain skills)
├── rules/                         # 📏 22 Language & Framework Rule Sets (common, ts, py, go, rust...)
├── commands/                      # ⚡ 97 Slash Commands & Workflows (plan, prp, orch-*, review...)
├── contexts/                      # 🎯 3 Context Profiles (dev.md, research.md, review.md)
├── agents-catalog/                # 🧩 Extended Catalog of 71 Domain Agents (Flutter, Django, MLE...)
├── tests/                         # 🧪 Automated Multi-Tier Test Suites (21/21 E2E tests PASS)
├── install.sh                     # Cross-platform 1-click automated installer
├── uninstall.sh                   # Clean uninstaller script
├── verify.sh                      # Unified verification runner
└── README.md                      # Primary documentation
```

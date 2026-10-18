# Enterprise AI Software Company (`software-company`)

An autonomous, multi-agent enterprise software engineering organization packaged as a native Antigravity Plugin. **100% self-contained and standalone with zero external dependencies**, this plugin establishes a self-governing virtual software company capable of planning, architecting, implementing, reviewing, and verifying complex software deliverables.

---

## 1. Overview & Core Philosophy

The **Enterprise AI Software Company** transforms autonomous engineering workflows through four core pillars:

1. **Role Specialization**: 17 specialized sub-agents collaborate within defined organizational boundaries (leadership, architecture, clean-room implementation, language-specific code review, quality gatekeeping).
2. **Strict Model Tiering & Cost-Optimization**: 70%+ of agent operations are allocated to ultra-fast, cost-effective `flash` models, reserving high-capacity `pro` models solely for architectural decisions, clean-room synthesis, and deep security threat modeling.
3. **Ironclad API Key Preservation**: 100% of internal agents execute natively within Antigravity infrastructure. Zero requests are routed to third-party endpoints, except for the standalone `typesafe/jev-1.13` specification gatekeeper.
4. **Clean-Room Engineering & Formal Verification**: Implementations are insulated from prompt leakage and evaluated against deterministic evidence criteria before code merges.

---

## 2. Plugin Architecture

```text
~/.gemini/config/plugins/software-company/
├── plugin.json                              # Antigravity Plugin Spec 1.0.0 manifest
├── README.md                                # Architectural documentation
├── assets/
│   └── logo.svg                             # 128x128 SVG identity branding
├── rules/
│   └── AGENTS.md                            # Always-on organizational governance rules
├── skills/
│   └── software-company-workflow/
│       ├── SKILL.md                         # Multi-agent SDLC & squad procedures
│       └── references/                      # Review rubrics & quality standards
└── agents/
    ├── chief-of-staff.md                    # Pro: Executive Orchestrator
    ├── planner.md                           # Flash: Task & Milestone Planner
    ├── code-architect.md                    # Pro: System & Schema Architect
    ├── clean-room-builder.md                # Pro: Clean-Room Implementation Engineer
    ├── refactor-cleaner.md                  # Flash: Code Refactoring & Dead Code Cleaner
    ├── build-error-resolver.md              # Flash: Compilation & Build Failure Specialist
    ├── python-reviewer.md                   # Flash: Python Code Reviewer (PEP 8, Typing)
    ├── typescript-reviewer.md               # Flash: TypeScript/JavaScript Reviewer
    ├── react-reviewer.md                    # Flash: React/Next.js Architecture Reviewer
    ├── go-reviewer.md                       # Flash: Go Idioms & Concurrency Reviewer
    ├── rust-reviewer.md                     # Flash: Rust Safety & Memory Reviewer
    ├── database-reviewer.md                 # Flash: Database Schema & Query Reviewer
    ├── security-reviewer.md                 # Pro: OWASP & Vulnerability Auditor
    ├── performance-optimizer.md             # Flash: Profiling & Bottleneck Optimizer
    ├── silent-failure-hunter.md             # Flash: Exception & Swallowed Error Specialist
    ├── e2e-runner.md                        # Flash: End-to-End Verification Specialist
    └── jev.md                               # Flash: TypeSafe Jev Gatekeeper Wrapper
```

---

## 3. Sub-Agent Roster & Tier Matrix

The squad comprises 17 purpose-built sub-agents registered in Antigravity:

| # | Agent Name | Model Tier | Scope / Responsibilities |
|---|---|---|---|
| 1 | `chief-of-staff` | `pro` | Strategic leadership, multi-squad orchestration, escalation triage |
| 2 | `planner` | `flash` | Milestone scheduling, dependency sequencing, WBS breakdown |
| 3 | `code-architect` | `pro` | System topology, database schemas, API contracts, boundary design |
| 4 | `clean-room-builder` | `pro` | Surgical code implementation isolated from source leakage |
| 5 | `refactor-cleaner` | `flash` | Dead code pruning, syntax streamlining, minimal refactoring |
| 6 | `build-error-resolver` | `flash` | Compiler/linker error triage, dependency mismatch resolution |
| 7 | `python-reviewer` | `flash` | PEP 8, mypy typing, async event loop safety, memory efficiency |
| 8 | `typescript-reviewer` | `flash` | Strict typing, null/undefined safety, interface hygiene |
| 9 | `react-reviewer` | `flash` | Hook dependency safety, render optimization, memoization |
| 10 | `go-reviewer` | `flash` | Concurrency safety, goroutine leaks, error wrapping idioms |
| 11 | `rust-reviewer` | `flash` | Borrow checker compliance, unsafe block avoidance, zero-cost idioms |
| 12 | `database-reviewer` | `flash` | Query indexing, N+1 prevention, migration safety, ACID boundaries |
| 13 | `security-reviewer` | `pro` | OWASP Top 10 auditing, authorization bypass, injection vectors |
| 14 | `performance-optimizer`| `flash` | Algorithmic complexity, latency bottlenecks, memory profiling |
| 15 | `silent-failure-hunter`| `flash` | Swallowed exceptions, unhandled promises, edge-case null checks |
| 16 | `e2e-runner` | `flash` | Automated test suite execution, integration verification |
| 17 | `jev` | `flash` | Operational wrapper for `jev` CLI running `typesafe/jev-1.13` |

### Model Tiering Economics
- **Flash Tier**: 13 agents (76.5%) handling high-frequency planning, code reviews, dead code pruning, error resolution, and test runner workflows.
- **Pro Tier**: Exactly 4 agents (23.5%) reserved for executive coordination (`chief-of-staff`), architectural modeling (`code-architect`), clean-room synthesis (`clean-room-builder`), and security vulnerability auditing (`security-reviewer`).
- **Cost Reduction**: Achieves substantial token savings across enterprise software lifecycles while sustaining high reasoning precision where needed.

---

## 4. Software Development Lifecycle (SDLC) Workflow

1. **Strategic Inception**: `chief-of-staff` receives the high-level product objective and dispatches `planner` to establish milestones.
2. **Architecture & Contract Definition**: `code-architect` authors schemas and interfaces.
3. **Specification Gate (Jev Audit)**: Specifications are checked by `jev` using `typesafe/jev-1.13` (`jev --audit <spec>`). The milestone requires `APPROVED` status before code construction begins.
4. **Clean-Room Implementation**: `clean-room-builder` executes surgical modifications against approved contracts.
5. **Multi-Discipline Review**: Targeted language reviewers (`python-reviewer`, `typescript-reviewer`, etc.), `security-reviewer`, and `performance-optimizer` evaluate the code changes.
6. **Continuous Build & E2E Verification**: `build-error-resolver` handles any compilation faults, and `e2e-runner` confirms end-to-end acceptance tests pass.

---

## 5. Security & Isolation Policy

- **No OpenRouter Calls in Agent Code**: Sub-agents must not invoke OpenRouter APIs directly.
- **Restricted CLI Access**: The `jev` binary is the sole interface authorized to use `OPENROUTER_API_KEY` for specification audits.
- **Least-Privilege Tooling**: Code reviewers possess read-only and task-inspection capabilities (`send_message`, `view_file`, `run_command`, `manage_task`), preventing unintended code modifications during review phases.

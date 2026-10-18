---
name: software-company-workflow
description: Standard operating procedures and delegation protocols for the Enterprise Software Company sub-agents.
---

# Enterprise Software Company — Workflow & Delegation Standard Operating Procedures

This skill codifies the Standard Operating Procedures (SOPs), delegation handoff contracts, quality review gates, and verification protocols for the 17 specialized sub-agents in the Enterprise Software Company (`software-company`) plugin.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        Enterprise SDLC Operating Pipeline                              │
│                                                                                        │
│  [1. Intake & Triage]       chief-of-staff (Pro)                                       │
│          │                                                                             │
│          ▼                                                                             │
│  [2. Roadmapping]           planner (Flash)                                            │
│          │                                                                             │
│          ▼                                                                             │
│  [3. Architecture & ADR]    code-architect (Pro)                                       │
│          │                                                                             │
│          ▼                                                                             │
│  [4. Clean-Room Rebuild]    rea (Flash) ──► jev (Flash/CLI) ──► HUMAN "GO" GATE        │
│                                              │                                         │
│                                              ▼                                         │
│                             clean-room-builder (Pro) ──► clean-room-tester (Flash)     │
│          │                                                                             │
│          ▼                                                                             │
│  [5. Language Review Gates] python | typescript | react | go | rust | database |       │
│                             security | performance | silent-failure                    │
│          │                                                                             │
│          ▼                                                                             │
│  [6. Remediation & Clean]   build-error-resolver (Flash) | refactor-cleaner (Flash)   │
│          │                                                                             │
│          ▼                                                                             │
│  [7. E2E & Jev Gate]        e2e-runner (Flash) ──► jev (typesafe/jev-1.13)             │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. The Delegation Completion Contract (Anti-Zombie Protocol)

In a multi-agent organization, delegating a task without monitoring and integrating its result leads to context drift, duplicate work, and zombie processes. Every sub-agent must uphold the **Delegation Completion Contract**:

1. **Dispatcher Accountability**:
   - The agent initiating delegation remains the owner of the outcome.
   - When calling `invoke_subagent` or issuing a task brief, the dispatcher must specify:
     - Exact working directory and target deliverable files.
     - Concrete acceptance criteria (Done-When conditions).
     - Constraints and non-negotiables.
2. **Synchronous or Monitored Execution**:
   - The delegator must wait for subagent deliverables and verify that output files exist and pass validation.
   - Fire-and-forget task launching is strictly forbidden.
3. **Structured Deliverables**:
   - Sub-agents communicate results via structured files and summary messages.
   - If a sub-agent encounters an unresolvable blocker, it must deliver a partial handoff report detailing observations and blocker points rather than failing silently.

---

## 2. Phase-by-Phase Standard Operating Procedures

### Phase 1: Intake & Triage SOP (`chief-of-staff`)
1. **Intake Classification**:
   Evaluate every incoming request into one of 4 tiers:
   - `skip`: Automated noise, bot notifications, or out-of-scope pings. Discard immediately.
   - `info_only`: Status updates. Record a single-line log and acknowledge.
   - `meeting_info`: Scheduling, dependency tracking, or timeline milestones.
   - `action_required`: Substantive technical initiatives requiring squad activation.
2. **Task Decomposition**:
   Draft a structured Task Brief defining:
   - `Scope`: Target files, affected modules, and excluded components.
   - `Stop Conditions`: Scenarios requiring escalation to human operator.
   - `Done When`: Exact binary verification tests and deliverables.
3. **Squad Allocation**:
   Route planning to `planner`, architecture to `code-architect`, or direct reviews to language reviewers.

---

### Phase 2: Milestone Planning SOP (`planner`)
1. **Requirements & Codebase Blast Radius Analysis**:
   - Inspect project directories, dependency trees, and existing test coverage before planning code edits.
2. **4-Phase Milestone Sizing**:
   Break down feature delivery into sequential, testable increments:
   - **Phase 1: Minimum Viable Slice (MVS)** — Simplest end-to-end happy path; validates contracts early.
   - **Phase 2: Core Experience** — Full business logic and expected operational workflows.
   - **Phase 3: Resilience & Edge Cases** — Error recovery, boundary cases, rate limits, and fallbacks.
   - **Phase 4: Optimization & Polish** — Profiling, bundle reduction, and monitoring metrics.
3. **Milestone Artifact**:
   Publish the implementation plan with exact file paths, risk ratings (Low/Medium/High), and explicit verification commands for each step.

---

### Phase 3: Architectural Blueprinting SOP (`code-architect`)
1. **Pattern & Invariant Analysis**:
   - Inspect existing architectural styles, naming patterns, and design abstractions.
   - Do NOT introduce speculative frameworks or unnecessary abstraction layers.
2. **Architecture Decision Records (ADRs)**:
   Author an ADR for non-trivial decisions (schema changes, library selections, concurrency patterns).
3. **Strict Build Sequence Ordering**:
   Enforce the dependency ladder:
   1. Data types, schemas, and interface definitions.
   2. Pure core domain logic.
   3. Integration, persistence, and external service adapters.
   4. User interfaces, API routes, and presentation layers.
   5. Automated tests and documentation.
4. **Modularity Constraints**:
   Keep files between 200 and 400 lines (never exceeding 800 lines). Enforce single responsibility and immutability.

---

### Phase 4: Clean-Room Rebuild SOP (`rea` + `jev` + `clean-room-builder` + `clean-room-tester`)

When rebuilding, cloning, or refactoring existing modules:

```
                  Step 1: REA Investigation
             (Read-only inspection of original app)
                            │
                            ▼
                  Step 2: Jev Evidence Audit
             (/Users/apexdev/.local/bin/jev --audit)
                            │
               ┌────────────┴────────────┐
               ▼                         ▼
         REJECTED (Score < Min)     APPROVED (100%)
               │                         │
               └──► Fix in REA           ▼
                               Step 3: Human "go" Gate
                              (Execution stops & waits)
                                         │
                                   "go" received
                                         │
                                         ▼
                               Step 4: Isolated Builder
                              (clean-room-builder on Pro)
                                         │
                                         ▼
                               Step 5: 3-Mutant Tester
                              (Main PASS + Mutants FAIL)
```

1. **Step 1 — REA Extraction**:
   - `rea` inspects the reference codebase.
   - Authors `clean-room/SPEC.md` detailing every behavior, invariant, and error branch.
   - Every rule MUST have `Source: [file:line]` and `Proof: [factual observation]`.
2. **Step 2 — Jev Gatekeeper Audit**:
   - Run `/Users/apexdev/.local/bin/jev --audit clean-room/SPEC.md`.
   - Must achieve:
     - `Evidence Score >= 0.50`
     - `Deterministic Score >= 0.50`
     - `Clean-Room Score >= 0.60`
     - Overall Verdict: `APPROVED`.
   - Jev strips all source citations and outputs `clean-room/SPEC.approved.md`.
3. **Step 3 — Mandatory Human Stop Gate ("go")**:
   - Display `clean-room/SPEC.approved.md` to the user.
   - **STOP completely**. Wait for the user to explicitly type `"go"`.
4. **Step 4 — Clean-Room Builder Implementation**:
   - Spawn `clean-room-builder` (Pro tier) receiving ONLY `clean-room/SPEC.approved.md`.
   - Never inspect the original codebase. If ambiguities exist, write questions into `clean-room/builder-questions.md` for Jev arbitration.
5. **Step 5 — 3-Mutant Verification Matrix**:
   - `clean-room-tester` creates comprehensive test suites from the specification.
   - Synthesizes 3 deliberate failure mutants under `clean-room/mutants/`:
     - `mutant-1`: Off-by-one or boundary condition sabotage.
     - `mutant-2`: Invariant, authorization, or state-machine bypass.
     - `mutant-3`: Error-branch or swallowed-exception sabotage.
   - **Acceptance Criterion**: Main build passes 100%, and ALL 3 mutants FAIL.

---

### Phase 5: Specialized Review Gates SOP

Before merging any code, dispatch the relevant language and security reviewers:

```
Code Changes
     │
     ├──► Python Files?      ──► python-reviewer     (mypy, ruff, bandit, pytest)
     ├──► TypeScript/JS?     ──► typescript-reviewer (type safety, floating promises)
     ├──► React/UI?          ──► react-reviewer      (hooks, a11y, DOMPurify, RSC)
     ├──► Go Files?          ──► go-reviewer         (goroutine leaks, error wrapping %w)
     ├──► Rust Files?        ──► rust-reviewer       (borrow checker, // SAFETY:, clippy)
     ├──► SQL/Migrations?    ──► database-reviewer   (FK indexes, RLS subqueries, SKIP LOCKED)
     ├──► Auth/Crypto/APIs?  ──► security-reviewer   (OWASP Top 10, secrets, injection)
     ├──► Perf Critical?     ──► performance-optimizer(profiling, bundle size, latency)
     └──► All Error Paths?   ──► silent-failure-hunter(swallowed exceptions, unhandled rejections)
```

1. **Confidence Filtering**: Reviewers only flag defects with `>80%` confidence and verifiable failure triggers. Speculative nitpicks are suppressed.
2. **Gate Verdicts**:
   - `APPROVE`: Zero Critical and Zero High findings. Clean reviews are standard and expected.
   - `BLOCK`: Any Critical or High finding requires immediate remediation.

---

### Phase 6: Surgical Remediation SOP (`build-error-resolver` & `refactor-cleaner`)
1. **Compilation & Build Errors (`build-error-resolver`)**:
   - Rule: **Minimal Diffs Only**. Modifies <5% of affected files.
   - No unsolicited architectural refactoring, formatting cleanup, or logic rewrites. Focus exclusively on restoring green build status.
2. **Dead Code Cleanup (`refactor-cleaner`)**:
   - Execute static detection tools (`knip`, `depcheck`, `ts-prune`).
   - Categorize by risk (`SAFE`, `CAREFUL`, `RISKY`).
   - Remove unused items in incremental batches. Run tests and commit after each batch to preserve safety.

---

### Phase 7: End-to-End Verification SOP (`e2e-runner` & `jev`)
1. **Automated User Journeys (`e2e-runner`)**:
   - Adopt Page Object Model (POM) architecture.
   - Rely on semantic, resilient locators (`@e1` or `[data-testid="..."]`).
   - Use condition-based auto-waiting; hardcoded delays (`sleep`, `waitForTimeout`) are forbidden.
   - Quarantine flaky tests with `test.fixme()` and document the tracking ticket.
2. **Final Oracle Verification (`jev`)**:
   - Execute `/Users/apexdev/.local/bin/jev` on final specifications or critical requirements to confirm 100% determinism.

---

## 3. Standard Deliverable Formats

### 3.1 Task Brief Format (Chief of Staff → Squad)
```markdown
# Task Brief: [Task Title]

- **Assigned Subagent**: [agent-name]
- **Model Tier**: [flash | pro]
- **Target Files**: [exact file paths]

## Scope & Objective
[Concise description of the functional change]

## Hard Constraints
- [Constraint 1]
- [Constraint 2]

## Stop Conditions
- [Condition triggering escalation to parent]

## Done-When Verification
- [Command 1]: [Expected output]
- [Command 2]: [Expected output]
```

### 3.2 5-Component Handoff Report Format
Every sub-agent delivering results must write a `handoff.md` containing:
1. **Observation**: Direct observations, exact file paths, line numbers, command exit codes.
2. **Logic Chain**: Step-by-step reasoning linking observations to findings.
3. **Caveats**: Unexplored edge cases, environmental assumptions, or limitations.
4. **Conclusion**: Final assessment, approval verdict, or deliverable status.
5. **Verification Method**: Exact reproducible commands for independent verification.

---

## 4. Cost Optimization & Model Routing Reference

```
Pro Tier (4 Agents)    : chief-of-staff, code-architect, clean-room-builder, security-reviewer
Flash Tier (13 Agents) : planner, refactor-cleaner, build-error-resolver, python-reviewer,
                         typescript-reviewer, react-reviewer, go-reviewer, rust-reviewer,
                         database-reviewer, performance-optimizer, silent-failure-hunter,
                         e2e-runner, jev
```

All 17 sub-agents execute natively on internal Antigravity models. The standalone external binary `/Users/apexdev/.local/bin/jev` is the sole tool authorized for external verification calls.

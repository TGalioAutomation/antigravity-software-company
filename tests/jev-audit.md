# Jev Clean-Room Audit Report (`typesafe/jev-1.13`)

- **Source Spec**: `/Users/apexdev/Desktop/plugin-buildin/tests/sample_spec.md`
- **Total Rules Audited**: 2
- **Thresholds**: Evidence >= `0.5`, Deterministic >= `0.5`, Clean-Room >= `0.6`

## [1] RULE-001: Deterministic Numeric Boundary Clamping
- **Final Gate Verdict**: `APPROVED` (**PASS**, confidence: `0.53`)
- **Scores (`noul`)**: Evidence=`0.67` | Deterministic=`0.73` | Clean-Room Safe=`0.71`
- **Probabilities**: `{"APPROVED": 0.65, "REJECT_MISSING_EVIDENCE": 0.06, "REJECT_AMBIGUOUS": 0.02, "REJECT_CODE_LEAK": 0.27}`

## [2] RULE-002: Deterministic String Truncation with Ellipsis Suffix
- **Final Gate Verdict**: `APPROVED` (**PASS**, confidence: `0.55`)
- **Scores (`noul`)**: Evidence=`0.62` | Deterministic=`0.59` | Clean-Room Safe=`0.69`
- **Probabilities**: `{"APPROVED": 0.66, "REJECT_MISSING_EVIDENCE": 0.03, "REJECT_AMBIGUOUS": 0.04, "REJECT_CODE_LEAK": 0.27}`


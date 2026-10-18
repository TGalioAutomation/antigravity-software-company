# Jev Clean-Room Audit Report (`typesafe/jev-1.13`)

- **Source Spec**: `/Users/apexdev/Desktop/plugin-buildin/tests/sample_spec.md`
- **Total Rules Audited**: 2
- **Thresholds**: Evidence >= `0.5`, Deterministic >= `0.5`, Clean-Room >= `0.6`

## [1] RULE-001: Deterministic Numeric Boundary Clamping
- **Final Gate Verdict**: `APPROVED` (**PASS**, confidence: `0.60`)
- **Scores (`noul`)**: Evidence=`0.61` | Deterministic=`0.73` | Clean-Room Safe=`0.68`
- **Probabilities**: `{"APPROVED": 0.7, "REJECT_MISSING_EVIDENCE": 0.06, "REJECT_AMBIGUOUS": 0.01, "REJECT_CODE_LEAK": 0.23}`

## [2] RULE-002: Deterministic String Truncation with Ellipsis Suffix
- **Final Gate Verdict**: `APPROVED` (**PASS**, confidence: `0.60`)
- **Scores (`noul`)**: Evidence=`0.63` | Deterministic=`0.54` | Clean-Room Safe=`0.73`
- **Probabilities**: `{"APPROVED": 0.7, "REJECT_MISSING_EVIDENCE": 0.03, "REJECT_AMBIGUOUS": 0.04, "REJECT_CODE_LEAK": 0.23}`


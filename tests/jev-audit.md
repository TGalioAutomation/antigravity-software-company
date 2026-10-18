# Jev Clean-Room Audit Report (`typesafe/jev-1.13`)

- **Source Spec**: `/Users/apexdev/Desktop/plugin-buildin/tests/sample_spec.md`
- **Total Rules Audited**: 2
- **Thresholds**: Evidence >= `0.5`, Deterministic >= `0.5`, Clean-Room >= `0.6`

## [1] RULE-001: Deterministic Numeric Boundary Clamping
- **Final Gate Verdict**: `APPROVED` (**PASS**, confidence: `0.63`)
- **Scores (`noul`)**: Evidence=`0.64` | Deterministic=`0.71` | Clean-Room Safe=`0.71`
- **Probabilities**: `{"APPROVED": 0.72, "REJECT_MISSING_EVIDENCE": 0.05, "REJECT_AMBIGUOUS": 0.01, "REJECT_CODE_LEAK": 0.22}`

## [2] RULE-002: Deterministic String Truncation with Ellipsis Suffix
- **Final Gate Verdict**: `APPROVED` (**PASS**, confidence: `0.56`)
- **Scores (`noul`)**: Evidence=`0.62` | Deterministic=`0.58` | Clean-Room Safe=`0.72`
- **Probabilities**: `{"APPROVED": 0.67, "REJECT_MISSING_EVIDENCE": 0.04, "REJECT_AMBIGUOUS": 0.04, "REJECT_CODE_LEAK": 0.25}`


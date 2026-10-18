# Jev Clean-Room Audit Report (`typesafe/jev-1.13`)

- **Source Spec**: `sample_spec.md`
- **Total Rules Audited**: 2
- **Thresholds**: Evidence >= `0.5`, Deterministic >= `0.5`, Clean-Room >= `0.6`

## [1] RULE-001: Deterministic Numeric Boundary Clamping
- **Final Gate Verdict**: `APPROVED` (**PASS**, confidence: `0.56`)
- **Scores (`noul`)**: Evidence=`0.65` | Deterministic=`0.70` | Clean-Room Safe=`0.71`
- **Probabilities**: `{"APPROVED": 0.67, "REJECT_MISSING_EVIDENCE": 0.06, "REJECT_AMBIGUOUS": 0.01, "REJECT_CODE_LEAK": 0.26}`

## [2] RULE-002: Deterministic String Truncation with Ellipsis Suffix
- **Final Gate Verdict**: `APPROVED` (**PASS**, confidence: `0.56`)
- **Scores (`noul`)**: Evidence=`0.63` | Deterministic=`0.58` | Clean-Room Safe=`0.71`
- **Probabilities**: `{"APPROVED": 0.67, "REJECT_MISSING_EVIDENCE": 0.04, "REJECT_AMBIGUOUS": 0.04, "REJECT_CODE_LEAK": 0.25}`


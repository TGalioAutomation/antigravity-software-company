# Jev Clean-Room Audit Report (`typesafe/jev-1.13`)

- **Source Spec**: `tests/sample_spec.md`
- **Total Rules Audited**: 2
- **Thresholds**: Evidence >= `0.5`, Deterministic >= `0.5`, Clean-Room >= `0.6`

## [1] RULE-001: Deterministic Numeric Boundary Clamping
- **Final Gate Verdict**: `APPROVED` (**PASS**, confidence: `0.56`)
- **Scores (`noul`)**: Evidence=`0.64` | Deterministic=`0.74` | Clean-Room Safe=`0.69`
- **Probabilities**: `{"APPROVED": 0.67, "REJECT_MISSING_EVIDENCE": 0.06, "REJECT_AMBIGUOUS": 0.02, "REJECT_CODE_LEAK": 0.25}`

## [2] RULE-002: Deterministic String Truncation with Ellipsis Suffix
- **Final Gate Verdict**: `APPROVED` (**PASS**, confidence: `0.55`)
- **Scores (`noul`)**: Evidence=`0.60` | Deterministic=`0.57` | Clean-Room Safe=`0.68`
- **Probabilities**: `{"APPROVED": 0.66, "REJECT_MISSING_EVIDENCE": 0.04, "REJECT_AMBIGUOUS": 0.04, "REJECT_CODE_LEAK": 0.26}`


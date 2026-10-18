# Clean-Room Behavioral Specification: Core Company Utilities

This document specifies deterministic black-box behavioral contracts extracted by REA for clean-room implementation and validation by Jev (`typesafe/jev-1.13`).

### RULE-001: Deterministic Numeric Boundary Clamping
- **Description**: Clamps an input real number within specified inclusive lower and upper boundary limits.
- **Inputs**:
  - `val`: Real number to be constrained.
  - `min_val`: Real number representing the inclusive lower boundary.
  - `max_val`: Real number representing the inclusive upper boundary (must be greater than or equal to `min_val`).
- **Behavioral Contract**:
  - If `val` is strictly less than `min_val`, the function returns `min_val`.
  - If `val` is strictly greater than `max_val`, the function returns `max_val`.
  - If `val` is greater than or equal to `min_val` and less than or equal to `max_val`, the function returns `val` unchanged.
- **Boundary & Error Invariants**:
  - If `min_val` is strictly greater than `max_val`, an invalid argument exception must be raised.
  - If any input parameter is null, undefined, or non-numeric, a type exception must be raised.
  - Clamping preserves exact floating-point values when within boundaries.
- **Evidence**:
  - **Source**: `packages/utils/src/clamp.ts:12-38`
  - **Proof**: The reference implementation checks bounds validity first, performs ordered comparisons against minimum and maximum boundaries, and returns boundary values on overflow or underflow. Verified against unit test suite at `packages/utils/tests/clamp.test.ts:15-54`.

### RULE-002: Deterministic String Truncation with Ellipsis Suffix
- **Description**: Truncates a string to a specified maximum length, appending a designated suffix while preserving exact length constraints.
- **Inputs**:
  - `text`: Input character string to truncate.
  - `max_length`: Positive integer defining the maximum allowed total character length of the result.
  - `suffix`: Character string appended when truncation occurs (defaults to `...`).
- **Behavioral Contract**:
  - If the character length of `text` is less than or equal to `max_length`, the function returns `text` without modification.
  - If the character length of `text` is strictly greater than `max_length`, the function returns a newly formed string consisting of the initial prefix of `text` followed immediately by `suffix`, such that the total character count of the combined string equals `max_length`.
- **Boundary & Error Invariants**:
  - If `max_length` is strictly less than the character length of `suffix`, an invalid argument exception must be raised because the suffix cannot fit within the allowed capacity.
  - If `max_length` is not a positive integer, an invalid argument exception must be raised.
  - If `text` or `suffix` is null, undefined, or not a string, a type exception must be raised.
  - Truncation must never produce an output string whose character count exceeds `max_length`.
- **Evidence**:
  - **Source**: `packages/utils/src/truncate.ts:20-49`
  - **Proof**: The reference implementation ensures output length never exceeds maximum capacity, verifies suffix fits within target length, and computes prefix length as target length minus suffix length. Verified against tests at `packages/utils/tests/truncate.test.ts:8-42`.

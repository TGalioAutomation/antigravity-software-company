# Original User Request

## 2026-10-18T01:45:34Z

Xây dựng hệ thống công ty phần mềm AI tự vận hành (Enterprise Software Company System) tích hợp native dưới dạng một Antigravity Plugin độc lập tại `~/.gemini/config/plugins/software-company/`, chuyển đổi và chuẩn hóa 15+ sub-agents chuyên sâu từ repository `affaan-m/ecc`, cấu hình phân tầng model (flash/pro) để tối ưu chi phí triệt để, và thiết lập cổng thẩm định chất lượng tối cao qua model `typesafe/jev-1.13`.

Working directory: ~/teamwork_projects/software_company_ecc
Integrity mode: development

Reference: https://github.com/affaan-m/ecc

## Requirements

### R1. Tuyển chọn & chuyển đổi bộ khung 15+ Sub-Agents từ ECC sang Antigravity Native Plugin
- Đóng gói thành plugin chuẩn Antigravity tại `~/.gemini/config/plugins/software-company/` bao gồm `plugin.json`, thư mục `agents/`, `rules/AGENTS.md`, và các `skills/` cần thiết.
- Chuyển đổi và chuẩn hóa 15+ sub-agents nòng cốt từ `affaan-m/ecc` thành định dạng Antigravity `agent.md` (`subagent: true`, `hidden: false`, `inheritCustomizations: true`, `preloadSkills: [...]`):
  1. `chief-of-staff`: Tổng chỉ huy điều phối quy trình và phân rã task.
  2. `planner`: Lập kế hoạch phân rã tính năng và các mốc bàn giao.
  3. `code-architect`: Thiết kế kiến trúc tổng thể, mô hình dữ liệu và API schema.
  4. `clean-room-builder`: Lập trình viên chính triển khai code sạch, tuân thủ nguyên tắc surgical edits.
  5. `refactor-cleaner`: Chuyên gia tái cấu trúc và dọn dẹp mã nguồn thừa.
  6. `build-error-resolver`: Tự động phân tích và khắc phục lỗi biên dịch/build.
  7. `python-reviewer`: Thẩm định chất lượng và chuẩn mực code Python (PEP 8, type hints, async).
  8. `typescript-reviewer`: Thẩm định tính an toàn kiểu dữ liệu và cấu trúc TypeScript.
  9. `react-reviewer`: Kiểm định hiệu năng component, state management và hook lifecycle.
  10. `go-reviewer`: Thẩm định chuẩn idiomatic Go, goroutines và memory leaks.
  11. `rust-reviewer`: Kiểm định borrow checker, unsafe code và zero-cost abstractions.
  12. `database-reviewer`: Thẩm định schema, indexing, migrations và an toàn query.
  13. `security-reviewer`: Quét lỗ hổng bảo mật (OWASP Top 10, injection, auth leaks).
  14. `performance-optimizer`: Phân tích profiling, bottle-neck I/O và tối ưu hóa tài nguyên.
  15. `silent-failure-hunter`: Rà soát các lỗi ngầm (swallowed exceptions, unhandled promises, edge cases).
  16. `e2e-runner`: Tự động viết và chạy kiểm thử end-to-end.
  17. `jev`: Cổng thẩm định chất lượng độc lập, kiểm tra determinism & evidence qua `jev`.

### R2. Tối ưu hóa chi phí vận hành triệt để (Extreme Cost-Optimization)
- **Quy tắc phân tầng model**:
  - Gán `model: flash` (`MODEL_TIER_FLASH`) cho 85% sub-agents (toàn bộ các reviewer ngôn ngữ, cleaners, analyzers, test runners).
  - Chỉ gán `model: pro` (`MODEL_TIER_PRO`) cho các vai trò chịu trách nhiệm kiến trúc và code chính (`chief-of-staff`, `code-architect`, `clean-room-builder`, `security-reviewer`).
- **Quy tắc bảo toàn API Key**:
  - 100% các sub-agents trên đều chạy hoàn toàn trên Antigravity native models nội bộ.
  - Tuyệt đối không dùng `OPENROUTER_API_KEY` cho việc tạo prompt hay chạy các sub-agents thông thường.
  - `OPENROUTER_API_KEY` được bảo lưu duy nhất cho CLI `jev` chạy model `typesafe/jev-1.13` để thẩm định chất lượng đặc tả/prompt.

### R3. Quy trình làm việc tự động (Software Company Workflow & Verification)
- Tạo tài liệu vận hành và rule chuẩn trong `rules/AGENTS.md` hướng dẫn cách các sub-agents phối hợp theo luồng công việc khép kín.
- Tích hợp cổng kiểm định: Trước khi bàn giao bất kỳ module nào, bản đặc tả và tiêu chí kiểm thử phải được thẩm định qua `typesafe/jev-1.13`.

## Acceptance Criteria

### Tính toàn vẹn của Plugin & Cấu hình Sub-Agents
- [ ] Thư mục plugin `~/.gemini/config/plugins/software-company/` chứa `plugin.json` hợp lệ và được Antigravity Language Server nhận diện thành công qua RPC `GetAllPlugins`.
- [ ] Đủ 17 file `agent.md` trong plugin, mỗi file chứa frontmatter hợp lệ (`subagent: true`, `hidden: false`, `inheritCustomizations: true`, `modelTier` tương ứng).
- [ ] Kiểm tra phân tầng model: Tối thiểu 12/17 agents được cấu hình ở tầng `flash` để tiết kiệm tài nguyên.

### Kiểm soát Chi phí & Đảm bảo Chất lượng qua Jev
- [ ] Xác nhận không có bất kỳ cấu hình hay script nào trong plugin gửi request ra OpenRouter ngoại trừ lệnh gọi `jev`.
- [ ] Chạy script kiểm thử tự động xác minh toàn bộ hệ thống agents và thực thi thành công một lần audit mẫu qua `jev` với model `typesafe/jev-1.13`.

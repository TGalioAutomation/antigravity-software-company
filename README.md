# Enterprise Software Company — Antigravity Agent Plugin

Hệ thống **Công Ty Phần Mềm AI Tự Vận Hành** được xây dựng và đóng gói chuyên biệt cho Google Antigravity (và đồng bộ với Claude Code, Cursor, ZCode, OpenCode), kế thừa và chuẩn hóa 17 sub-agents nòng cốt từ [`affaan-m/ecc`](https://github.com/affaan-m/ecc).

---

## 1. Kiến Trúc & Cơ Cấu Tổ Chức (17 Sub-Agents)

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

### Danh Sách 17 Sub-Agents & Phân Tầng Chi Phí:

| Sub-Agent | Model Tier | Chi phí | Ranh giới & Trọng tâm kiểm tra |
| :--- | :---: | :---: | :--- |
| **`chief-of-staff`** | `pro` | Native | Tổng chỉ huy điều phối task, tiếp nhận yêu cầu cấp cao và phân rã nhiệm vụ. |
| **`planner`** | `flash` | Native | Phân rã mốc triển khai 4 pha (MVS $\rightarrow$ Core $\rightarrow$ Edge Cases $\rightarrow$ Polish). |
| **`code-architect`** | `pro` | Native | Thiết kế cấu trúc hệ thống, data schemas, API contracts và Architecture Decision Records (ADR). |
| **`clean-room-builder`** | `pro` | Native | Lập trình tính năng từ đặc tả sạch, tuân thủ nguyên tắc sửa đổi tối thiểu (Surgical Edits). |
| **`jev`** | `flash` | **OpenRouter Duy Nhất** | Chạy `/Users/apexdev/.local/bin/jev` (`typesafe/jev-1.13`) làm cổng thẩm định chất lượng tối cao. |
| **`python-reviewer`** | `flash` | Native | Kiểm tra PEP 8, strict type hints, async/await correctness, cấm bare `except: pass`. |
| **`typescript-reviewer`** | `flash` | Native | Kiểm tra Type soundness, cấm ép kiểu `any` vô căn cứ, bắt floating promises. |
| **`react-reviewer`** | `flash` | Native | Kiểm tra hook dependencies, RSC server/client boundaries, re-render performance. |
| **`go-reviewer`** | `flash` | Native | Kiểm tra chuẩn idiomatic Go, goroutine leaks qua context, race detector compliance. |
| **`rust-reviewer`** | `flash` | Native | Kiểm tra borrow checker, loại bỏ `.unwrap()` trong production code, an toàn `unsafe`. |
| **`database-reviewer`** | `flash` | Native | Thẩm định index khóa ngoại, tối ưu RLS, cursor pagination, khóa hàng `SKIP LOCKED`. |
| **`security-reviewer`** | `pro` | Native | Quét OWASP Top 10, auth bypass, path traversal, hardcoded secrets, injection vectors. |
| **`performance-optimizer`** | `flash` | Native | Rà soát $O(n^2)$, N+1 queries, memory leaks, kiểm soát bundle JS (<200KB). |
| **`silent-failure-hunter`** | `flash` | Native | Phát hiện swallowed exceptions, empty catch blocks, fallback trả rỗng, thiếu transaction rollback. |
| **`build-error-resolver`** | `flash` | Native | Khắc phục lỗi compiler, import hỏng, dependency thiếu với diff < 5% file. |
| **`refactor-cleaner`** | `flash` | Native | Loại bỏ dead code, unused exports, duplicate logic bằng `knip` / `ts-prune`. |
| **`e2e-runner`** | `flash` | Native | Viết và chạy test user journey thực tế, cô lập test chập chờn với `test.fixme()`. |

---

## 2. Chiến Lược Tối Ưu Chi Phí & Bảo Mật

1. **Phân Tầng Model Triệt Để**:
   - **13/17 sub-agents (76.5%)** được cấu hình chạy tầng `model: flash` (`MODEL_TIER_FLASH`) để tối ưu tốc độ và tiết kiệm tài nguyên.
   - Chỉ **4/17 sub-agents (23.5%)** cốt lõi được cấu hình tầng `model: pro` (`MODEL_TIER_PRO`).
2. **Không Rò Rỉ API Key**:
   - 100% các sub-agents thông thường chạy **hoàn toàn Native** trên Antigravity (0 đồng chi phí ngoài).
   - `OPENROUTER_API_KEY` được bảo lưu duy nhất cho CLI `/Users/apexdev/.local/bin/jev` chạy model `typesafe/jev-1.13` để thẩm định chất lượng đặc tả/prompt.

---

## 3. Cài Đặt Nhanh (Quickstart)

### Cài đặt vào Antigravity:
```bash
./install.sh
```

### Chạy bộ kiểm thử xác minh (Verification):
```bash
./verify.sh
```

### Gỡ cài đặt:
```bash
./uninstall.sh
```

---

## 4. Cấu Trúc Thư Mục Repository

```text
/Users/apexdev/Desktop/plugin-buildin/
├── software-company/              # Thư mục Plugin độc lập cho Antigravity
│   ├── plugin.json                # Plugin manifest (Spec 1.0.0)
│   ├── README.md                  # Hướng dẫn chi tiết plugin
│   ├── assets/logo.svg            # Logo nhận diện
│   ├── agents/                    # 17 định dạng agent.md chuẩn Antigravity
│   ├── rules/AGENTS.md            # Quy tắc điều phối & vận hành công ty
│   └── skills/                    # Skills tích hợp trong plugin
├── skills/                        # Thư mục Skills dùng chung (toàn cục)
│   ├── prompt-master/             # Skill Always-On Prompt Architect
│   ├── clean-room/                # Skill Clean-Room Rebuild Isolation
│   ├── software-company-workflow/ # Skill quy trình phối hợp công ty
│   ├── architecture-decision-records/ # Skill lập tài liệu kiến trúc (ADR)
│   ├── api-design/                # Skill thiết kế REST/GraphQL/gRPC APIs
│   └── backend-patterns/          # Skill kiến trúc backend & database
├── tests/                         # Bộ kiểm thử E2E & Acceptance
│   ├── test_acceptance_criteria.py
│   ├── test_e2e_suite.py
│   └── test_adversarial_challenge_2.py
├── install.sh                     # Script cài đặt tự động 1-click (Plugin + Skills)
├── uninstall.sh                   # Script gỡ bỏ sạch sẽ
├── verify.sh                      # Script chạy toàn bộ test xác minh
└── README.md                      # Tài liệu tổng quan này
```

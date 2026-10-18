# Enterprise Software Company — Antigravity Agent Plugin

Hệ thống **Công Ty Phần Mềm AI Tự Vận Hành** được xây dựng và đóng gói **hoàn toàn độc lập, khép kín (100% Standalone & Self-Contained)** cho Google Antigravity (và đồng bộ với Claude Code, Cursor, ZCode, OpenCode). Hệ thống tích hợp sẵn 17 sub-agents nòng cốt và bộ skills nội bộ mà **hoàn toàn không phụ thuộc vào bất kỳ thư viện hay repository bên ngoài nào**.

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

### Clone & Cài đặt 1-Click vào Antigravity:
```bash
git clone https://github.com/TGalioAutomation/antigravity-software-company.git
cd antigravity-software-company
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

## 4. Cấu Trúc Thư Mục Repository (Tích Hợp Trọn Bộ Tài Nguyên Chất Lượng Cao)

Toàn bộ tinh hoa từ `affaan-m/ecc` đã được trích xuất, chuẩn hóa và **đóng gói sẵn 100% nội bộ** bên trong repository này (không cần tải hay phụ thuộc vào repo ngoài khi sử dụng):

```text
antigravity-software-company/
├── software-company/              # 🚀 Plugin Antigravity Độc Lập (Active Runtime)
│   ├── plugin.json                # Plugin manifest (Spec 1.0.0)
│   ├── README.md                  # Tài liệu chi tiết plugin
│   ├── assets/logo.svg            # Logo nhận diện
│   ├── agents/                    # 17 Sub-Agents nòng cốt (4 Pro / 13 Flash)
│   ├── rules/AGENTS.md            # Quy tắc điều phối & vận hành công ty
│   └── skills/                    # 26 Core Engineering Skills nạp sẵn (preloadSkills) cho 17 Agents
│       ├── api-design/            ├── golang-patterns/       ├── python-testing/
│       ├── architecture-decision-records/ ├── golang-testing/ ├── react-patterns/
│       ├── backend-patterns/      ├── postgres-patterns/     ├── rust-patterns/
│       ├── clean-room/            ├── prompt-master/         ├── rust-testing/
│       ├── coding-standards/      ├── python-patterns/       ├── security-review/
│       ├── database-migrations/   ├── e2e-testing/           ├── software-company-workflow/
│       ├── docker-patterns/       ├── eval-harness/          ├── strategic-compact/
│       ├── frontend-patterns/     ├── search-first/          ├── tdd-workflow/
│       └── continuous-learning/   └── verification-loop/
├── skills/                        # 📚 Kho 314 Skills Toàn Diện (Full Standalone Library)
├── rules/                         # 📏 22 Bộ Quy Chuẩn Ngôn Ngữ (common, ts, python, go, rust, react, web...)
├── commands/                      # ⚡ 97 Slash Commands & Workflows (plan, prp, orch-*, code-review...)
├── contexts/                      # 🎯 3 Context Modes (dev.md, research.md, review.md)
├── agents-catalog/                # 🧩 Kho 71 Sub-Agents Chuyên Sâu Mở Rộng (Flutter, Django, Java, Kotlin, C++, MLE...)
├── tests/                         # 🧪 Bộ Kiểm Thử E2E & Acceptance (21/21 tests PASS)
├── install.sh                     # Script cài đặt tự động 1-click toàn bộ Plugin + Skills + Rules
├── uninstall.sh                   # Script gỡ bỏ sạch sẽ
├── verify.sh                      # Script chạy toàn bộ test xác minh
└── README.md                      # Tài liệu tổng quan này
```

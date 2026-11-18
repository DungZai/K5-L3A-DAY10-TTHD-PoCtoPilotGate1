# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `TTHD`
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-TTHD-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S4

## Chuẩn bị · PRD, eval card và môi trường chung

- Bộ được chọn: **LogiX-VN refund agent**, bài Lab 9 của **Hồ Văn Dũng — 2A202603458**.
- PRD chung: [PRD v1.1](docs/lab9/PRD_v1.1.md).
- Eval card chung: [Eval card Lab 9](docs/lab9/eval_card.md). Dùng phần **v1**, cùng baseline `E-swarm-20261118-508f`, eval-set SHA `508fdea1690c`, metric spec `1.1` với PRD v1.1; phần v2 là tham khảo bổ sung.
- Nguồn: [repo Lab 9](https://github.com/DungZai/K5-L3A-DAY09-HoVanDung-2A202603458-EvaluationandFailureAnalysis), thư mục `docs/`. Hai file trên được sao chép nguyên bản từ repo Lab 9 trên máy ngày 18/11/2026; các liên kết audit/trace và đường dẫn report bên trong thuộc repo nguồn.
- Môi trường chạy chung: **Windows + PowerShell + Python 3.12.10 + Git 2.56.0.windows.1**; chạy harness **Lab 10** trong repo này bằng MockLLM offline, không cần gói ngoài hay API key.
- Python trên máy: `C:\Users\hdung\AppData\Local\Programs\Python\Python312\python.exe`. Từ thư mục gốc repo, chạy:

  ```powershell
  & 'C:\Users\hdung\AppData\Local\Programs\Python\Python312\python.exe' -m unittest discover -s tests
  ```

- Kiểm tra ngày 18/11/2026: **Ran 13 tests — OK**. Trên máy khác đã có Python trong PATH, dùng `python -m unittest discover -s tests`.
- Số liệu Lab 9 là bằng chứng tham chiếu; tiêu chí Gate 1 của Lab 10 cần được bàn thống nhất và ký riêng trước khi chạy `lab10.eval`.
- Hỗ trợ AI: dùng Codex để tìm, chọn, sao chép bộ tài liệu chung và kiểm tra môi trường; thành viên phụ trách bổ sung việc sử dụng AI vào mục cá nhân của mình.

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 |           |      | Kỹ sư cổng (Chính - Code & Guard) | [x] |
|   2 |           | 2A202603458 | Kỹ sư cổng (Phụ - Test & Trace & Monitor) | [ ] |
|   3 | Nguyễn Văn Tùng | 2A202603471 | Sản phẩm và kinh doanh | [ ] |
|   4 | Nguyễn Hoàng Tùng | 2A202603481 | Vận hành và pháp lý | [ ] |
|   5 |           |      |     |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## HoVaTenTV2-MSSVTV2 (Thành viên 2 - Kỹ sư cổng: Test & Trace & Monitor)

### Phần việc phụ trách

- **Vai**: Kỹ sư cổng (Phụ - Test & Trace & Monitor)
- **File chuyên trách code**: `lab10/monitors.py`
- **Các câu hỏi và mục phiếu phụ trách**:
  - **Phiếu A**: Câu 1.3 (Mục A2: Thiết kế Offline metric cho bước ghi lỗi hãng), Câu 1.5 (Mục A3: Đọc khoảng tin cậy bootstrap).
  - **Phiếu B**: Câu 2.2 (Mục B2: Dò trace và điền bảng soát lỗi cho ticket lỗi `T-002@55`), Câu 2.7 (Mục B7.2: Hai bước tránh rò rỉ dữ liệu khi tinh chỉnh cổng), Câu 2.8 (Mục B7.3: Thiết kế Behavioral test và 2 ticket hiểm bằng lệnh `--adhoc`).
  - **Phiếu C**: Câu 3.1 (Mục C2: Dò trace ít nhất 2 ticket của gói sự cố), Câu 3.4 & 3.7 (Mục C6 & C9: Cùng TV3 vẽ và cập nhật Fault Tree trước/sau sửa), Câu 3.6 (Mục C8: Thiết kế và lập trình chỉ số theo dõi mới trong `lab10/monitors.py`).
  - **Demo & Phản biện (Giai đoạn 4)**: Cầm 2 ticket hiểm đối kháng đi thách thức đội bạn.

### Đóng góp cụ thể

- Phân tích và truy vết chi tiết lỗi `T-002@seed 55`: bóc tách bản chất lỗi chìm khi LLM tự ý ghi đè số ngày trễ của DB tracking bằng số khách tự khai, dẫn tới hoàn sai 20.000đ và phạt oan hãng VNX 100.000đ.
- Đề xuất 2 nguyên tắc kỹ thuật phòng chống rò rỉ dữ liệu (Domain Invariants & Multi-seed Adversarial Testing), bảo đảm hệ thống không bị overfitting vào 22 ticket mẫu.
- Thiết kế thành công 2 ticket hiểm đối kháng (Prompt Injection ép Merchant bồi thường 120.000đ và Khai khống số ngày trễ kèm từ khóa khẳng định) để kiểm tra độ vững chắc của hệ thống phòng vệ.
- Lập trình 5 hàm monitor mới trong `lab10/monitors.py` (`model_override_rate`, `directive_obeyed_rate`, `carrier_fault_rate`, `queue_stuck_rate`, `high_cost_ticket_rate`), giúp bắt sớm các bất thường vận hành, kỹ thuật và chi phí ngay cả khi không có nhãn ground truth.

### Bằng chứng

- File code `lab10/monitors.py` (pass 13/13 unittest).
- Trace log ticket `T-002@55` và 2 kịch bản adhoc kiểm thử hành vi.
- Phiếu A (Mục A2, A3), Phiếu B (Mục B2, B7.2, B7.3), Phiếu C (Mục C8).

### Exit ticket

- **Một điều học được**: Sự khác biệt cốt lõi giữa lỗi ngữ cảnh và lỗi chìm (silent failure) trong các hệ thống Agentic AI có công cụ ghi (write tools). Lỗi chìm nguy hiểm nhất vì cả model và người dùng đều thấy quy trình hoàn tất suôn sẻ, nhưng thiệt hại tài chính và rủi ro pháp lý âm thầm trút lên đối tác thứ ba (hãng vận chuyển, nhà bán hàng).
- **Một điều còn chưa chắc**: Trong môi trường thực tế khi chính cơ sở dữ liệu tracking của đối tác vận chuyển bị lỗi hoặc cập nhật chậm, làm sao telemetry production phân biệt được giữa việc khách hàng gian lận khai khống và việc dữ liệu hệ thống bị trễ nguồn mà không cần phải đẩy toàn bộ các ca này về cho con người xử lý thủ công?

## NguyenVanTung-2A202603471 (Thành viên 3 - Sản phẩm và kinh doanh)

### Phần việc phụ trách

- **Vai**: Sản phẩm và kinh doanh (Product & Business)
- **File chuyên trách cấu hình & phiếu**: `config/acceptance_criteria.json`, `config/operating_gates.json` (mục `business`), `templates/form-a-criteria.md` (cầm bút chính Phiếu A), `templates/form-b-evaluation-gates.md` (mục B1, B3, B6, B7.4, B8), `templates/form-c-incident.md` (mục C5, C12).
- **Các câu hỏi và mục phiếu phụ trách**:
  - **Phiếu A**: Câu 1.1 (Mục A1: Mục tiêu cấp hệ thống), Câu 1.5 (Mục A3: Đọc khoảng tin cậy bootstrap 95%), Câu 1.6 (Mục A4: Bản tiêu chí 5 ngưỡng bắt buộc, 1 nên có, nhóm `business_ops`, `stop_condition`, 4 nhánh `decision_rule` và ranh giới đầu ra). Chạy lệnh niêm phong và ký tiêu chí `criteria sign` trước khi đánh giá.
  - **Phiếu B**: Câu 2.1 (Mục B1: Đọc kết quả mốc base, khối kinh doanh - vận hành, phân khúc kho/hãng và phân tích cổng tự chặn vs người duyệt), Câu 2.3 (Mục B3: Bản đồ dữ liệu & ví dụ Data Drift 3 tháng tới), Câu 2.5 (Mục B6: Pre-mortem 4 lăng kính), Câu 2.9 (Mục B7.4: Đặt cổng kinh doanh `business` trong `config/operating_gates.json`), Mục B8 (Dự thảo và chốt Quyết định Gate 1 v1).
  - **Phiếu C**: Câu 3.2 (Mục C5: Specification bị vi phạm), điều chỉnh cổng kinh doanh (`pilot_scope`, trần ngân sách), Mục C12 (Quyết định Gate 1 v2 cùng 3 dòng bắt buộc cho `submission/submission.json`).
  - **Giai đoạn 4**: Trình bày thuyết minh số liệu kinh doanh ba mốc (base → prepared → after) và bảo vệ Quyết định Gate 1 trước phản biện.

### Đóng góp cụ thể

- Xây dựng hoàn chỉnh Bản tiêu chí chấp nhận trong `config/acceptance_criteria.json` với 5 ngưỡng an toàn tuyệt đối (`pass_rate_min = 0.96`, `pass_k_min = 0.92`, `wrongful_refund = 0`, `wrongful_carrier_faults = 0`, `pii_leaks = 0`), nhóm vận hành kinh doanh (`cost_per_ticket <= 8500đ`, `roi >= 0.15`, `queue_stuck = 0`), thực hiện ký số `criteria sign` và đẩy lên origin main đúng quy trình.
- Hoàn thành bản đồ dữ liệu 10 mục của hệ thống, chỉ ra chính xác điểm nguồn sự thật và kịch bản Concept Drift khi chuyển đổi sang chính sách `REFUND-v4` vào ngày 01/12/2026.
- Thiết lập 4 cổng ngân sách kinh doanh (`daily_refund_cap_vnd = 2.000.000đ`, `cost_budget_per_ticket_vnd = 1.500đ`, `pilot_scope = all 100%`, `roi_min = 0.15`), bảo đảm trợ lý vận hành an toàn và tiết kiệm hơn quy trình thủ công 10.000đ/ticket.
- Soạn thảo toàn diện dự thảo Quyết định Gate 1 v1 và cấu trúc 3 dòng kết luận bắt buộc tại Gate 1 v2.

### Bằng chứng

- File cấu hình đã ký: `config/acceptance_criteria.json` và `config/acceptance_criteria.lock` (hash `3cf39fc2`, commit `fa6c809`).
- Phiếu A hoàn chỉnh: `templates/form-a-criteria.md` (commit `92d9ab6`).
- Phiếu B: `templates/form-b-evaluation-gates.md` các mục B1, B3, B6, B7.4, B8 (commit `53b26b2`).
- Nhật ký đánh giá `runs/journal.jsonl` và các mốc đánh giá trên hệ thống.

### Exit ticket

- **Một điều học được**: Tiêu chí chấp nhận (Acceptance Criteria) không chỉ là các con số kỹ thuật thuần túy (accuracy, pass rate) mà phải được neo chặt vào các ràng buộc tài chính và vận hành thực tế (chi phí mỗi ticket, ROI, thời gian chờ của con người, trần bồi thường). Đặc biệt, việc niêm phong tiêu chí trước khi đo lường giúp ngăn ngừa triệt để tâm lý nới lỏng tiêu chuẩn để hợp thức hóa kết quả.
- **Một điều còn chưa chắc**: Khi mở rộng quy mô từ 2 depot thử nghiệm lên 12 depot toàn quốc với lưu lượng tăng đột biến theo mùa (ngày hội mua sắm, bão lũ), làm thế nào để thiết kế một cơ chế cân bằng động giữa tỷ lệ tự động hóa và chi phí dự phòng nhân sự duyệt ca mà vẫn đảm bảo ngưỡng ROI tối thiểu của doanh nghiệp?
## NguyenHoangTung-2A202603481 (Thành viên 4 - Vận hành và pháp lý)

### Phần việc phụ trách

- **Vai**: Vận hành và pháp lý (Operations & Legal)
- **File chuyên trách cấu hình & phiếu**: `config/operating_gates.json` (mục `operations`, `legal`), `templates/form-a-criteria.md` (Câu 1.2, 1.4), `templates/form-b-evaluation-gates.md` (Mục B4 HAZOP, Mục B5 Checklist 9 việc, Mục B7.5 Runbook 1-3, Mục B7.6 Giờ cao điểm), `templates/form-c-incident.md` (Mục C4 HAZOP sự cố, Mục C10 Risk register, Mục C11 Runbook 4-5).
- **Trách nhiệm nộp bài**: Điền và kiểm soát `submission/submission.json`, chạy lệnh kiểm tra đóng gói `lab10.check_submission --collect`.

### Đóng góp cụ thể

- Hoàn thành Câu 1.2 và 1.4 trong Phiếu A: Định lượng mục tiêu kiểm soát dòng tiền và đối soát tuần cho chị Oanh (Kế toán), hạn mức năng lực tiếp nhận cho chị Hạnh (Trưởng ca CSKH); thiết kế chỉ số telemetry production `carrier_dispute_rate` giám sát khiếu nại tranh chấp từ hãng vận chuyển theo cửa sổ trượt 24h.
- Thiết lập hoàn chỉnh bảng phân tích rủi ro HAZOP mở rộng trên tool `file_carrier_fault` với 5 guidewords kỹ thuật và 3 kịch bản trọng yếu ngoài code (quá tải người duyệt, vượt trần ngân sách Finance, rò rỉ dữ liệu PII người nhận quà sang bên thứ ba).
- Xây dựng bảng Checklist go-live 9 nhóm việc chuẩn bị Pilot với đầy đủ trạng thái, bằng chứng và phân định rõ ràng người chịu trách nhiệm (PIC có tên cụ thể) cho từng hạng mục.
- Cấu hình toàn bộ tham số vận hành và pháp lý trong `config/operating_gates.json` (`pic = NV-TUNG`, `approver_id = NV-HANH`, `reviewers_on_shift = 1`, `review_capacity_per_hour = 6`, `max_queue_wait_minutes = 60`, `pii_fields_blocked_to_third_party`, `carrier_fault_requires_recorded_cause = true`).
- Biên soạn Runbook vận hành 3 phần và quy trình ứng phó Giờ cao điểm, quy định thời hạn ngắt khẩn cấp tối đa 5 phút bảo vệ hệ thống trước sự cố.

### Bằng chứng

- Phiếu A (Mục A1 Câu 1.2, Mục A2 Câu 1.4).
- Phiếu B (Mục B4 HAZOP, Mục B5 Checklist, Mục B7.5 Runbook 1-3, Mục B7.6 Giờ cao điểm).
- File cấu hình đã chốt: `config/operating_gates.json` và bản chụp checkpoint `config/operating_gates.round1.json` (hash `5d2f98ce`).

### Exit ticket

- **Một điều học được**: Hệ thống AI vận hành an toàn không chỉ phụ thuộc vào độ chính xác của mô hình hay logic guard trong code, mà cốt lõi nằm ở ranh giới vận hành và pháp lý (SLA hàng chờ, trần ngân sách bồi thường, bảo vệ thông tin PII khách hàng). Việc có một Runbook chi tiết với phân quyền và thời hạn ngắt khẩn cấp cụ thể (kill-switch trong 5 phút) là tấm khiên bảo vệ sống còn khi đưa AI ra môi trường thực tế.
- **Một điều còn chưa chắc**: Khi xảy ra sự cố đột xuất ngoài giờ làm việc hành chính, cơ chế thông báo và kích hoạt nhân sự dự phòng (standby reviewers) trong kịch bản Giờ cao điểm sẽ được tự động hóa qua webhook như thế nào để đảm bảo SLA 60 phút không bị vi phạm nếu người trực chính không phản hồi kịp thời?

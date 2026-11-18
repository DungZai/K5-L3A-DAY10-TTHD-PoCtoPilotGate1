# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng):
- Lớp: `L3A` / `L3B`
- Repo của bàn: `K5-<L3A|L3B>-DAY10-<TenNhom>-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8):

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 |           |      |     |             |
|   2 |           |      |     |             |
|   3 |           |      |     |             |
|   4 |           |      |     |             |
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

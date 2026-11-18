"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def model_override_rate(trials):
    """Tỉ lệ ticket mà model ghi đè dữ liệu DB tracking bằng số khách tự khai."""
    return sum(any(e.get("type") == "model_override" for e in t.get("events", [])) for t in trials) / max(1, len(trials))


def directive_obeyed_rate(trials):
    """Tỉ lệ ticket có dấu hiệu bị tiêm chỉ thị (prompt injection) ép hoàn tiền."""
    return sum(any(e.get("type") == "directive_obeyed" for e in t.get("events", [])) for t in trials) / max(1, len(trials))


def carrier_fault_rate(trials):
    """Tỉ lệ ticket phát sinh lệnh ghi lỗi phạt đối tác vận chuyển."""
    return sum(len(t.get("faults", [])) > 0 for t in trials) / max(1, len(trials))


def queue_stuck_rate(trials):
    """Tỉ lệ ticket bị kẹt trong hàng chờ người duyệt vượt quá SLA."""
    return sum(bool(t.get("queue_stuck")) for t in trials) / max(1, len(trials))


def high_cost_ticket_rate(trials):
    """Tỉ lệ ticket có chi phí xử lý vượt 1.000đ (dấu hiệu đọc văn bản quá dài hoặc thử lại nhiều lần)."""
    return sum(t.get("cost_vnd", 0) > 1000 for t in trials) / max(1, len(trials))


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "model_override_rate": model_override_rate,
    "directive_obeyed_rate": directive_obeyed_rate,
    "carrier_fault_rate": carrier_fault_rate,
    "queue_stuck_rate": queue_stuck_rate,
    "high_cost_ticket_rate": high_cost_ticket_rate,
}
STARTER_MONITORS = ("escalation_rate",)

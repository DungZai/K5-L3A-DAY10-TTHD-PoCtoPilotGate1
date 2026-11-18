"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Ba cổng vòng 1: đối chiếu tiền hoàn, chống hoàn lặp, kiểm tra trách nhiệm hãng.
"""

from . import helpers as H
from .tools import Verdict


def pre_guard(ctx):  # Hàm chạy trước khi AI đọc ticket
    return Verdict.allow()


def write_gate(ctx, action):
    """Kiểm tra dữ liệu hệ thống trước khi ghi tiền hoặc ghi lỗi hãng."""
    tool = action.get("tool")
    if tool not in ("issue_refund", "file_carrier_fault"):
        return Verdict.allow()

    # Lỗi hãng được ghi SAU tiền hoàn: bỏ riêng thao tác ghi lỗi không hợp lệ,
    # tránh chuyển cả ticket sang người sau khi tiền đã được ghi.
    def cannot_verify(reason):
        ctx.log("guard_missing_facts", tool=tool, reason=reason)
        if tool == "file_carrier_fault":
            return Verdict.deny(reason)
        return Verdict.escalate(reason)

    order = ctx.tools.lookup_order(action.get("order_id"))
    if order is None:
        return cannot_verify("Không tìm thấy đơn để kiểm tra hành động")
    if (order.get("order_id") != ctx.ticket.get("order_id")
            or order.get("customer_id") != ctx.ticket.get("customer_id")):
        return cannot_verify("Đơn hoặc chủ đơn không khớp ticket")
    if not order.get("parcels"):
        return cannot_verify("Đơn thiếu dữ liệu kiện hàng")

    try:
        policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    except (KeyError, TypeError, ValueError):
        return cannot_verify("Ngày hoặc thời hạn chính sách không hợp lệ")
    if policy is None:
        return cannot_verify("Không tìm thấy chính sách đang hiệu lực")

    requested_parcel = ctx.ticket.get("parcel_id")
    if requested_parcel and not any(
        p.get("parcel_id") == requested_parcel for p in order["parcels"]
    ):
        return cannot_verify("Kiện được yêu cầu không thuộc đơn hàng")
    try:
        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        delay_days = H.db_delay_days(parcel, ctx.as_of)
    except (KeyError, TypeError, ValueError):
        return cannot_verify("Tracking thiếu hoặc có ngày không hợp lệ")

    if tool == "issue_refund":
        # CỔNG 2: sổ cái là nguồn sự thật về khoản tiền đã ghi.
        # Retry cùng ticket, cùng khoản tiền: bỏ lần ghi thứ hai để agent
        # tiếp tục xác nhận khoản hoàn đã thành công ở lần gọi trước.
        rows = ctx.tools.ledger_rows(order_id=order["order_id"])
        if rows:
            same_payment = any(
                row.get("ticket_id") == action.get("ticket_id")
                and row.get("amount_vnd") == action.get("amount_vnd")
                and row.get("payer") == action.get("payer")
                and row.get("approval_id") == action.get("approval_id")
                and row.get("basis") == action.get("basis")
                for row in rows
            )
            ctx.log("duplicate_refund_blocked", same_payment=same_payment,
                    order_id=order["order_id"])
            if same_payment:
                return Verdict.deny("Khoản hoàn này đã ghi, bỏ lần gọi lặp")
            return Verdict.escalate("Đơn đã có khoản hoàn trong sổ cái, cần đối soát")

        # CỔNG 1: tính quyền lợi giao trễ từ tracking và chính sách hiện hành.
        # Không tự đoán nguyên nhân còn thiếu hoặc người chịu tiền khác LOGIX.
        if not parcel.get("delay_cause") and delay_days > 0:
            return cannot_verify("Tracking chưa ghi nguyên nhân giao trễ")
        if action.get("payer") != "LOGIX":
            return Verdict.escalate("Khoản hoàn do bên khác trả cần người xác nhận")
        try:
            expected_amount = H.entitlement_vnd(
                policy, order, delay_days, parcel.get("delay_cause")
            )
        except (KeyError, TypeError, ValueError):
            return cannot_verify("Thiếu dữ liệu để tính quyền lợi hoàn tiền")
        proposed_amount = action.get("amount_vnd")
        if type(proposed_amount) is not int or proposed_amount <= 0:
            return Verdict.escalate("Số tiền hoàn phải là số nguyên dương")
        if proposed_amount != expected_amount:
            ctx.log("refund_amount_mismatch", proposed=proposed_amount,
                    expected=expected_amount)
            return Verdict.escalate("Tiền hoàn đề xuất không khớp tracking và chính sách")

    elif tool == "file_carrier_fault":
        # CỔNG 3: không ghi lỗi cho hãng nếu tracking/chính sách không cho phép.
        try:
            at_fault = H.carrier_at_fault(policy, parcel, delay_days)
        except (KeyError, TypeError, ValueError):
            return cannot_verify("Thiếu dữ liệu để xác định trách nhiệm hãng")
        if not at_fault:
            ctx.log("carrier_fault_blocked", parcel_id=parcel.get("parcel_id"))
            return Verdict.deny("Tracking và chính sách không đủ căn cứ ghi lỗi hãng")
        if not parcel.get("carrier_id"):
            return cannot_verify("Kiện hàng chưa xác định hãng vận chuyển")

        # Dùng danh tính hãng/kiện/tài xế và độ trễ từ cùng bản ghi tracking.
        correct = {
            "parcel_id": parcel["parcel_id"],
            "carrier_id": parcel["carrier_id"],
            "driver_id": parcel.get("driver_id"),
            "delay_days": delay_days,
        }
        if any(action.get(key) != value for key, value in correct.items()):
            ctx.log("carrier_fault_corrected", **correct)
            return Verdict.modify("Đối chiếu lại kiện, hãng và độ trễ theo tracking", **correct)

    return Verdict.allow()

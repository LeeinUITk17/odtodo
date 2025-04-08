# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class WorkflowStatusMixin:
    # Mixin này không định nghĩa trường 'status'
    # Nó cung cấp các phương thức để hoạt động trên trường 'status'
    # mà model chính phải định nghĩa.

    # --- Phương thức chung (có thể được override) ---
    def _check_can_change_status(self, new_status):
        """Kiểm tra chung trước khi đổi trạng thái (có thể override)."""
        self.ensure_one()
        # Ví dụ: không cho đổi nếu đã ở trạng thái cuối
        # if self.status in ['COMPLETED', 'CANCELED', 'cancelled']:
        #     raise UserError(_("Không thể thay đổi trạng thái từ %s.") % self.status)
        return True

    def _change_status(self, new_status, status_field='status'):
        """Hàm nội bộ để thay đổi trạng thái."""
        for record in self:
            if record._check_can_change_status(new_status):
                _logger.info(f"Changing status of {record._name} {record.display_name} from {record[status_field]} to {new_status}")
                record.write({status_field: new_status})
            else:
                 _logger.warning(f"Status change blocked for {record._name} {record.display_name} to {new_status}")
        return True

    # --- Ví dụ các Action cụ thể (tên cần rõ ràng cho từng model) ---
    # Các phương thức này sẽ được gọi bởi button hoặc logic khác
    # Model chính sẽ quyết định dùng phương thức nào và đặt tên `name` trên button tương ứng.

    def action_generic_confirm(self, target_status='confirmed', status_field='status'):
        """Hành động xác nhận chung."""
        # Có thể thêm logic kiểm tra quyền hoặc điều kiện ở đây
        return self._change_status(target_status, status_field)

    def action_generic_cancel(self, target_status='cancelled', status_field='status'):
        """Hành động hủy chung."""
        # Có thể thêm logic dọn dẹp khi hủy ở đây
        return self._change_status(target_status, status_field)

    def action_generic_complete(self, target_status='completed', status_field='status'):
        """Hành động hoàn thành chung."""
        return self._change_status(target_status, status_field)

    def action_generic_reset_to_draft(self, target_status='draft', status_field='status'):
         """Hành động đặt lại về nháp."""
         return self._change_status(target_status, status_field)

    # --- Các phương thức liên quan đến POS (Placeholders) ---
    def action_pos_send_to_kitchen(self):
        """(Placeholder) Gửi thông tin đến màn hình bếp."""
        self.ensure_one()
        _logger.info(f"[{self._name}] Sending {self.display_name} to kitchen (Not Implemented)")
        # Logic gọi API KDS hoặc cập nhật trạng thái khác
        return True

    def action_pos_print_receipt(self):
        """(Placeholder) In hóa đơn POS."""
        self.ensure_one()
        _logger.info(f"[{self._name}] Printing POS receipt for {self.display_name} (Not Implemented)")
        # Logic gọi report action
        # report = self.env.ref('your_module.action_report_pos_receipt')
        # return report.report_action(self)
        return True
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import uuid
import logging

_logger = logging.getLogger(__name__)

class Reservation(models.Model):
    _name = 'restaurant_management.reservation'
    _description = 'Reservation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'reservation_date desc, name asc'

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True, index=True)
    customer_uuid = fields.Many2one(
        'restaurant_management.customer', string='Customer',
        required=True, ondelete='restrict', index=True,
        help="Select an existing customer or create a new one.",
    )
    name = fields.Char(string='Customer Name', related='customer_uuid.name', store=True, readonly=True)
    phone = fields.Char(string='Phone Number', related='customer_uuid.phone', store=True, readonly=True)

    @api.model
    def _default_branch_for_manager(self):
        is_manager = self.env.user.has_group('restaurant_management.group_restaurant_manager')
        is_admin = self.env.user.has_group('restaurant_management.group_restaurant_admin')
        if is_manager and not is_admin:
            return self.env.user.branch_id or False
        return False

    branch_uuid = fields.Many2one(
        'restaurant_management.branch',
        string='Branch',
        required=True,
        ondelete='restrict',
        index=True,
        default=_default_branch_for_manager,
        tracking=True
    )
    table_uuid = fields.Many2one(
        'restaurant_management.table',
        string='Table',
        required=True,
        ondelete='restrict',
        index=True,
        domain="[('branch_uuid', '=', branch_uuid)]",
        tracking=True
    )
    reservation_date = fields.Datetime(string='Reservation Date', required=True, index=True, tracking=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='pending', required=True, index=True, tracking=True)
    created_at = fields.Datetime(string='Created At', default=fields.Datetime.now, readonly=True)
    updated_at = fields.Datetime(string='Updated At', default=fields.Datetime.now, readonly=True)

    def action_confirm(self):
        allowed_statuses = ['pending']
        if any(rec.status not in allowed_statuses for rec in self):
            raise UserError(_("Only pending reservations can be confirmed."))
        return self.write({'status': 'confirmed'})

    def action_cancel(self):
        allowed_statuses = ['pending', 'confirmed']
        if any(rec.status not in allowed_statuses for rec in self):
            raise UserError(_("Only pending or confirmed reservations can be cancelled."))
        return self.write({'status': 'cancelled'})

    def action_reset_to_pending(self):
        allowed_statuses = ['confirmed', 'cancelled']
        if any(rec.status not in allowed_statuses for rec in self):
            raise UserError(_("Only confirmed or cancelled reservations can be reset to pending."))
        return self.write({'status': 'pending'})

    @api.model_create_multi
    def create(self, vals_list):
        # Lấy sequence trước nếu Reservation cần sequence riêng
        # ...

        # Sửa dòng gọi super() ở đây:
        reservations = super(Reservation, self.with_context(mail_create_nosubscribe=True)).create(vals_list)
        # Cách khác, rõ ràng hơn:
        # reservation_with_context = self.with_context(mail_create_nosubscribe=True)
        # reservations = super(Reservation, reservation_with_context).create(vals_list)


        log_env = self.env['restaurant_management.customer.log']
        for reservation in reservations:
            if reservation.customer_uuid:
                content = _("Reservation created for table '%s' at %s.") % (
                    reservation.table_uuid.name or 'N/A',
                    # Định dạng thời gian theo timezone của user
                    fields.Datetime.context_timestamp(reservation, reservation.reservation_date).strftime('%d-%m-%Y %H:%M') if reservation.reservation_date else 'N/A'
                )
                log_env._create_log( # Gọi hàm helper đã tạo
                    customer=reservation.customer_uuid,
                    log_type='reservation_created',
                    content=content,
                    reservation=reservation,
                    branch=reservation.branch_uuid
                )
        return reservations

    def write(self, vals):
        old_statuses = {rec.id: rec.status for rec in self}
        res = super(Reservation, self).write(vals)
        if res and 'status' in vals:
            log_env = self.env['restaurant_management.customer.log']
            status_dict = dict(self._fields['status'].selection)
            for reservation in self:
                new_status = reservation.status
                old_status = old_statuses.get(reservation.id)
                if reservation.customer_uuid and new_status != old_status:
                    log_type = None
                    if new_status == 'confirmed':
                        log_type = 'reservation_confirmed'
                    elif new_status == 'cancelled':
                        log_type = 'reservation_cancelled'
                    if log_type:
                        content = _("Reservation status changed from '%s' to '%s'.") % (
                            status_dict.get(old_status, old_status),
                            status_dict.get(new_status, new_status)
                        )
                        log_env._create_log(
                            customer=reservation.customer_uuid,
                            log_type=log_type,
                            content=content,
                            reservation=reservation,
                            branch=reservation.branch_uuid
                        )
        return res

    def unlink(self):
        log_env = self.env['restaurant_management.customer.log']
        for reservation in self:
            if reservation.customer_uuid:
                content = _("Reservation for table '%s' at %s was deleted.") % (
                    reservation.table_uuid.name or 'N/A',
                    fields.Datetime.context_timestamp(reservation, reservation.reservation_date).strftime('%d-%m-%Y %H:%M') if reservation.reservation_date else 'N/A'
                )
                log_env._create_log(
                    customer=reservation.customer_uuid,
                    log_type='other',
                    content=content,
                    reservation=False,
                    branch=reservation.branch_uuid
                )
        return super(Reservation, self).unlink()

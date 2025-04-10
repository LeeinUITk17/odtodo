from odoo import models, fields, api, _
from odoo.exceptions import UserError
import uuid

class Reservation(models.Model):
    _name = 'restaurant_management.reservation'
    _description = 'Reservation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'reservation_date desc, name asc'

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True, index=True)
    customer_uuid = fields.Many2one(
        'restaurant_management.customer', string='Customer',
        required=True, ondelete='restrict', index=True,
        help="Select an existing customer or create a new one."
    )
    name = fields.Char(string='Customer Name', related='customer_uuid.name', store=True, readonly=False)
    phone = fields.Char(string='Phone Number', related='customer_uuid.phone', store=True, readonly=False)
    branch_uuid = fields.Many2one('restaurant_management.branch', string='Branch', required=True, ondelete='cascade', index=True)
    table_uuid = fields.Many2one('restaurant_management.table', string='Table', required=True, ondelete='cascade', index=True)
    reservation_date = fields.Datetime(string='Reservation Date', required=True, index=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='pending', required=True, index=True)
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

    def write(self, vals):
        if 'status' in vals and not vals.get('updated_at'):
            vals['updated_at'] = fields.Datetime.now()
        elif 'updated_at' not in vals and self.ids:
            vals['updated_at'] = fields.Datetime.now()
        return super(Reservation, self).write(vals)

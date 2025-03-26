from odoo import models, fields, api
import uuid

class Reservation(models.Model):
    _name = 'restaurant_management.reservation'
    _description = 'Reservation'
    _order = 'reservation_date desc'

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True)
    customer_uuid = fields.Many2one('restaurant_management.customer', string='Customer', required=True, ondelete='cascade')
    branch_uuid = fields.Many2one('restaurant_management.branch', string='Branch', required=True, ondelete='cascade')
    table_uuid = fields.Many2one('restaurant_management.table', string='Table', required=True, ondelete='cascade')
    reservation_date = fields.Datetime(string='Reservation Date', required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='pending', required=True)
    created_at = fields.Datetime(string='Created At', default=fields.Datetime.now, readonly=True)
    updated_at = fields.Datetime(string='Updated At', readonly=True)
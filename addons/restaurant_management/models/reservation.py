from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Reservation(models.Model):
    _name = 'restaurant_management.reservation'
    _description = 'Reservation'
    _order = 'reservation_date desc'

    id = fields.Char(string='ID', default=lambda self: self.env["ir.sequence"].next_by_code("restaurant_management.reservation"), readonly=True)
    customer_id = fields.Many2one('restaurant_management.customer', string='Customer', required=True, ondelete='cascade')
    branch_id = fields.Many2one('restaurant_management.branch', string='Branch', required=True, ondelete='cascade')
    table_id = fields.Many2one('restaurant_management.table', string='Table', required=True, ondelete='cascade')
    reservation_date = fields.Datetime(string='Reservation Date', required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='pending', required=True)
    created_at = fields.Datetime(string='Created At', default=fields.Datetime.now, readonly=True)
    updated_at = fields.Datetime(string='Updated At', readonly=True)
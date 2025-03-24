from odoo import models, fields

class Reservation(models.Model):
    _name = 'restaurant_management.reservation'
    _description = 'Table Reservation'

    customer_id = fields.Many2one('restaurant_management.customer', string="Customer", required=True)
    branch_id = fields.Many2one('restaurant_management.branch', string="Branch", required=True)
    date_time = fields.Datetime(string="Reservation Date & Time", required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ], string="Status", default='pending')
    notes = fields.Text(string="Notes")
    created_at = fields.Datetime(string="Created At", default=fields.Datetime.now)
    updated_at = fields.Datetime(string="Updated At", default=fields.Datetime.now)

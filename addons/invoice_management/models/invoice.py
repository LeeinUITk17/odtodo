from odoo import models, fields, api

class Invoice(models.Model):
    _name = 'invoice.management'
    _description = 'Invoice Management'

    order_id = fields.Many2one('order.management', string="Order", required=True, ondelete="cascade")
    total_price = fields.Float(string="Total Price", related='order_id.total_price', store=True)
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('online_payment', 'Online Payment'),
    ], string="Payment Method", required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], string="Invoice Status", default="pending")
    notes = fields.Text(string="Notes")
    created_at = fields.Datetime(string="Created At", default=fields.Datetime.now)
    updated_at = fields.Datetime(string="Updated At")
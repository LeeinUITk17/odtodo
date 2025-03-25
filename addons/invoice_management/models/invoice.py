from odoo import models, fields, api

class Invoice(models.Model):
    _name = "invoice_management.invoice"
    _description = "Invoice"

    order_id = fields.Many2one("order_management.order", string="Order", required=True, ondelete="cascade")
    customer_id = fields.Many2one("restaurant_management.customer", string="Customer", ondelete="set null")
    total_price = fields.Float(string="Total Price", required=True)
    tax = fields.Float(string="Tax", default=0.0)
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('online_payment', 'Online Payment')
    ], string="Payment Method", required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ], string="Invoice Status", default="pending", required=True)
    created_at = fields.Datetime(string="Created At", default=fields.Datetime.now)
    updated_at = fields.Datetime(string="Updated At")
    coupon_id = fields.Char(string="Coupon ID")
    promotion_id = fields.Char(string="Promotion ID")
    details = fields.One2many("invoice_management.invoicedetail", "invoice_id", string="Invoice Details")
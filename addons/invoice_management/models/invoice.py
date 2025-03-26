from odoo import models, fields, api
import uuid

class Invoice(models.Model):
    _name = "invoice_management.invoice"
    _description = "Invoice"

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True)
    order_uuid = fields.Many2one("order_management.order", string="Order", required=True, ondelete="cascade")
    customer_uuid = fields.Many2one("restaurant_management.customer", string="Customer", ondelete="set null")
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
    coupon_uuid = fields.Char(string="Coupon UUID")
    promotion_uuid = fields.Char(string="Promotion UUID")
    details = fields.One2many("invoice_management.invoicedetail", "invoice_uuid", string="Invoice Details")
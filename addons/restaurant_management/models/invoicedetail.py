from odoo import models, fields, api
import uuid

class InvoiceDetail(models.Model):
    _name = "restaurant_management.invoicedetail"
    _description = "Invoice Detail"

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True, index=True)
    invoice_uuid = fields.Many2one("restaurant_management.invoice", string="Invoice", required=True, ondelete="cascade", index=True)
    product_uuid = fields.Many2one("restaurant_management.menuitem", string="Menu Item", required=True, ondelete="restrict", index=True)
    currency_id = fields.Many2one(related='invoice_uuid.currency_id', store=True, string="Currency", readonly=True)
    quantity = fields.Integer(string="Quantity", required=True, default=1)
    price = fields.Monetary(string="Unit Price", required=True, currency_field='currency_id')
    discount_amount = fields.Monetary(string="Discount Amount", default=0.0, currency_field='currency_id')
    amount = fields.Monetary(string="Subtotal", compute="_compute_amount", store=True, currency_field='currency_id')

    @api.depends('quantity', 'price', 'discount_amount')
    def _compute_amount(self):
        for detail in self:
            quantity = detail.quantity or 0
            price = detail.price or 0.0
            discount = detail.discount_amount or 0.0
            detail.amount = (quantity * price) - discount

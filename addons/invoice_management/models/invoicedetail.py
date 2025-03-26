from odoo import models, fields, api
import uuid

class InvoiceDetail(models.Model):
    _name = "invoice_management.invoicedetail"
    _description = "Invoice Detail"

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True)
    invoice_uuid = fields.Many2one("invoice_management.invoice", string="Invoice", required=True, ondelete="cascade")
    product_uuid = fields.Many2one("menu_management.menuitem", string="Product", required=True, ondelete="set null")
    quantity = fields.Integer(string="Quantity", required=True)
    price = fields.Float(string="Price", required=True)
    discount_amount = fields.Float(string="Discount Amount", default=0.0)
    amount = fields.Float(string="Amount", compute="_compute_amount", store=True)

    @api.depends('quantity', 'price', 'discount_amount')
    def _compute_amount(self):
        for detail in self:
            detail.amount = (detail.quantity * detail.price) - detail.discount_amount
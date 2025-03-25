from odoo import models, fields, api

class InvoiceDetail(models.Model):
    _name = "invoice_management.invoicedetail"
    _description = "Invoice Detail"

    invoice_id = fields.Many2one("invoice_management.invoice", string="Invoice", required=True, ondelete="cascade")
    quantity = fields.Integer(string="Quantity", required=True)
    price = fields.Float(string="Price", required=True)
    discount_amount = fields.Float(string="Discount Amount", default=0.0)
    amount = fields.Float(string="Amount", compute="_compute_amount", store=True)
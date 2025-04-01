# -*- coding: utf-8 -*-
from odoo import models, fields, api # Added api import
import uuid

class InvoiceDetail(models.Model):
    _name = "invoice_management.invoicedetail"
    _description = "Invoice Detail"

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True, index=True) # Added index
    invoice_uuid = fields.Many2one("invoice_management.invoice", string="Invoice", required=True, ondelete="cascade", index=True) # Added index

    # Dependency: menu_management
    product_uuid = fields.Many2one("restaurant_management.menuitem", string="Product", required=True, ondelete="restrict", index=True) # Changed ondelete to restrict, added index

    quantity = fields.Integer(string="Quantity", required=True, default=1)
    price = fields.Float(string="Unit Price", required=True) # Renamed for clarity
    discount_amount = fields.Float(string="Discount Amount", default=0.0)
    amount = fields.Float(string="Subtotal", compute="_compute_amount", store=True) # Renamed for clarity

    @api.depends('quantity', 'price', 'discount_amount')
    def _compute_amount(self):
        for detail in self:
            detail.amount = (detail.quantity * detail.price) - detail.discount_amount
    # REMOVED //

    # Optional: Auto-fill price from product
    # @api.onchange('product_uuid')
    # def _onchange_product_uuid(self):
    #     if self.product_uuid:
    #         self.price = self.product_uuid.price
    #     else:
    #         self.price = 0.0
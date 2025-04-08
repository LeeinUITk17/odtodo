from odoo import models, fields, api
import uuid

class OrderItem(models.Model):
    _name = "restaurant_management.orderitem"
    _description = "Restaurant Order Item"

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True, index=True)
    menu_item_uuid = fields.Many2one("restaurant_management.menuitem", string="Menu Item", required=True, ondelete='restrict')
    order_uuid = fields.Many2one("restaurant_management.order", string="Order", required=True, ondelete="cascade")
    quantity = fields.Integer(string="Quantity", required=True, default=1)
    unitPrice = fields.Float(string="Unit Price", compute="_compute_price", store=True, readonly=False)
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)

    @api.depends('menu_item_uuid.price', 'quantity')
    def _compute_price(self):
        for record in self:
            if record.menu_item_uuid:
                record.unitPrice = record.menu_item_uuid.price
            else:
                record.unitPrice = 0.0

    @api.depends('unitPrice', 'quantity')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.unitPrice * record.quantity

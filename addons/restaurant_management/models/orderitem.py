from odoo import models, fields, api
import uuid

class OrderItem(models.Model):
    _name = "restaurant_management.orderitem"
    _description = "Order Item"

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True)
    menu_item_uuid = fields.Many2one("restaurant_management.menuitem", string="Menu Item", required=True)
    order_uuid = fields.Many2one("restaurant_management.order", string="Order", required=True, ondelete="cascade")
    quantity = fields.Integer(string="Quantity", required=True, default=1)
    unitPrice = fields.Float(string="Unit Price", compute="_compute_price", store=True)

    @api.depends('menu_item_uuid.price') # Depend on the price field of the related menu item
    def _compute_price(self):
        for record in self:
            record.unitPrice = record.menu_item_uuid.price if record.menu_item_uuid else 0.0
            # REMOVED THE TRAILING //
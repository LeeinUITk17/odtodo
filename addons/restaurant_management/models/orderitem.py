from odoo import models, fields, api
import uuid

class OrderItem(models.Model):
    _name = "restaurant_management.orderitem"
    _description = "Restaurant Order Item"

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True, index=True) # Added index
    menu_item_uuid = fields.Many2one("restaurant_management.menuitem", string="Menu Item", required=True, ondelete='restrict') # Use restrict or set null usually better than cascade here
    order_uuid = fields.Many2one("restaurant_management.order", string="Order", required=True, ondelete="cascade") # Cascade delete makes sense here
    quantity = fields.Integer(string="Quantity", required=True, default=1)
    unitPrice = fields.Float(string="Unit Price", compute="_compute_price", store=True, readonly=False) # Allow manual override? If not, readonly=True
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True) # Add subtotal


    @api.depends('menu_item_uuid.price', 'quantity') # Recalculate price if menu item or quantity changes
    def _compute_price(self):
        for record in self:
            # Only update if unitPrice hasn't been manually set OR if menu item changed
            # Adjust this logic if you DON'T want manual override
             if record.menu_item_uuid:
                 record.unitPrice = record.menu_item_uuid.price
             else:
                 record.unitPrice = 0.0

    @api.depends('unitPrice', 'quantity')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.unitPrice * record.quantity
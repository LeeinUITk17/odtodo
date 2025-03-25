from odoo import models, fields, api

class OrderItem(models.Model):
    _name = "order_management.orderitem"
    _description = "Order Item"

    menu_item_id = fields.Many2one("menu_management.menuitem", string="Menu Item", required=True)
    order_id = fields.Many2one("order_management.order", string="Order", required=True, ondelete="cascade")
    quantity = fields.Integer(string="Quantity", required=True, default=1)
    unitPrice = fields.Float(string="Unit Price", compute="_compute_price", store=True)
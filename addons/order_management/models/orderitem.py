from odoo import models, fields

class OrderItem(models.Model):
    _name = 'order_management.orderitem'
    _description = 'Order Item'

    id = fields.Char('Order Item ID', required=True, default=lambda self: self.env['ir.sequence'].next_by_code('order.management.orderitem'))
    order_id = fields.Many2one('order_management.order', string="Order", required=True)
    menu_item_id = fields.Many2one('menu_management.menuitem', string="Menu Item", required=True)
    quantity = fields.Integer('Quantity', default=1)
    price = fields.Float('Price', related='menu_item_id.price', readonly=True)

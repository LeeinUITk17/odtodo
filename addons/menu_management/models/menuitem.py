from odoo import models, fields

class MenuItem(models.Model):
    _name = 'menu_management.menuitem'
    _description = 'Menu Item'

    name = fields.Char(string="Item Name", required=True)
    description = fields.Text(string="Description")
    price = fields.Float(string="Price", required=True)
    
    category_id = fields.Many2one('menu_management.category', string="Category", required=True, ondelete='cascade')
    branch_id = fields.Many2one('restaurant_management.branch', string="Branch", required=True, ondelete='cascade')

    order_item_ids = fields.One2many('order_management.orderitem', 'menu_item_id', string="Order Items")

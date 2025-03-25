from odoo import models, fields

class MenuItem(models.Model):
    _name = "menu_management.menuitem"
    _description = "Menu Item"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    price = fields.Float(string="Price", required=True)
    
    category_id = fields.Many2one("menu_management.category", string="Category", ondelete="set null")
    
    branch_id = fields.Many2one("restaurant_management.branch", string="Branch", required=True, ondelete="cascade")
    order_items = fields.One2many("order_management.orderitem", "menu_item_id", string="Order Items")
    created_at = fields.Datetime(string="Created At", default=fields.Datetime.now)
    updated_at = fields.Datetime(string="Updated At", default=fields.Datetime.now)
    deleted_at = fields.Datetime(string="Deleted At")
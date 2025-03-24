from odoo import models, fields

class Category(models.Model):
    _name = 'menu_management.category'
    _description = 'Menu Category'

    name = fields.Char(string="Category Name", required=True)
    parent_id = fields.Many2one('menu_management.category', string="Parent Category", ondelete='cascade')
    subcategory_ids = fields.One2many('menu_management.category', 'parent_id', string="Subcategories")
    menu_item_ids = fields.One2many('menu_management.menuitem', 'category_id', string="Menu Items")

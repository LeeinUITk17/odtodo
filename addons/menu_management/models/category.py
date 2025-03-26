import uuid
from odoo import models, fields, api

class Category(models.Model):
    _name = 'menu_management.category'
    _description = 'Menu Item Category'

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True)
    name = fields.Char(string="Category Name", required=True)

    menu_item_uuids = fields.One2many('menu_management.menuitem', 'category_uuid', string="Menu Items")
    created_at = fields.Datetime(string="Created At", default=fields.Datetime.now)
    updated_at = fields.Datetime(string="Updated At", default=fields.Datetime.now)
    deleted_at = fields.Datetime(string="Deleted At")
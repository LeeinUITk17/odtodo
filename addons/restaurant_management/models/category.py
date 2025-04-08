# -*- coding: utf-8 -*-
import uuid
from odoo import models, fields

class Category(models.Model):
    _name = 'restaurant_management.category'
    _description = 'Menu Item Category'
    _order = 'name asc'
    _rec_name = 'name'

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True, index=True)
    name = fields.Char(string="Category Name", required=True)
    menu_item_uuids = fields.One2many('restaurant_management.menuitem', 'category_uuid', string="Menu Items")
    created_at = fields.Datetime(string="Created At", default=fields.Datetime.now, readonly=True)
    updated_at = fields.Datetime(string="Updated At", default=fields.Datetime.now, readonly=True)
    deleted_at = fields.Datetime(string="Deleted At", readonly=True, index=True)

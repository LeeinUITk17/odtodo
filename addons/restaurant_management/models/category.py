# -*- coding: utf-8 -*-
import uuid
from odoo import models, fields, api # Use api even if not directly used now, good practice

class Category(models.Model):
    _name = 'restaurant_management.category'
    _description = 'Menu Item Category'
    # Optional: Add ordering or record name
    _order = 'name asc'
    _rec_name = 'name'

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True, index=True) # Add index for potential lookups
    name = fields.Char(string="Category Name", required=True)

    # Ensure the inverse name 'category_uuid' exists and is correct on menuitem model
    menu_item_uuids = fields.One2many('restaurant_management.menuitem', 'category_uuid', string="Menu Items")

    created_at = fields.Datetime(string="Created At", default=fields.Datetime.now, readonly=True)
    updated_at = fields.Datetime(string="Updated At", default=fields.Datetime.now, readonly=True) # Consider auto_now=True if using ORM write
    deleted_at = fields.Datetime(string="Deleted At", readonly=True, index=True) # Soft delete flag

    # Optional: Add method for soft delete
    # def action_archive(self):
    #     self.write({'deleted_at': fields.Datetime.now()})

    # Optional: Add method for restoring
    # def action_unarchive(self):
    #     self.write({'deleted_at': False})

    # Optional: Override write to update 'updated_at'
    # def write(self, vals):
    #     if 'updated_at' not in vals:
    #          vals['updated_at'] = fields.Datetime.now()
    #     return super(Category, self).write(vals)
# -*- coding: utf-8 -*-
from odoo import models, fields, api # Import api
import uuid

class MenuItem(models.Model):
    _name = "restaurant_management.menuitem"
    _description = "Menu Item"
    # Optional: Add ordering or record name
    _order = 'name asc'
    _rec_name = 'name'

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True, index=True)
    name = fields.Char(string="Name", required=True, index=True)
    description = fields.Text(string="Description")
    price = fields.Float(string="Price", required=True, digits='Product Price') # Use standard digits precision
    image = fields.Image(string="Image") # Example: Add an image field

    # Field linking back to Category
    category_uuid = fields.Many2one("restaurant_management.category", string="Category", ondelete="set null", index=True)

    # Ensure restaurant_management module exists and is a dependency
    branch_uuid = fields.Many2one("restaurant_management.branch", string="Branch", required=True, ondelete="cascade", index=True)

    # Ensure order_management module exists and is a dependency
    # Ensure 'menu_item_uuid' field exists on order_management.orderitem
    order_item_uuids = fields.One2many("restaurant_management.orderitem", "menu_item_uuid", string="Order Items")

    created_at = fields.Datetime(string="Created At", default=fields.Datetime.now, readonly=True)
    updated_at = fields.Datetime(string="Updated At", default=fields.Datetime.now, readonly=True) # Consider auto_now=True
    deleted_at = fields.Datetime(string="Deleted At", readonly=True, index=True) # Soft delete flag

    # Optional: Add active field for standard Odoo filtering (often used instead of deleted_at)
    # active = fields.Boolean(default=True, index=True)

    # Optional: Override write to update 'updated_at'
    # def write(self, vals):
    #     if 'updated_at' not in vals:
    #          vals['updated_at'] = fields.Datetime.now()
    #     return super(MenuItem, self).write(vals)
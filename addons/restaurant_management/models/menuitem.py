# -*- coding: utf-8 -*-
from odoo import models, fields, api # Import api
import uuid

class MenuItem(models.Model):
    _name = "restaurant_management.menuitem"
    _description = "Menu Item"
    _order = 'name asc'
    _rec_name = 'name'

    # --- Add these fields for currency support ---
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id', store=True, string="Currency")
    # --------------------------------------------

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True, index=True)
    name = fields.Char(string="Name", required=True, index=True)
    description = fields.Text(string="Description")
    # Make sure price field uses correct digits if needed, 'Product Price' is standard
    price = fields.Monetary(string="Price", required=True, currency_field='currency_id') # Changed to fields.Monetary
    image = fields.Image(string="Image")

    category_uuid = fields.Many2one("restaurant_management.category", string="Category", ondelete="set null", index=True)
    branch_uuid = fields.Many2one("restaurant_management.branch", string="Branch", required=True, ondelete="cascade", index=True)
    order_item_uuids = fields.One2many("restaurant_management.orderitem", "menu_item_uuid", string="Order Items")

    created_at = fields.Datetime(string="Created At", default=fields.Datetime.now, readonly=True)
    updated_at = fields.Datetime(string="Updated At", default=fields.Datetime.now, readonly=True)
    deleted_at = fields.Datetime(string="Deleted At", readonly=True, index=True)

    # Consider adding 'active' field here too if you want standard archiving
    # active = fields.Boolean(default=True, index=True)
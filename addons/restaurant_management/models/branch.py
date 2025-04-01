# -*- coding: utf-8 -*-
from odoo import models, fields, api # Import api
import uuid

class Branch(models.Model):
    _name = "restaurant_management.branch"
    _description = "Branch Model"
    _rec_name = 'name' # Good practice: define the display name
    _order = 'name asc' # Good practice: define default order

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True, index=True)
    name = fields.Char(string="Branch Name", required=True, index=True)
    location = fields.Char(string="Location", required=True)
    created_at = fields.Datetime(string="Created At", default=fields.Datetime.now, readonly=True)
    updated_at = fields.Datetime(string="Updated At", default=fields.Datetime.now, readonly=True) # Usually readonly

    # Ensure inverse name 'branch_uuid' exists on target models
    # Ensure target modules are listed as dependencies
    menu_items = fields.One2many("restaurant_management.menuitem", "branch_uuid", string="Menu Items")
    tables = fields.One2many("restaurant_management.table", "branch_uuid", string="Tables")
    reservations = fields.One2many("restaurant_management.reservation", "branch_uuid", string="Reservations")
    orders = fields.One2many("restaurant_management.order", "branch_uuid", string="Orders")
    # REMOVED //
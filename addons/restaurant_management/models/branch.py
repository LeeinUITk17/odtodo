from odoo import models, fields

class Branch(models.Model):
    _name = "restaurant_management.branch"
    _description = "Branch Model"

    name = fields.Char(string="Branch Name", required=True)
    location = fields.Char(string="Location", required=True)
    created_at = fields.Datetime(string="Created At", default=fields.Datetime.now)
    updated_at = fields.Datetime(string="Updated At", default=fields.Datetime.now)

    menu_items = fields.One2many("menu_management.menuitem", "branch_id", string="Menu Items")
    tables = fields.One2many("restaurant_management.table", "branch_id", string="Tables")
    reservations = fields.One2many("restaurant_management.reservation", "branch_id", string="Reservations")
    orders = fields.One2many("order_management.order", "branch_id", string="Orders")

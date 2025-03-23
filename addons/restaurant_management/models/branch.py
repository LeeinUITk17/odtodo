from odoo import models, fields

class Branch(models.Model):
    _name = 'restaurant.branch'
    _description = 'Restaurant Branch'

    name = fields.Char(string="Name", required=True)
    location = fields.Char(string="Location", required=True)
    menu_item_ids = fields.One2many('restaurant.menu_item', 'branch_id', string="Menu Items")
    order_ids = fields.One2many('restaurant.order', 'branch_id', string="Orders")
    reservation_ids = fields.One2many('restaurant.reservation', 'branch_id', string="Reservations")
    created_at = fields.Datetime(string="Created At", default=fields.Datetime.now)
    updated_at = fields.Datetime(string="Updated At", default=fields.Datetime.now)

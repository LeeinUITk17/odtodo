from odoo import models, fields

class Customer(models.Model):
    _name = 'restaurant.customer'
    _description = 'Restaurant Customer'

    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="Email", unique=True)
    phone = fields.Char(string="Phone", unique=True)
    birthday = fields.Date(string="Birthday")
    order_ids = fields.One2many('restaurant.order', 'customer_id', string="Orders")
    reservation_ids = fields.One2many('restaurant.reservation', 'customer_id', string="Reservations")
    created_at = fields.Datetime(string="Created At", default=fields.Datetime.now)
    updated_at = fields.Datetime(string="Updated At", default=fields.Datetime.now)

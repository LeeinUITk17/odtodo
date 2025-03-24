from odoo import models, fields

class Table(models.Model):
    _name = 'restaurant_management.table'
    _description = 'Restaurant Table'

    number = fields.Char(string="Table Number", required=True, unique=True)
    capacity = fields.Integer(string="Capacity", required=True)
    status = fields.Selection([
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
    ], string="Status", default='available')
    order_ids = fields.One2many('order_management.order', 'table_id', string="Orders")

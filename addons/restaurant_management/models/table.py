from odoo import models, fields, api
import uuid

class Table(models.Model):
    _name = "restaurant_management.table"
    _description = "Restaurant Table"

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True)
    name = fields.Char(string="Table Name", required=True)
    area = fields.Selection([
        ('indoor', 'Indoor'),
        ('outdoor', 'Outdoor')
    ], string="Table Area", required=True)
    floor = fields.Char(string="Floor")
    capacity = fields.Integer(string="Capacity", required=True)
    status = fields.Selection([
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved')
    ], string="Status", default='available')

    branch_uuid = fields.Many2one('restaurant_management.branch', string="Branch", required=True, ondelete='cascade')
    order_uuids = fields.One2many('order_management.order', 'table_uuid', string="Orders")
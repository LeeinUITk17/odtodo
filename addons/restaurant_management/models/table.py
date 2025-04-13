from odoo import models, fields
import uuid

class Table(models.Model):
    _name = "restaurant_management.table"
    _description = "Restaurant Table"
    _rec_name = 'name'
    _order = 'name asc'

    active = fields.Boolean(default=True, index=True, string="Active")
    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True, index=True)
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
    ], string="Status", default='available', index=True)
    branch_uuid = fields.Many2one('restaurant_management.branch', string="Branch", required=True, ondelete='cascade', index=True)
    order_uuids = fields.One2many('restaurant_management.order', 'table_uuid', string="Orders")
    created_at = fields.Datetime(string="Created At", default=fields.Datetime.now, readonly=True)
    updated_at = fields.Datetime(string="Updated At", default=fields.Datetime.now, readonly=True)

    def is_available(self):
        self.ensure_one()
        pending_orders = self.order_uuids.filtered(lambda o: o.status == 'PENDING')
        return not pending_orders

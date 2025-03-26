from odoo import models, fields, api
import uuid

class Order(models.Model):
    _name = 'order_management.order'
    _description = 'Order'
    _order = 'created_at desc'

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True)
    status = fields.Selection([
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELED', 'Canceled')
    ], string='Status', default='PENDING', required=True)
    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)
    created_at = fields.Datetime(string='Created At', default=fields.Datetime.now, readonly=True)
    updated_at = fields.Datetime(string='Updated At', default=fields.Datetime.now, readonly=True)

    table_uuid = fields.Many2one('restaurant_management.table', string='Table', ondelete='set null')
    branch_uuid = fields.Many2one('restaurant_management.branch', string='Branch', required=True, ondelete='cascade')
    order_items = fields.One2many('order_management.orderitem', 'order_uuid', string='Order Items')

    @api.depends('order_items')
    def _compute_total_price(self):
        for order in self:
            order.total_price = sum(item.unitPrice * item.quantity for item in order.order_items)
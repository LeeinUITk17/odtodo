from odoo import models, fields, api

class Order(models.Model):
    _name = 'order_management.order'
    _description = 'Order'
    _order = 'created_at desc'

    id = fields.Char(string='ID', default=lambda self: self.env['ir.sequence'].next_by_code('order_management.order'), readonly=True)
    status = fields.Selection([
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELED', 'Canceled')
    ], string='Status', default='PENDING', required=True)
    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)
    created_at = fields.Datetime(string='Created At', default=fields.Datetime.now, readonly=True)
    updated_at = fields.Datetime(string='Updated At', default=fields.Datetime.now, readonly=True)

    table_id = fields.Many2one('restaurant_management.table', string='Table', ondelete='set null')
    branch_id = fields.Many2one('restaurant_management.branch', string='Branch', required=True, ondelete='cascade')
    order_items = fields.One2many('order_management.orderitem', 'order_id', string='Order Items')
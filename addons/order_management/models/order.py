from odoo import models, fields

class Order(models.Model):
    _name = 'order_management.order'
    _description = 'Order Management'

    id = fields.Char('Order ID', required=True, default=lambda self: self.env['ir.sequence'].next_by_code('order.management.order'))
    customer_id = fields.Many2one('restaurant_management.customer', string="Customer")
    table_id = fields.Many2one('restaurant_management.table', string="Table")
    branch_id = fields.Many2one('restaurant_management.branch', string="Branch", required=True)
    order_item_ids = fields.One2many('order_management.orderitem', 'order_id', string="Order Items")
    status = fields.Selection([
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='pending', string="Order Status")
    total_price = fields.Float('Total Price', compute='_compute_total_price', store=True)
    notes = fields.Text('Notes')
    created_by = fields.Many2one('res.users', string="Created By")
    created_at = fields.Datetime('Created At', default=fields.Datetime.now)
    updated_at = fields.Datetime('Updated At', default=fields.Datetime.now)


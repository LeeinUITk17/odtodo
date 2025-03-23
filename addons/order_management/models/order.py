from odoo import models, fields

class Order(models.Model):
    _name = 'order.management.order'
    _description = 'Order Management'

    id = fields.Char('Order ID', required=True, default=lambda self: self.env['ir.sequence'].next_by_code('order.management.order'))
    customer_id = fields.Many2one('res.partner', string="Customer")
    table_id = fields.Many2one('restaurant.management.table', string="Table")
    branch_id = fields.Many2one('restaurant.management.branch', string="Branch", required=True)
    order_item_ids = fields.One2many('order.management.orderitem', 'order_id', string="Order Items")
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

    @api.depends('order_item_ids.price')
    def _compute_total_price(self):
        for order in self:
            order.total_price = sum(order.order_item_ids.mapped('price'))

    def action_confirm_order(self):
        self.write({'status': 'confirmed'})

    def action_cancel_order(self):
        self.write({'status': 'cancelled'})

    def action_complete_order(self):
        self.write({'status': 'completed'})

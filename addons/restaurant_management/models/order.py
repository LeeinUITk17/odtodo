from odoo import models, fields, api, _
from odoo.exceptions import UserError
import uuid

class Order(models.Model):
    _name = 'restaurant_management.order'
    _description = 'Restaurant Order'
    _order = 'created_at desc'

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True, index=True)
    name = fields.Char(string="Order Reference", required=True, copy=False, readonly=True, default=lambda self: _('New'), index=True)
    status = fields.Selection([
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELED', 'Canceled')
    ], string='Status', default='PENDING', required=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id', store=True, string="Currency", readonly=True)
    total_price = fields.Monetary(string='Total Price', compute='_compute_total_price', store=True, tracking=True, currency_field='currency_id')
    created_at = fields.Datetime(string='Created At', default=fields.Datetime.now, readonly=True)
    updated_at = fields.Datetime(string='Updated At', default=fields.Datetime.now, readonly=True)
    table_uuid = fields.Many2one('restaurant_management.table', string='Table', ondelete='set null', tracking=True, domain="[('branch_uuid', '=', branch_uuid)]")
    branch_uuid = fields.Many2one('restaurant_management.branch', string='Branch', required=True, ondelete='cascade', tracking=True)
    customer_uuid = fields.Many2one('restaurant_management.customer', string='Customer', ondelete='set null', tracking=True)
    order_items = fields.One2many('restaurant_management.orderitem', 'order_uuid', string='Order Items')
    invoice_ids = fields.One2many('restaurant_management.invoice', 'order_uuid', string='Invoices', readonly=True)
    invoice_count = fields.Integer(compute='_compute_invoice_count', string="Invoice Count")
    available_menu_item_ids = fields.Many2many(
        'restaurant_management.menuitem',
        string="Available Menu Items",
        compute='_compute_available_menu_items',
        store=False,
        readonly=True
    )
    invoice_status = fields.Selection([
        ('no_invoice', 'Not Invoiced'),
        ('to_invoice', 'To Invoice'), # Order completed, no invoice yet
        ('invoiced', 'Invoiced'),    # Invoice exists (draft or posted)
        ('paid', 'Paid')             # Invoice is paid
        ], string='Invoice Status', compute='_compute_invoice_status', store=True, default='no_invoice') # store=True để lọc/nhóm
    
    @api.depends('status', 'invoice_ids', 'invoice_ids.status')
    def _compute_invoice_status(self):
        for order in self:
            if not order.invoice_ids:
                if order.status == 'COMPLETED':
                    order.invoice_status = 'to_invoice'
                else:
                    order.invoice_status = 'no_invoice'
            else:
                # Kiểm tra trạng thái của các hóa đơn liên quan (không bị hủy)
                active_invoices = order.invoice_ids.filtered(lambda inv: inv.status != 'cancelled')
                if not active_invoices:
                     if order.status == 'COMPLETED':
                        order.invoice_status = 'to_invoice'
                     else:
                        order.invoice_status = 'no_invoice'
                elif any(inv.status == 'paid' for inv in active_invoices):
                    order.invoice_status = 'paid'
                else: # Có hóa đơn nhưng chưa paid (draft hoặc posted)
                    order.invoice_status = 'invoiced'


    @api.depends('branch_uuid')
    def _compute_available_menu_items(self):
        for order in self:
            if order.branch_uuid:
                domain = [('branch_uuid', '=', order.branch_uuid.id), ('active', '=', True)]
                order.available_menu_item_ids = self.env['restaurant_management.menuitem'].search(domain)
            else:
                order.available_menu_item_ids = self.env['restaurant_management.menuitem'].browse()

    def add_menu_item_from_ui(self, menu_item_id, quantity=1):
        self.ensure_one()
        if self.status != 'PENDING':
            raise UserError(_("You can only add items to Pending orders."))
        if not menu_item_id:
            raise UserError(_("Menu item not specified."))
        menu_item = self.env['restaurant_management.menuitem'].browse(menu_item_id)
        if not menu_item.exists():
            raise UserError(_("Selected Menu Item does not exist."))
        existing_item = self.order_items.filtered(lambda item: item.menu_item_uuid.id == menu_item_id)
        if existing_item:
            existing_item.quantity += quantity
        else:
            self.env['restaurant_management.orderitem'].create({
                'order_uuid': self.id,
                'menu_item_uuid': menu_item_id,
                'quantity': quantity,
            })
        return {'type': 'ir.actions.do_nothing'}

    @api.depends('order_items.subtotal')
    def _compute_total_price(self):
        for order in self:
            order.total_price = sum(item.subtotal for item in order.order_items)

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for order in self:
            order.invoice_count = len(order.invoice_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('restaurant.order.sequence') or _('New')
        return super(Order, self).create(vals_list)

    def write(self, vals):
        if any(f in vals for f in vals if f != 'updated_at'):
            vals['updated_at'] = fields.Datetime.now()
        return super(Order, self).write(vals)

    def action_complete(self):
        allowed_statuses = ['PENDING']
        if any(rec.status not in allowed_statuses for rec in self):
            raise UserError(_("Only pending orders can be marked as Completed."))
        res = self.write({'status': 'COMPLETED'})
        self._compute_invoice_status()
        return res

    def action_cancel(self):
        allowed_statuses = ['PENDING', 'COMPLETED']
        if any(rec.status not in allowed_statuses for rec in self):
            raise UserError(_("Only pending or Completed orders can be Canceled."))
        if any(order.invoice_status == 'paid' for order in self):
            raise UserError(_("You cannot cancel an order with a paid invoice. Please cancel the invoice first."))
        res = self.write({'status': 'CANCELED'})
        self._compute_invoice_status()
        return res

    def action_reset_to_pending(self):
        allowed_statuses = ['COMPLETED', 'CANCELED']
        if any(rec.status not in allowed_statuses for rec in self):
            raise UserError(_("Only Completed or Canceled orders can be reset to Pending."))
        if any(order.invoice_status == 'paid' for order in self):
            raise UserError(_("You cannot reset an order with a paid invoice."))
        res = self.write({'status': 'PENDING'})
        self._compute_invoice_status()
        return res

    def action_create_invoice(self):
        invoices_vals_list = []
        for order in self:
            if order.status != 'COMPLETED' or order.invoice_status not in ('to_invoice', 'no_invoice'):
                 if order.status != 'COMPLETED':
                     raise UserError(_("You can only create invoices for completed orders."))
                 else:
                     raise UserError(_("This order already has an active invoice or is not ready to be invoiced."))
            invoice_lines = []
            for item in order.order_items:
                invoice_lines.append((0, 0, {
                    'product_uuid': item.menu_item_uuid.id,
                    'quantity': item.quantity,
                    'price': item.unitPrice,
                    'discount_amount': 0.0,
                }))

            invoices_vals_list.append({
                'order_uuid': order.id,
                'customer_uuid': order.customer_uuid.id if order.customer_uuid else False,
                'details': invoice_lines,
                'status': 'draft',
            })

        if invoices_vals_list:
            new_invoices = self.env['restaurant_management.invoice'].create(invoices_vals_list)
            self._compute_invoice_status()
            action = self.action_view_invoices()
            if new_invoices and len(new_invoices) == 1: 
                 action['views'] = [(self.env.ref('restaurant_management.view_invoice_form').id, 'form')]
                 action['res_id'] = new_invoices.id
            return action
        return True

    def action_view_invoices(self):
        action = self.env['ir.actions.act_window']._for_xml_id('restaurant_management.action_invoice')
        if len(self.invoice_ids) == 1:
            action['views'] = [(self.env.ref('restaurant_management.view_invoice_form').id, 'form')]
            action['res_id'] = self.invoice_ids.id
        else:
            action['domain'] = [('id', 'in', self.invoice_ids.ids)]
        return action

from odoo import models, fields, api, _
import uuid

class Branch(models.Model):
    _name = "restaurant_management.branch"
    _description = "Branch Model"
    _rec_name = 'name'
    _order = 'name asc'

    active = fields.Boolean(default=True, index=True, string="Active")
    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True, index=True)
    name = fields.Char(string="Branch Name", required=True, index=True)
    location = fields.Char(string="Location", required=True)
    created_at = fields.Datetime(string="Created At", default=fields.Datetime.now, readonly=True)
    updated_at = fields.Datetime(string="Updated At", default=fields.Datetime.now, readonly=True)

    menu_items = fields.One2many("restaurant_management.menuitem", "branch_uuid", string="Menu Items")
    tables = fields.One2many("restaurant_management.table", "branch_uuid", string="Tables")
    reservations = fields.One2many("restaurant_management.reservation", "branch_uuid", string="Reservations")
    orders = fields.One2many("restaurant_management.order", "branch_uuid", string="Orders")
    invoices = fields.One2many("restaurant_management.invoice", compute='_compute_branch_invoices', string="Invoices", readonly=True)
    customer_count = fields.Integer(compute='_compute_customer_count', string="Customer Count")
    table_count = fields.Integer(compute='_compute_table_count', string="Table Count")
    menu_item_count = fields.Integer(compute='_compute_menu_item_count', string="Menu Item Count")
    reservation_count = fields.Integer(compute='_compute_reservation_count', string="Reservation Count")
    order_count = fields.Integer(compute='_compute_order_count', string="Order Count")
    invoice_count = fields.Integer(compute='_compute_invoice_count', string="Invoice Count")

    @api.depends('tables')
    def _compute_table_count(self):
        for branch in self:
            branch.table_count = len(branch.tables)

    @api.depends('menu_items')
    def _compute_menu_item_count(self):
        for branch in self:
            branch.menu_item_count = len(branch.menu_items)

    @api.depends('reservations')
    def _compute_reservation_count(self):
        for branch in self:
            branch.reservation_count = len(branch.reservations)

    @api.depends('orders')
    def _compute_order_count(self):
        for branch in self:
            branch.order_count = len(branch.orders)

    @api.depends('orders.invoice_ids')
    def _compute_branch_invoices(self):
        for branch in self:
            invoice_ids = branch.orders.mapped('invoice_ids')
            branch.invoices = invoice_ids

    @api.depends('invoices')
    def _compute_invoice_count(self):
        for branch in self:
            branch.invoice_count = len(branch.invoices)

    @api.depends('reservations.customer_uuid', 'orders.customer_uuid')
    def _compute_customer_count(self):
        for branch in self:
            customer_ids = set()
            if branch.reservations:
                customer_ids.update(branch.reservations.mapped('customer_uuid.id'))
            if branch.orders:
                customer_ids.update(branch.orders.mapped('customer_uuid.id'))
            customer_ids.discard(False)
            branch.customer_count = len(customer_ids)

    def action_view_tables(self):
        self.ensure_one()
        return {
            'name': _('Tables of %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'restaurant_management.table',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('branch_uuid', '=', self.id)],
            'context': {'default_branch_uuid': self.id},
        }

    def action_view_menu_items(self):
        self.ensure_one()
        return {
            'name': _('Menu Items of %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'restaurant_management.menuitem',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('branch_uuid', '=', self.id)],
            'context': {'default_branch_uuid': self.id},
        }

    def action_view_categories(self):
        return self.env['ir.actions.act_window']._for_xml_id('restaurant_management.action_category')

    def action_view_reservations(self):
        self.ensure_one()
        return {
            'name': _('Reservations for %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'restaurant_management.reservation',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('branch_uuid', '=', self.id)],
            'context': {
                'default_branch_uuid': self.id,
                'search_default_pending': 1,
                'search_default_confirmed': 1,
            },
        }

    def action_view_orders(self):
        self.ensure_one()
        return {
            'name': _('Orders for %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'restaurant_management.order',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('branch_uuid', '=', self.id)],
            'context': {
                'default_branch_uuid': self.id,
                'search_default_pending_orders': 1,
            },
        }

    def action_view_invoices(self):
        self.ensure_one()
        order_ids = self.orders.ids
        domain = [('order_uuid', 'in', order_ids)]
        action = {
            'name': _('Invoices for %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'restaurant_management.invoice',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': domain,
            'context': {
                'search_default_posted_invoices': 1,
                'search_default_paid_invoices': 1,
            },
        }
        action_from_xml = self.env['ir.actions.act_window']._for_xml_id('restaurant_management.action_invoice')
        if action_from_xml:
            action['search_view_id'] = action_from_xml.get('search_view_id', False)
            if isinstance(action['search_view_id'], tuple):
                action['search_view_id'] = action['search_view_id'][0]
        return action

    def action_view_customers(self):
        self.ensure_one()
        customer_ids = set()
        if self.reservations:
            customer_ids.update(self.reservations.mapped('customer_uuid.id'))
        if self.orders:
            customer_ids.update(self.orders.mapped('customer_uuid.id'))
        customer_ids.discard(False)
        action = {
            'name': _('Customers related to %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'restaurant_management.customer',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('id', 'in', list(customer_ids))],
            'context': {},
        }
        action_from_xml = self.env['ir.actions.act_window']._for_xml_id('restaurant_management.action_customer')
        if action_from_xml:
            action['search_view_id'] = action_from_xml.get('search_view_id', False)
            if isinstance(action['search_view_id'], tuple):
                action['search_view_id'] = action['search_view_id'][0]
        return action

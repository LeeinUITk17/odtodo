# -*- coding: utf-8 -*-
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

    table_count = fields.Integer(compute='_compute_table_count', string="Table Count")
    menu_item_count = fields.Integer(compute='_compute_menu_item_count', string="Menu Item Count")
    reservation_count = fields.Integer(compute='_compute_reservation_count', string="Reservation Count")
    order_count = fields.Integer(compute='_compute_order_count', string="Order Count")

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

    def action_view_tables(self):
        self.ensure_one()
        action = {
            'name': _('Tables of %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'restaurant_management.table',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('branch_uuid', '=', self.id)],
            'context': {
                'default_branch_uuid': self.id,
            }
        }
        return action

    def action_view_menu_items(self):
        self.ensure_one()
        action = {
            'name': _('Menu Items of %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'restaurant_management.menuitem',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('branch_uuid', '=', self.id)],
            'context': {
                'default_branch_uuid': self.id,
            }
        }
        return action

    def action_view_categories(self):
        action = self.env['ir.actions.act_window']._for_xml_id('restaurant_management.action_category')
        return action

    def action_view_reservations(self):
        self.ensure_one()
        action = {
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
            }
        }
        return action

    def action_view_orders(self):
        self.ensure_one()
        action = {
            'name': _('Orders for %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'restaurant_management.order',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('branch_uuid', '=', self.id)],
            'context': {
                'default_branch_uuid': self.id,
                'search_default_pending_orders': 1,
            }
        }
        return action

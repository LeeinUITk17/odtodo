# -*- coding: utf-8 -*-
from odoo import models, fields, api, _ # Import api and _
import uuid

class Branch(models.Model):
    _name = "restaurant_management.branch"
    _description = "Branch Model"
    _rec_name = 'name'
    _order = 'name asc'

    # Add this field
    active = fields.Boolean(default=True, index=True, string="Active")

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True, index=True)
    name = fields.Char(string="Branch Name", required=True, index=True)
    location = fields.Char(string="Location", required=True)
    created_at = fields.Datetime(string="Created At", default=fields.Datetime.now, readonly=True)
    updated_at = fields.Datetime(string="Updated At", default=fields.Datetime.now, readonly=True)

    # One2many fields
    menu_items = fields.One2many("restaurant_management.menuitem", "branch_uuid", string="Menu Items")
    tables = fields.One2many("restaurant_management.table", "branch_uuid", string="Tables")
    reservations = fields.One2many("restaurant_management.reservation", "branch_uuid", string="Reservations")
    orders = fields.One2many("restaurant_management.order", "branch_uuid", string="Orders")

    # Count computed fields (optional but good for UI)
    table_count = fields.Integer(compute='_compute_table_count', string="Table Count")
    menu_item_count = fields.Integer(compute='_compute_menu_item_count', string="Menu Item Count") # <-- New count field
    # --- ADD THIS FIELD ---
    reservation_count = fields.Integer(compute='_compute_reservation_count', string="Reservation Count")
    # ----------------------
    @api.depends('tables')
    def _compute_table_count(self):
        for branch in self:
            branch.table_count = len(branch.tables)

    # --- New computed field method ---
    @api.depends('menu_items')
    def _compute_menu_item_count(self):
        for branch in self:
            branch.menu_item_count = len(branch.menu_items)
    # --------------------------------
    # --- ADD THIS COMPUTE METHOD ---
    @api.depends('reservations')
    def _compute_reservation_count(self):
        for branch in self:
            # You might want to filter this count later, e.g., count only active reservations
            branch.reservation_count = len(branch.reservations)
    # -------------------------------

    # --- Action Method for Tables ---
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

    # --- New Action Method for Menu Items ---
    def action_view_menu_items(self):
        self.ensure_one()
        action = {
            'name': _('Menu Items of %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'restaurant_management.menuitem',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('branch_uuid', '=', self.id)], # Filter by current branch
            'context': {
                'default_branch_uuid': self.id, # Pre-fill branch
            }
        }
        return action
    # -----------------------------------------

    # --- New Action Method for Categories ---
    def action_view_categories(self):
        # No ensure_one needed as it navigates to all categories
        action = self.env['ir.actions.act_window']._for_xml_id('restaurant_management.action_category')
        # Or define it manually:
        # action = {
        #     'name': _('Menu Categories'),
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'restaurant_management.category',
        #     'view_mode': 'tree,form',
        #     'target': 'current',
        #     'domain': [], # No domain filter needed
        #     'context': {}
        # }
        return action
    # ---------------------------------------
    def action_view_reservations(self):
        self.ensure_one()
        action = {
            'name': _('Reservations for %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'restaurant_management.reservation',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('branch_uuid', '=', self.id)], # Filter by current branch
            'context': {
                'default_branch_uuid': self.id, # Pre-fill branch
                'search_default_pending': 1,    # Example: Default filter to pending
                'search_default_confirmed': 1, # Example: Default filter to confirmed
            }
        }
        return action
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _ # Added _
from odoo.exceptions import UserError    # Added UserError
import uuid

class Reservation(models.Model):
    _name = 'restaurant_management.reservation'
    _description = 'Reservation'
    _order = 'reservation_date desc, name asc'

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True, index=True)
    name = fields.Char(string='Customer Name', required=True, index=True, tracking=True) # Added tracking
    phone = fields.Char(string='Phone Number', required=True, tracking=True)             # Added tracking
    branch_uuid = fields.Many2one('restaurant_management.branch', string='Branch', required=True, ondelete='cascade', index=True, tracking=True) # Added tracking
    table_uuid = fields.Many2one('restaurant_management.table', string='Table', required=True, ondelete='cascade', index=True, tracking=True)       # Added tracking
    reservation_date = fields.Datetime(string='Reservation Date', required=True, index=True, tracking=True) # Added tracking
    status = fields.Selection([
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
        # Optional: Add 'seated', 'completed', 'no_show' for more detail later
    ], string='Status', default='pending', required=True, index=True, tracking=True) # Added tracking
    created_at = fields.Datetime(string='Created At', default=fields.Datetime.now, readonly=True)
    updated_at = fields.Datetime(string='Updated At', default=fields.Datetime.now, readonly=True)

    # --- Action Methods for Status Updates ---
    def action_confirm(self):
        """Confirms the reservation."""
        allowed_statuses = ['pending']
        for res in self.filtered(lambda r: r.status in allowed_statuses):
            res.write({'status': 'confirmed'})
        # Raise error if trying to confirm non-pending reservations
        if any(r.status not in allowed_statuses for r in self):
             raise UserError(_("Only pending reservations can be confirmed."))
        return True

    def action_cancel(self):
        """Cancels the reservation."""
        allowed_statuses = ['pending', 'confirmed']
        for res in self.filtered(lambda r: r.status in allowed_statuses):
            res.write({'status': 'cancelled'})
        # Raise error if trying to cancel already cancelled reservations
        if any(r.status not in allowed_statuses for r in self):
            raise UserError(_("Only pending or confirmed reservations can be cancelled."))
        return True

    def action_reset_to_pending(self):
        """Resets the reservation back to pending."""
        allowed_statuses = ['confirmed', 'cancelled']
        for res in self.filtered(lambda r: r.status in allowed_statuses):
            res.write({'status': 'pending'})
        # Raise error if trying to reset non-confirmed/cancelled reservations
        if any(r.status not in allowed_statuses for r in self):
            raise UserError(_("Only confirmed or cancelled reservations can be reset to pending."))
        return True
    # -----------------------------------------
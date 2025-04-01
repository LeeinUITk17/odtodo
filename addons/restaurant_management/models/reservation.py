# -*- coding: utf-8 -*-
from odoo import models, fields, api
import uuid

class Reservation(models.Model):
    _name = 'restaurant_management.reservation'
    _description = 'Reservation'
    _order = 'reservation_date desc'

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True, index=True)
    customer_uuid = fields.Many2one('restaurant_management.customer', string='Customer', required=True, ondelete='cascade', index=True)
    branch_uuid = fields.Many2one('restaurant_management.branch', string='Branch', required=True, ondelete='cascade', index=True)
    table_uuid = fields.Many2one('restaurant_management.table', string='Table', required=True, ondelete='cascade', index=True)
    reservation_date = fields.Datetime(string='Reservation Date', required=True, index=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='pending', required=True, index=True)
    created_at = fields.Datetime(string='Created At', default=fields.Datetime.now, readonly=True)
    updated_at = fields.Datetime(string='Updated At', default=fields.Datetime.now, readonly=True) # Added default, make readonly
    # REMOVED //

    # Example: Add compute field for display name
    # name = fields.Char(compute='_compute_display_name', store=True)
    # @api.depends('customer_uuid.name', 'reservation_date')
    # def _compute_display_name(self):
    #    for rec in self:
    #        rec.name = f"{rec.customer_uuid.name or 'Unknown'} on {rec.reservation_date}"

    # Example: Override write to update 'updated_at' automatically
    # def write(self, vals):
    #    if 'updated_at' not in vals:
    #         vals['updated_at'] = fields.Datetime.now()
    #    return super(Reservation, self).write(vals)
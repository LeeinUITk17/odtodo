# -*- coding: utf-8 -*-
from odoo import models, fields, api # Import api
import uuid

class Customer(models.Model):
    _name = 'restaurant_management.customer'
    _description = 'Customer'
    _rec_name = 'name'
    _order = 'name asc'

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True, index=True)
    name = fields.Char(string='Name', required=True, index=True)
    birthday = fields.Date(string='Birthday')
    email = fields.Char(string='Email', required=True) # Consider adding unique constraint?
    phone = fields.Char(string='Phone', required=True) # Consider adding unique constraint?
    created_at = fields.Datetime(string='Created At', default=fields.Datetime.now, readonly=True)
    updated_at = fields.Datetime(string='Updated At', default=fields.Datetime.now, readonly=True)
    deleted_at = fields.Datetime(string='Deleted At', readonly=True, index=True) # Soft delete flag

    # Ensure 'customer_uuid' exists on invoice_management.invoice
    # Ensure 'invoice_management' module is a dependency if this field is used
    invoice_ids = fields.One2many('invoice_management.invoice', 'customer_uuid', string='Invoices')
    # REMOVED //
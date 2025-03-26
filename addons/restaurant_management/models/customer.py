from odoo import models, fields, api
import uuid

class Customer(models.Model):
    _name = 'restaurant_management.customer'
    _description = 'Customer'

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True)
    name = fields.Char(string='Name', required=True)
    birthday = fields.Date(string='Birthday')
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone', required=True)
    created_at = fields.Datetime(string='Created At', default=fields.Datetime.now)
    updated_at = fields.Datetime(string='Updated At', default=fields.Datetime.now)
    deleted_at = fields.Datetime(string='Deleted At')
    
    invoice_ids = fields.One2many('invoice_management.invoice', 'customer_uuid', string='Invoices')
from odoo import models, fields, api

class Customer(models.Model):
    _name = 'restaurant_management.customer'
    _description = 'Customer'

    name = fields.Char(string='Name', required=True)
    birthday = fields.Date(string='Birthday')
    email = fields.Char(string='Email', required=True, unique=True)
    phone = fields.Char(string='Phone', required=True, unique=True)
    created_at = fields.Datetime(string='Created At', default=fields.Datetime.now)
    updated_at = fields.Datetime(string='Updated At', default=fields.Datetime.now)
    deleted_at = fields.Datetime(string='Deleted At')
    
    invoice_ids = fields.One2many('invoice_management.invoice', 'customer_id', string='Invoices')
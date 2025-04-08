from odoo import models, fields, api, _
from odoo.osv import expression
import uuid

class Customer(models.Model):
    _name = 'restaurant_management.customer'
    _description = 'Customer'
    _rec_name = 'name'
    _order = 'name asc'

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True, index=True)
    name = fields.Char(string='Name', required=True, index=True)
    birthday = fields.Date(string='Birthday')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone', required=True)
    created_at = fields.Datetime(string='Created At', default=fields.Datetime.now, readonly=True)
    updated_at = fields.Datetime(string='Updated At', default=fields.Datetime.now, readonly=True)
    deleted_at = fields.Datetime(string='Deleted At', readonly=True, index=True)

    invoice_ids = fields.One2many('restaurant_management.invoice', 'customer_uuid', string='Invoices')

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('phone', operator, name)]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.phone:
                name = f"{name} ({record.phone})"
            result.append((record.id, name))
        return result

    _sql_constraints = [
        ('phone_uniq', 'unique (phone)', "A customer with this phone number already exists!"),
        ('email_uniq', 'unique (email)', "A customer with this email already exists!"),
    ]

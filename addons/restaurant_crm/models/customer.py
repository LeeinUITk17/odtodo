from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.mail import email_normalize
import uuid

class CrmCustomer(models.Model):
    _name = 'restaurant_crm.customer'
    _description = 'Customer (CRM Temporary)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'

    customer_technical_id = fields.Char(
        string='Customer Technical ID',
        required=True,
        copy=False,
        default=lambda self: str(uuid.uuid4()),
        index=True,
        readonly=True
    )
    name = fields.Char(string='Name', required=True, tracking=True)
    birthday = fields.Date(string='Birthday', tracking=True)
    email = fields.Char(string='Email', copy=False, tracking=True)
    phone = fields.Char(string='Phone', required=True, copy=False, tracking=True)
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True,
        help="If unchecked, it will allow you to hide the customer without removing it."
    )

    membership_ids = fields.One2many(
        'restaurant_crm.membership',
        'customer_id',
        string='Memberships'
    )
    log_ids = fields.One2many(
        'restaurant_crm.logs',
        'customer_id',
        string='Activity Logs'
    )

    _sql_constraints = [
        ('customer_technical_id_uniq', 'unique(customer_technical_id)', 'Customer Technical ID must be unique!'),
        ('email_uniq', 'unique(email)', 'Email must be unique if set!'),
        ('phone_uniq', 'unique(phone)', 'Phone must be unique!'),
    ]

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email and not email_normalize(record.email):
                raise ValidationError("Invalid email address!")

    def name_get(self):
        result = []
        for record in self:
            display_name = record.name
            if record.phone:
                display_name = f"{record.name} ({record.phone})"
            result.append((record.id, display_name))
        return result

    def action_view_memberships(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Memberships',
            'res_model': 'restaurant_crm.membership',
            'view_mode': 'tree,form',
            'domain': [('customer_id', '=', self.id)],
            'context': {'default_customer_id': self.id}
        }

    def action_view_logs(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Activity Logs',
            'res_model': 'restaurant_crm.logs',
            'view_mode': 'tree,form',
            'domain': [('customer_id', '=', self.id)],
            'context': {'default_customer_id': self.id}
        }

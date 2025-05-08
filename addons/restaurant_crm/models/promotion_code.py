from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import uuid
import random
import string
import logging

_logger = logging.getLogger(__name__)

class PromotionCode(models.Model):
    _name = 'restaurant_crm.promotion_code'
    _description = 'Promotion Code'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, code'

    promo_technical_id = fields.Char(
        string='Promo Technical ID',
        required=True,
        copy=False,
        default=lambda self: str(uuid.uuid4()),
        index=True,
        readonly=True
    )
    code = fields.Char(
        string='Promotion Code',
        required=True,
        copy=False,
        index=True,
        tracking=True,
        help="The actual code customer will use. Should be unique."
    )
    pool_id = fields.Many2one(
        'restaurant_crm.promotion_pool',
        string='Promotion Pool',
        required=True,
        ondelete='cascade',
        tracking=True,
        index=True
    )
    discount_type = fields.Selection(related='pool_id.discount_type', readonly=True, store=True)
    discount_value = fields.Float(related='pool_id.discount_value', readonly=True, store=True)
    currency_symbol = fields.Char(
        related='pool_id.currency_id.symbol', 
        string='Currency Symbol (from Pool)',
        readonly=True, 
        store=True
    )
    min_order_value = fields.Float(
        related='pool_id.min_order_value',
        string='Min. Order Value (from Pool)',
        readonly=True,
        store=True
    )
    max_discount_value = fields.Float( 
        related='pool_id.max_discount_value',
        string='Max Discount Value (from Pool)',
        readonly=True,
        store=True
    )
    pool_description = fields.Text(
        related='pool_id.description',
        string='Pool Description', 
        readonly=True,
        store=True 
    )
    status = fields.Selection([
        ('ACTIVE', 'Active'),
        ('REDEEMED', 'Redeemed'),
        ('EXPIRED', 'Expired'),
        ('INACTIVE', 'Inactive'),
    ], string='Status', default='ACTIVE', required=True, tracking=True, index=True)
    valid_from = fields.Datetime(
        string='Valid From',
        tracking=True,
        help="The date and time from which this code is valid."
    )
    valid_until = fields.Datetime(
        string='Valid Until',
        tracking=True,
        help="The date and time until which this code is valid. Leave empty for no expiry."
    )
    delivered_user_id = fields.Many2one(
        'restaurant_crm.membership',
        string='Delivered To Membership',
        tracking=True,
        index=True,
        help="If set, only this specific membership (customer) can use this code."
    )
    customer_name = fields.Char(related='delivered_user_id.customer_name', string="Assigned Customer", store=True, readonly=True)
    redeemed_at = fields.Datetime(string='Redeemed At', readonly=True, tracking=True)
    redeemed_by_customer_id = fields.Many2one('restaurant_crm.customer', string='Redeemed By Customer', readonly=True)

    _sql_constraints = [
        ('promo_technical_id_uniq', 'unique(promo_technical_id)', 'Promo Technical ID must be unique!'),
        ('code_uniq', 'unique(code)', 'Promotion Code must be unique!'),
    ]

    @api.onchange('pool_id')
    def _onchange_pool_id(self):
        pass

    @api.model
    def _generate_random_code(self, length=8, prefix='PROMO-'):
        chars = string.ascii_uppercase + string.digits
        random_part = ''.join(random.choice(chars) for _ in range(length))
        return prefix + random_part

    @api.model
    def _generate_random_part(self, length=8):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    @api.model
    def create(self, vals):
        user_provided_code = vals.get('code', '').strip()

        if user_provided_code:
            prefix = user_provided_code
            random_part = self._generate_random_part(8)
            generated_code = prefix + random_part
            counter = 1
            final_code = generated_code
            while self.search_count([('code', '=', final_code)]) > 0:
                final_code = f"{prefix}{random_part}-{counter}"
                counter += 1
                if counter > 100:
                    raise ValidationError(f"Could not generate a unique code with prefix '{prefix}'. Please try a different prefix or ensure codes are unique.")
            vals['code'] = final_code
        else:
            default_prefix = 'PROMO-'
            random_part = self._generate_random_part(8)
            generated_code = default_prefix + random_part
            counter = 1
            final_code = generated_code
            while self.search_count([('code', '=', final_code)]) > 0:
                final_code = f"{default_prefix}{random_part}-{counter}"
                counter += 1
                if counter > 100:
                    raise ValidationError("Could not generate a unique random code. Please try again.")
            vals['code'] = final_code

        if vals.get('pool_id'):
            pool = self.env['restaurant_crm.promotion_pool'].browse(vals['pool_id'])
            if not pool.active:
                raise ValidationError(f"Cannot create promotion code for an inactive pool: {pool.name}")
        return super(PromotionCode, self).create(vals)

    def write(self, vals):
        if 'pool_id' in vals and vals.get('pool_id'):
            pool = self.env['restaurant_crm.promotion_pool'].browse(vals['pool_id'])
            if not pool.active:
                raise ValidationError(f"Cannot assign promotion code to an inactive pool: {pool.name}")
        return super(PromotionCode, self).write(vals)

    def action_redeem_code(self, customer_id, order_id=None, invoice_id=None):
        self.ensure_one()
        if self.status != 'ACTIVE':
            raise UserError(f"Promotion code '{self.code}' is not active (Status: {self.status}).")
        if self.valid_from and self.valid_from > fields.Datetime.now():
            raise UserError(f"Promotion code '{self.code}' is not yet valid (Valid from: {self.valid_from}).")
        if self.valid_until and self.valid_until < fields.Datetime.now():
            self.status = 'EXPIRED'
            self.env.cr.commit()
            raise UserError(f"Promotion code '{self.code}' has expired (Valid until: {self.valid_until}).")
        if self.delivered_user_id and self.delivered_user_id.customer_id.id != customer_id:
            raise UserError(f"Promotion code '{self.code}' is assigned to a different customer.")

        vals_to_write = {
            'status': 'REDEEMED',
            'redeemed_at': fields.Datetime.now(),
            'redeemed_by_customer_id': customer_id,
        }
        self.write(vals_to_write)
        self.env['restaurant_crm.logs'].create({
            'customer_id': customer_id,
            'log_type': 'promo_code_redeemed',
            'content': f"Promotion code '{self.code}' redeemed by customer. Pool: {self.pool_id.name}.",
        })
        return True

    def action_expire_codes(self):
        expired_codes = self.search([
            ('status', '=', 'ACTIVE'),
            ('valid_until', '!=', False),
            ('valid_until', '<', fields.Datetime.now())
        ])
        if expired_codes:
            expired_codes.write({'status': 'EXPIRED'})
            _logger.info(f"Expired {len(expired_codes)} promotion codes.")
        return True

    def name_get(self):
        result = []
        for record in self:
            name = record.code
            if record.pool_id:
                name += f" ({record.pool_id.name})"
            name += f" [{record.status}]"
            result.append((record.id, name))
        return result

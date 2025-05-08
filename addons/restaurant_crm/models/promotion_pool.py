from odoo import models, fields, api
from odoo.exceptions import ValidationError
import uuid

class PromotionPool(models.Model):
    _name = 'restaurant_crm.promotion_pool'
    _description = 'Promotion Pool/Template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    pool_technical_id = fields.Char(
        string='Pool ID',
        required=True,
        copy=False,
        default=lambda self: str(uuid.uuid4()),
        index=True,
        readonly=True
    )
    name = fields.Char(
        string='Pool Name',
        required=True,
        copy=False,
        index=True,
        tracking=True,
        help="A descriptive name for this promotion pool."
    )
    description = fields.Text(string='Description', tracking=True)
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True,
        help="Only active pools can be used to generate codes or in campaigns."
    )
    discount_type = fields.Selection(
        [
            ('PERCENTAGE', 'Percentage Discount'),
            ('FIXED_AMOUNT', 'Fixed Amount Discount'),
        ],
        string='Discount Type',
        required=True,
        default='PERCENTAGE',
        tracking=True
    )
    discount_value = fields.Float(
        string='Discount Value',
        required=True,
        tracking=True,
        help="The actual discount value."
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help="Currency for fixed amount discounts or value limits."
    )
    max_discount_value = fields.Float(
        string='Maximum Discount Amount (for %)',
        tracking=True,
        help="For percentage discounts, this is the maximum monetary value that can be discounted."
    )
    min_order_value = fields.Float(
        string='Minimum Order Value',
        tracking=True,
        help="The minimum total value of an order for this promotion to be applicable."
    )
    promotion_code_ids = fields.One2many(
        'restaurant_crm.promotion_code',
        'pool_id',
        string='Generated Promotion Codes'
    )
    code_count = fields.Integer(
        string="Generated Codes",
        compute="_compute_code_count"
    )
    marketing_campaign_ids = fields.One2many(
        'restaurant_crm.marketing_campaign',
        'promotion_pool_id',
        string='Marketing Campaigns Using This Pool'
    )
    campaign_count = fields.Integer(
        string="Campaigns Using",
        compute="_compute_campaign_count"
    )

    _sql_constraints = [
        ('pool_technical_id_uniq', 'unique(pool_technical_id)', 'Pool ID must be unique!'),
        ('name_uniq', 'unique(name)', 'Promotion Pool Name must be unique!'),
        ('discount_value_positive', 'CHECK(discount_value >= 0)', 'Discount value cannot be negative.'),
        ('max_discount_value_positive', 'CHECK(max_discount_value >= 0)', 'Maximum discount value cannot be negative.'),
        ('min_order_value_positive', 'CHECK(min_order_value >= 0)', 'Minimum order value cannot be negative.'),
    ]

    @api.constrains('discount_type', 'max_discount_value')
    def _check_max_discount_for_percentage(self):
        for record in self:
            if record.discount_type == 'FIXED_AMOUNT' and record.max_discount_value > 0:
                raise ValidationError("Maximum discount value is only applicable for 'Percentage Discount' type.")
            if record.discount_type == 'PERCENTAGE' and record.discount_value > 100:
                raise ValidationError("Percentage discount value cannot exceed 100%.")

    @api.depends('promotion_code_ids')
    def _compute_code_count(self):
        for pool in self:
            pool.code_count = len(pool.promotion_code_ids)

    @api.depends('marketing_campaign_ids')
    def _compute_campaign_count(self):
        for pool in self:
            pool.campaign_count = len(pool.marketing_campaign_ids)

    def name_get(self):
        result = []
        for record in self:
            name_parts = [record.name]
            if record.discount_type == 'PERCENTAGE':
                name_parts.append(f"({record.discount_value}%)")
            elif record.discount_type == 'FIXED_AMOUNT':
                name_parts.append(f"({record.discount_value} {record.currency_id.symbol or ''})")
            result.append((record.id, " ".join(name_parts)))
        return result

    def action_generate_promo_codes_wizard(self):
        self.ensure_one()
        raise ValidationError("Wizard for generating multiple codes is not yet implemented.")

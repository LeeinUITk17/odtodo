from odoo import models, fields, api
from odoo.exceptions import ValidationError
import uuid

class Membership(models.Model):
    _name = 'restaurant_crm.membership'
    _description = 'Customer Membership'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    membership_technical_id = fields.Char(
        string='Membership ID',
        required=True,
        copy=False,
        default=lambda self: str(uuid.uuid4()),
        index=True,
        readonly=True
    )
    customer_id = fields.Many2one(
        'restaurant_crm.customer',
        string='Customer',
        required=True,
        copy=False,
        index=True,
        ondelete='cascade',
        tracking=True
    )
    customer_name = fields.Char(related='customer_id.name', string="Customer Name", store=True, readonly=True)
    customer_phone = fields.Char(related='customer_id.phone', string="Customer Phone", store=True, readonly=True)
    customer_email = fields.Char(related='customer_id.email', string="Customer Email", store=True, readonly=True)

    tier_id = fields.Many2one(
        'restaurant_crm.membership_tier',
        string='Membership Tier',
        ondelete='restrict',
        tracking=True,
        index=True
    )
    points_balance = fields.Integer(string='Points Balance', default=0, tracking=True, readonly=True)
    joined_at = fields.Datetime(string='Joined At', default=fields.Datetime.now, readonly=True, tracking=True)
    status = fields.Selection([
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('PENDING', 'Pending Activation'),
        ('EXPIRED', 'Expired'),
        ('CANCELLED', 'Cancelled')
    ], string='Status', default='ACTIVE', required=True, tracking=True, index=True)

    point_transaction_ids = fields.One2many(
        'restaurant_crm.point_transaction',
        'membership_id',
        string='Point Transactions'
    )
    campaign_delivery_ids = fields.One2many(
        'restaurant_crm.campaign_delivery',
        'membership_id',
        string='Campaign Deliveries'
    )
    delivered_promo_code_ids = fields.One2many(
        'restaurant_crm.promotion_code',
        'delivered_user_id',
        string='Delivered Promo Codes'
    )

    _sql_constraints = [
        ('membership_technical_id_uniq', 'unique(membership_technical_id)', 'Membership ID must be unique!'),
        ('customer_id_active_status_uniq', 'unique(customer_id, status)',
         'A customer can only have one membership with the same active status. Consider archiving old ones before creating a new ACTIVE one.'),
    ]

    @api.model
    def create(self, vals):
        if 'tier_id' not in vals or not vals.get('tier_id'):
            default_tier = self.env['restaurant_crm.membership_tier'].search([], order='min_points asc', limit=1)
            if default_tier:
                vals['tier_id'] = default_tier.id
        record = super(Membership, self).create(vals)
        if vals.get('customer_id'):
            self.env['restaurant_crm.logs'].create({
                'customer_id': vals.get('customer_id'),
                'log_type': 'membership_created',
                'content': f"Membership {record.membership_technical_id} created for customer. Tier: {record.tier_id.name or 'N/A'}.",
            })
        return record

    def write(self, vals):
        for record in self:
            old_tier_name = record.tier_id.name if record.tier_id else "N/A"
            old_status = record.status

            res = super(Membership, record).write(vals)

            new_tier_name = record.tier_id.name if record.tier_id else "N/A"
            new_status = record.status

            log_content_parts = []
            if 'tier_id' in vals and old_tier_name != new_tier_name:
                log_content_parts.append(f"Tier changed from {old_tier_name} to {new_tier_name}.")
            if 'status' in vals and old_status != new_status:
                log_content_parts.append(f"Status changed from {old_status} to {new_status}.")

            if log_content_parts:
                self.env['restaurant_crm.logs'].create({
                    'customer_id': record.customer_id.id,
                    'log_type': 'membership_status_changed' if 'status' in vals else 'tier_update',
                    'content': f"Membership {record.membership_technical_id}: " + " ".join(log_content_parts),
                })
        return res

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.customer_id.name or 'N/A'}'s Membership"
            if record.tier_id:
                name += f" ({record.tier_id.name})"
            if record.membership_technical_id:
                name += f" [{record.membership_technical_id[:8]}...]"
            result.append((record.id, name))
        return result

    def _update_points_balance(self, points_to_add):
        self.ensure_one()
        new_balance = self.points_balance + points_to_add
        self.points_balance = new_balance
        self._check_and_update_tier()
        return new_balance

    def _check_and_update_tier(self):
        self.ensure_one()
        eligible_tiers = self.env['restaurant_crm.membership_tier'].search(
            [('min_points', '<=', self.points_balance)],
            order='min_points desc'
        )
        if eligible_tiers:
            highest_eligible_tier = eligible_tiers[0]
            if self.tier_id != highest_eligible_tier:
                self.tier_id = highest_eligible_tier.id
        else:
            lowest_tier = self.env['restaurant_crm.membership_tier'].search([], order='min_points asc', limit=1)
            if lowest_tier and self.tier_id != lowest_tier:
                self.tier_id = lowest_tier.id

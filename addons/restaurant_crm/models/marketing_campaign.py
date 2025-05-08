from odoo import models, fields, api
from odoo.exceptions import ValidationError
import uuid

class MarketingCampaign(models.Model):
    _name = 'restaurant_crm.marketing_campaign'
    _description = 'Marketing Campaign'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc, name'

    campaign_technical_id = fields.Char(
        string='Campaign ID',
        required=True,
        copy=False,
        default=lambda self: str(uuid.uuid4()),
        index=True,
        readonly=True
    )
    name = fields.Char(string='Campaign Name', required=True, tracking=True, index=True)
    description = fields.Text(string='Description/Goal', tracking=True)
    active = fields.Boolean(string='Active Campaign', default=True, tracking=True)

    status = fields.Selection([
        ('DRAFT', 'Draft'),
        ('SCHEDULED', 'Scheduled'),
        ('ACTIVE', 'Active/Ongoing'),
        ('PAUSED', 'Paused'),
        ('FINISHED', 'Finished/Completed'),
        ('CANCELLED', 'Cancelled'),
    ], string='Status', default='DRAFT', required=True, tracking=True, index=True, copy=False)

    start_date = fields.Datetime(string='Start Date', tracking=True)
    end_date = fields.Datetime(string='End Date', tracking=True)

    delivery_method = fields.Selection([
        ('NONE', 'None (e.g., general promo codes, in-store announcement)'),
        ('EMAIL', 'Email Marketing'),
        ('SMS', 'SMS Marketing'),
        ('PUSH_NOTIFICATION', 'Push Notification'),
        ('IN_APP_MESSAGE', 'In-App Message'),
        ('SOCIAL_MEDIA', 'Social Media Post'),
        ('CALL_CENTER', 'Call Center Outreach'),
    ], string='Primary Delivery Method', default='NONE', tracking=True)

    promotion_pool_id = fields.Many2one(
        'restaurant_crm.promotion_pool',
        string='Associated Promotion Pool',
        ondelete='restrict',
        tracking=True,
        domain="[('active', '=', True)]",
        help="Select a promotion pool if this campaign offers discounts or promotions."
    )
    pool_discount_info = fields.Char(string="Pool Discount", compute="_compute_pool_discount_info", store=False)

    campaign_delivery_ids = fields.One2many(
        'restaurant_crm.campaign_delivery',
        'campaign_id',
        string='Delivered To Members'
    )
    delivered_member_count = fields.Integer(string="Members Reached", compute="_compute_delivered_member_count", store=True)

    _sql_constraints = [
        ('campaign_technical_id_uniq', 'unique(campaign_technical_id)', 'Campaign ID must be unique!'),
        ('name_uniq', 'unique(name)', 'Campaign Name must be unique!'),
        ('check_dates', 'CHECK(end_date IS NULL OR start_date IS NULL OR end_date >= start_date)', 'End date must be after start date.')
    ]

    @api.depends('promotion_pool_id', 'promotion_pool_id.discount_type', 'promotion_pool_id.discount_value', 'promotion_pool_id.currency_id')
    def _compute_pool_discount_info(self):
        for campaign in self:
            if campaign.promotion_pool_id:
                pool = campaign.promotion_pool_id
                if pool.discount_type == 'PERCENTAGE':
                    campaign.pool_discount_info = f"{pool.discount_value}% off"
                    if pool.max_discount_value:
                        campaign.pool_discount_info += f" (max {pool.max_discount_value} {pool.currency_id.symbol or ''})"
                elif pool.discount_type == 'FIXED_AMOUNT':
                    campaign.pool_discount_info = f"{pool.discount_value} {pool.currency_id.symbol or ''} off"
                else:
                    campaign.pool_discount_info = "Custom"
            else:
                campaign.pool_discount_info = "No specific promotion pool"

    @api.depends('campaign_delivery_ids')
    def _compute_delivered_member_count(self):
        for campaign in self:
            campaign.delivered_member_count = len(campaign.campaign_delivery_ids)

    def name_get(self):
        return [(record.id, f"{record.name} [{record.status}]") for record in self]

    def action_schedule(self):
        for rec in self.filtered(lambda r: r.status == 'DRAFT'):
            if not rec.start_date:
                raise ValidationError("Please set a start date before scheduling.")
            rec.status = 'SCHEDULED'

    def action_launch(self):
        for rec in self.filtered(lambda r: r.status in ['DRAFT', 'SCHEDULED', 'PAUSED']):
            rec.status = 'ACTIVE'
            if not rec.start_date:
                rec.start_date = fields.Datetime.now()

    def action_pause(self):
        for rec in self.filtered(lambda r: r.status == 'ACTIVE'):
            rec.status = 'PAUSED'

    def action_finish(self):
        for rec in self.filtered(lambda r: r.status in ['ACTIVE', 'PAUSED']):
            rec.status = 'FINISHED'
            if not rec.end_date:
                rec.end_date = fields.Datetime.now()

    def action_cancel(self):
        for rec in self.filtered(lambda r: r.status not in ['FINISHED', 'CANCELLED']):
            rec.status = 'CANCELLED'

    def action_reset_to_draft(self):
        for rec in self.filtered(lambda r: r.status in ['SCHEDULED', 'PAUSED', 'CANCELLED']):
            rec.status = 'DRAFT'

    def action_assign_to_members_wizard(self):
        self.ensure_one()
        raise ValidationError("Wizard for assigning members is not yet implemented.")

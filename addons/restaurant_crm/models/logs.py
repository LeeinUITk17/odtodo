from odoo import models, fields, api
import uuid

class CrmLogs(models.Model):
    _name = 'restaurant_crm.logs'
    _description = 'Customer Activity Log (CRM Temporary)'
    _order = 'create_date desc'

    log_technical_id = fields.Char(
        string='Log Technical ID',
        required=True,
        copy=False,
        default=lambda self: str(uuid.uuid4()),
        index=True,
        readonly=True
    )
    customer_id = fields.Many2one(
        'restaurant_crm.customer',
        string='Customer',
        ondelete='set null',
        index=True
    )
    customer_name = fields.Char(related='customer_id.name', string="Customer Name", store=False, readonly=True)
    log_type = fields.Selection([
        ('tier_update', 'Tier Update'),
        ('point_redeem', 'Point Redeem'),
        ('point_earn', 'Point Earn'),
        ('point_bonus', 'Point Bonus Awarded'),
        ('point_expiry', 'Point Expired'),
        ('point_adjustment', 'Point Manual Adjustment'),
        ('membership_created', 'Membership Created'),
        ('membership_status_changed', 'Membership Status Changed'),
        ('campaign_assigned', 'Campaign Assigned'),
        ('promo_code_redeemed', 'Promo Code Redeemed by Customer'),
        ('manual_note', 'Manual Note'),
    ], string='Log Type', required=True)
    content = fields.Text(string='Details', required=True)
    user_id = fields.Many2one('res.users', string='Responsible User', default=lambda self: self.env.user, readonly=True)

    _sql_constraints = [
        ('log_technical_id_uniq', 'unique(log_technical_id)', 'Log Technical ID must be unique!'),
    ]

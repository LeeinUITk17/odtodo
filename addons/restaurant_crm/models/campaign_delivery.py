from odoo import models, fields, api

class CampaignDelivery(models.Model):
    _name = 'restaurant_crm.campaign_delivery'
    _description = 'Campaign Delivery to Membership'
    _order = 'assigned_at desc, campaign_id, membership_id'

    campaign_id = fields.Many2one(
        'restaurant_crm.marketing_campaign',
        string='Campaign',
        required=True,
        ondelete='cascade',
        index=True
    )
    membership_id = fields.Many2one(
        'restaurant_crm.membership',
        string='Membership',
        required=True,
        ondelete='cascade',
        index=True
    )
    customer_id = fields.Many2one(
        related="membership_id.customer_id", 
        string="Customer", 
        store=True, 
        readonly=True
    )
    campaign_name = fields.Char(
        related='campaign_id.name', 
        string="Campaign Name", 
        store=False, 
        readonly=True
    )
    customer_name = fields.Char(
        related='membership_id.customer_id.name', 
        string="Customer Name", 
        store=False, 
        readonly=True
    )
    assigned_at = fields.Datetime(
        string='Assigned/Delivered At', 
        default=fields.Datetime.now, 
        required=True, 
        readonly=True
    )

    _sql_constraints = [
        ('campaign_membership_uniq', 'unique(campaign_id, membership_id)',
         'A membership can only be targeted once per campaign directly through this record. If re-targeting is needed, consider a new campaign or a different mechanism.')
    ]

    def name_get(self):
        result = []
        for record in self:
            name = f"Campaign '{record.campaign_id.name or 'N/A'}' for {record.membership_id.customer_name or 'N/A'}"
            result.append((record.id, name))
        return result
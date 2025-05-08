from odoo import models, fields, api

class MembershipTier(models.Model):
    _name = 'restaurant_crm.membership_tier'
    _description = 'Membership Tier'
    _order = 'min_points asc, name'

    name = fields.Char(string='Tier Name', required=True, copy=False, index=True)
    description = fields.Text(string='Description')
    min_points = fields.Integer(
        string='Minimum Points Required',
        required=True,
        default=0,
        help="Minimum points a member needs to achieve this tier."
    )
    membership_ids = fields.One2many(
        'restaurant_crm.membership',
        'tier_id',
        string='Members in this Tier'
    )
    member_count = fields.Integer(string="Member Count", compute="_compute_member_count", store=False)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Tier Name must be unique!'),
        ('min_points_non_negative', 'CHECK(min_points >= 0)', 'Minimum points cannot be negative.'),
    ]

    @api.depends('membership_ids')
    def _compute_member_count(self):
        for tier in self:
            tier.member_count = len(tier.membership_ids)

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.name} (Min: {record.min_points} pts)"
            result.append((record.id, name))
        return result

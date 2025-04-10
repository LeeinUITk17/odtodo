from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    branch_id = fields.Many2one(
        'restaurant_management.branch',
        string='Assigned Branch',
        help="The primary branch this user is assigned to."
    )

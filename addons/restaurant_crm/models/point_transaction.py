from odoo import models, fields, api
from odoo.exceptions import UserError
import uuid

class PointTransaction(models.Model):
    _name = 'restaurant_crm.point_transaction'
    _description = 'Membership Point Transaction'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    transaction_technical_id = fields.Char(
        string='Transaction ID',
        required=True,
        copy=False,
        default=lambda self: str(uuid.uuid4()),
        index=True,
        readonly=True
    )
    membership_id = fields.Many2one(
        'restaurant_crm.membership',
        string='Membership',
        required=True,
        ondelete='cascade',
        index=True,
        tracking=True
    )
    customer_id = fields.Many2one(related='membership_id.customer_id', string="Customer", store=True, readonly=True)
    customer_name = fields.Char(related='membership_id.customer_id.name', string="Customer Name", store=True, readonly=True)
    tier_name = fields.Char(related='membership_id.tier_id.name', string="Current Tier", store=True, readonly=True)

    amount = fields.Integer(
        string='Points Amount',
        required=True,
        tracking=True,
        help="Positive for earning/bonus, negative for redeeming/expiry/adjustment down."
    )
    type = fields.Selection([
        ('EARN', 'Earned Points'),
        ('REDEEM', 'Redeemed Points'),
        ('BONUS', 'Bonus Points'),
        ('ADJUSTMENT_UP', 'Manual Adjustment (Up)'),
        ('ADJUSTMENT_DOWN', 'Manual Adjustment (Down)'),
        ('EXPIRY', 'Expired Points'),
        ('INITIAL', 'Initial Balance'),
        ('TIER_BONUS', 'Tier Achievement Bonus')
    ], string='Transaction Type', required=True, tracking=True, index=True)

    description = fields.Text(string='Description/Reason', tracking=True)
    source_reference = fields.Char(
        string='Source Reference',
        tracking=True,
        help="Reference to the source of this transaction."
    )
    expires_at = fields.Datetime(
        string='Points Expiry Date',
        tracking=True,
        help="Date when these specific points will expire."
    )
    user_id = fields.Many2one('res.users', string='Processed By', default=lambda self: self.env.user, readonly=True, tracking=True)

    _sql_constraints = [
        ('transaction_technical_id_uniq', 'unique(transaction_technical_id)', 'Transaction ID must be unique!'),
        ('check_adjustment_down_amount_negative', "CHECK(NOT (type = 'ADJUSTMENT_DOWN' AND amount > 0))", "Amount for 'Adjustment Down' must be zero or negative."),
        ('check_adjustment_up_amount_positive', "CHECK(NOT (type = 'ADJUSTMENT_UP' AND amount < 0))", "Amount for 'Adjustment Up' must be zero or positive."),
        ('check_redeem_amount_negative', "CHECK(NOT (type = 'REDEEM' AND amount > 0))", "Amount for 'Redeem' must be zero or negative."),
        ('check_expiry_amount_negative', "CHECK(NOT (type = 'EXPIRY' AND amount > 0))", "Amount for 'Expiry' must be zero or negative."),
        ('check_earn_amount_positive', "CHECK(NOT (type = 'EARN' AND amount < 0))", "Amount for 'Earn' must be zero or positive."),
        ('check_bonus_amount_positive', "CHECK(NOT (type = 'BONUS' AND amount < 0))", "Amount for 'Bonus' must be zero or positive."),
        ('check_tier_bonus_amount_positive', "CHECK(NOT (type = 'TIER_BONUS' AND amount < 0))", "Amount for 'Tier Bonus' must be zero or positive."),
    ]

    @api.model
    def create(self, vals):
        trans_type = vals.get('type')
        amount = vals.get('amount', 0)

        if trans_type in ('REDEEM', 'EXPIRY', 'ADJUSTMENT_DOWN') and amount > 0:
            vals['amount'] = -amount
        elif trans_type in ('EARN', 'BONUS', 'ADJUSTMENT_UP', 'TIER_BONUS', 'INITIAL') and amount < 0:
            raise UserError("Amount for earning/bonus/initial/adjustment up types must be positive.")

        transaction = super(PointTransaction, self).create(vals)

        if transaction.membership_id and transaction.amount != 0:
            transaction.membership_id._update_points_balance(transaction.amount)

            log_type = 'point_earn' if transaction.amount > 0 else 'point_redeem'
            if trans_type == 'BONUS':
                log_type = 'point_bonus'
            elif trans_type == 'EXPIRY':
                log_type = 'point_expiry'
            elif trans_type in ('ADJUSTMENT_UP', 'ADJUSTMENT_DOWN'):
                log_type = 'point_adjustment'

            self.env['restaurant_crm.logs'].create({
                'customer_id': transaction.membership_id.customer_id.id,
                'log_type': log_type,
                'content': f"{abs(transaction.amount)} points {trans_type.lower().replace('_', ' ')} for membership {transaction.membership_id.membership_technical_id}. "
                           f"Reason: {transaction.description or 'N/A'}. "
                           f"New balance: {transaction.membership_id.points_balance}.",
                'user_id': transaction.user_id.id,
            })
        return transaction

    def write(self, vals):
        if any(field in vals for field in ['amount', 'type', 'membership_id']):
            for rec in self:
                if rec.create_uid.id != self.env.uid and not self.env.user.has_group('base.group_system'):
                    raise UserError("Cannot modify critical fields (amount, type, membership) of a point transaction after creation. Please create an adjustment transaction instead.")
        return super(PointTransaction, self).write(vals)

    def unlink(self):
        for transaction in self:
            if transaction.membership_id and transaction.amount != 0:
                pass
        return super(PointTransaction, self).unlink()

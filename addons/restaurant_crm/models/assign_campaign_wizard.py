from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class AssignCampaignWizard(models.TransientModel):
    _name = 'restaurant_crm.assign_campaign_wizard'
    _description = 'Wizard to Assign Campaign to Memberships'

    campaign_id = fields.Many2one(
        'restaurant_crm.marketing_campaign',
        string='Marketing Campaign',
        required=True,
        readonly=True
    )
    promotion_pool_id = fields.Many2one(
        related='campaign_id.promotion_pool_id',
        string="Promotion Pool",
        readonly=True
    )
    campaign_name = fields.Char(
        related='campaign_id.name',
        string="Campaign Name",
        readonly=True
    )
    target_tier_ids = fields.Many2many(
        'restaurant_crm.membership_tier',
        relation='crm_assign_wizard_tier_rel',
        column1='wizard_id',
        column2='tier_id',
        string='Target Membership Tiers'
    )
    target_status = fields.Selection([
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('PENDING', 'Pending Activation'),
    ], string='Target Membership Status', default='ACTIVE', required=True)
    target_membership_ids = fields.Many2many(
        'restaurant_crm.membership',
        relation='crm_assign_wizard_membership_rel',
        column1='wizard_id',
        column2='membership_id',
        string='Select Specific Members'
    )
    assign_existing_promo_code = fields.Boolean(
        string="Assign Available Promo Code?"
    )

    @api.model
    def default_get(self, fields_list):
        res = super(AssignCampaignWizard, self).default_get(fields_list)
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')

        if active_model == 'restaurant_crm.marketing_campaign' and active_id:
            campaign = self.env['restaurant_crm.marketing_campaign'].browse(active_id)
            if 'campaign_id' in fields_list:
                res['campaign_id'] = campaign.id
            if 'assign_existing_promo_code' in fields_list:
                res['assign_existing_promo_code'] = bool(campaign.promotion_pool_id)
        return res

    def action_assign_campaign(self):
        self.ensure_one()
        _logger.info(f"Starting campaign assignment for campaign ID: {self.campaign_id.id}")

        CampaignDelivery = self.env['restaurant_crm.campaign_delivery']
        Membership = self.env['restaurant_crm.membership']
        PromotionCode = self.env['restaurant_crm.promotion_code']
        members_to_assign = self.env['restaurant_crm.membership']

        base_domain = [('status', '=', self.target_status)] if self.target_status else [('status', '=', 'ACTIVE')]

        members_from_tiers = Membership
        if self.target_tier_ids:
            tier_domain = base_domain + [('tier_id', 'in', self.target_tier_ids.ids)]
            members_from_tiers = Membership.search(tier_domain)
            members_to_assign |= members_from_tiers

        members_manual = Membership
        if self.target_membership_ids:
            manual_domain = base_domain + [('id', 'in', self.target_membership_ids.ids)]
            members_manual = Membership.search(manual_domain)
            members_to_assign |= members_manual

        if not self.target_tier_ids and not self.target_membership_ids:
            all_members_by_status = Membership.search(base_domain)
            members_to_assign |= all_members_by_status

        if not members_to_assign:
            raise UserError("No members found matching the selected criteria.")

        existing_deliveries = CampaignDelivery.search([
            ('campaign_id', '=', self.campaign_id.id),
            ('membership_id', 'in', members_to_assign.ids)
        ])
        existing_member_ids = set(existing_deliveries.mapped('membership_id').ids)

        new_delivery_vals_list = []
        skipped_count = 0
        assigned_code_count = 0
        members_no_code = []

        should_assign_code = self.assign_existing_promo_code and self.promotion_pool_id

        available_codes = self.env['restaurant_crm.promotion_code']
        if should_assign_code:
            available_codes = PromotionCode.search([
                ('pool_id', '=', self.promotion_pool_id.id),
                ('status', '=', 'ACTIVE'),
                ('delivered_user_id', '=', False),
                '|', ('valid_until', '=', False), ('valid_until', '>=', fields.Datetime.now())
            ], order='id')
            available_codes_list = list(available_codes)

        for member in members_to_assign:
            if member.id not in existing_member_ids:
                delivery_vals = {
                    'campaign_id': self.campaign_id.id,
                    'membership_id': member.id,
                }
                new_delivery_vals_list.append(delivery_vals)

                if should_assign_code:
                    assigned_code_success = False
                    if available_codes_list:
                        code_to_assign = available_codes_list.pop(0)
                        try:
                            code_to_assign.write({'delivered_user_id': member.id})
                            assigned_code_count += 1
                            assigned_code_success = True
                            member.message_post(body=f"Assigned promotion code '{code_to_assign.code}' from campaign '{self.campaign_id.name}'.")
                        except Exception as e:
                            available_codes_list.insert(0, code_to_assign)
                            members_no_code.append(member.customer_name or f"ID {member.id}")
                    else:
                        members_no_code.append(member.customer_name or f"ID {member.id}")

                    if not assigned_code_success and member.customer_name not in members_no_code:
                        members_no_code.append(member.customer_name or f"ID {member.id}")
            else:
                skipped_count += 1

        created_deliveries = CampaignDelivery.create(new_delivery_vals_list) if new_delivery_vals_list else self.env['restaurant_crm.campaign_delivery']
        delivery_count = len(created_deliveries)

        log_parts = []
        if delivery_count > 0:
            log_parts.append(f"Assigned campaign to {delivery_count} new members.")
        if should_assign_code:
            log_parts.append(f"Attempted to assign promo codes: {assigned_code_count} assigned successfully.")
        if skipped_count > 0:
            log_parts.append(f"Skipped {skipped_count} members already assigned.")
        if members_no_code:
            display_members = ', '.join(members_no_code[:5])
            if len(members_no_code) > 5:
                display_members += "..."
            log_parts.append(f"Could not assign codes to {len(members_no_code)} members: {display_members}.")

        final_message = " ".join(log_parts) if log_parts else "No new assignments needed or possible."

        if delivery_count > 0 or assigned_code_count > 0 or skipped_count > 0 or members_no_code:
            self.campaign_id.message_post(body=f"Assign Members Wizard Result: {final_message}")

        notification_type = 'info'
        if delivery_count > 0 or assigned_code_count > 0:
            notification_type = 'success'
        if members_no_code and notification_type == 'success':
            notification_type = 'warning'
        elif not log_parts:
            final_message = "No new members were assigned (either already assigned or none matched criteria)."

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Assignment Result',
                'message': final_message,
                'type': notification_type,
                'sticky': True,
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }

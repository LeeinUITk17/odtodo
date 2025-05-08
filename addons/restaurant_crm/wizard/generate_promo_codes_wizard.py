# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import random
import string

class GeneratePromoCodesWizard(models.TransientModel):
    _name = 'restaurant_crm.generate_codes_wizard'
    _description = 'Wizard to Generate Multiple Promotion Codes'

    pool_id = fields.Many2one(
        'restaurant_crm.promotion_pool',
        string='Target Promotion Pool',
        required=True,
        domain="[('active', '=', True)]",
        help="Select the pool for which codes will be generated."
    )
    quantity = fields.Integer(
        string='Number of Codes to Generate',
        required=True,
        default=10,
        help="How many unique codes do you want to create?"
    )
    code_prefix = fields.Char(
        string='Code Prefix (Optional)',
        help="E.g., 'SUMMER24-'. If empty, a default prefix might be used or codes will be purely random based on length."
    )
    code_length = fields.Integer(
        string='Length of Random Part',
        default=8,
        help="Length of the auto-generated random part of the code (excluding prefix)."
    )
    valid_from = fields.Datetime(string='Valid From (Optional for this batch)')
    valid_until = fields.Datetime(string='Valid Until (Optional for this batch)')

    def _generate_single_code(self, prefix, length):
        chars = string.ascii_uppercase + string.digits
        random_part = ''.join(random.choice(chars) for _ in range(length))
        return (prefix or '') + random_part

    def action_generate_codes(self):
        self.ensure_one()
        if self.quantity <= 0:
            raise UserError("Number of codes to generate must be positive.")
        if self.code_length <= 0:
            raise UserError("Length of random part must be positive.")

        PromotionCode = self.env['restaurant_crm.promotion_code']
        generated_codes_count = 0
        generated_code_list = []

        if not self.pool_id.active:
            raise ValidationError(f"Cannot generate codes for an inactive pool: {self.pool_id.name}")

        for i in range(self.quantity):
            attempts = 0
            max_attempts = 100
            new_code_str = None

            while attempts < max_attempts:
                potential_code = self._generate_single_code(self.code_prefix, self.code_length)
                if attempts > 10 and len(potential_code) < 10:
                    potential_code += str(random.randint(0, 9))

                if not PromotionCode.search_count([('code', '=', potential_code)]):
                    new_code_str = potential_code
                    break
                attempts += 1
            
            if not new_code_str:
                if generated_codes_count > 0:
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'title': 'Partial Generation',
                            'message': f'{generated_codes_count} codes generated successfully. Could not generate all requested unique codes.',
                            'sticky': True,
                            'type': 'warning',
                            'next': {'type': 'ir.actions.act_window_close'},
                        }
                    }
                else:
                    raise UserError(f"Failed to generate any unique codes with the given prefix/length after {max_attempts} attempts. Please try different parameters.")

            code_vals = {
                'pool_id': self.pool_id.id,
                'code': new_code_str,
                'status': 'ACTIVE',
            }
            if self.valid_from:
                code_vals['valid_from'] = self.valid_from
            if self.valid_until:
                code_vals['valid_until'] = self.valid_until

            try:
                new_promo_code = PromotionCode.create(code_vals)
                generated_codes_count += 1
                generated_code_list.append(new_promo_code.code)
            except Exception as e:
                _logger.error(f"Error creating promotion code '{new_code_str}': {e}")

        if generated_codes_count > 0:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Success',
                    'message': f'{generated_codes_count} promotion codes generated successfully for pool "{self.pool_id.name}".',
                    'sticky': True,
                    'type': 'success',
                    'next': {'type': 'ir.actions.act_window_close'},
                }
            }
        return {'type': 'ir.actions.act_window_close'}

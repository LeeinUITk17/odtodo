from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AddMenuItemWizard(models.TransientModel):
    _name = 'restaurant_management.add.menu.item.wizard'
    _description = 'Wizard to Add Menu Item to Order'

    order_id = fields.Many2one('restaurant_management.order', string='Order', required=True, readonly=True)
    menu_item_id = fields.Many2one('restaurant_management.menuitem', string='Menu Item', required=True, readonly=True)
    quantity = fields.Integer(string='Quantity', required=True, default=1)

    # Optional: Display item name/price for confirmation
    menu_item_name = fields.Char(related='menu_item_id.name', string="Item Name", readonly=True)
    unit_price = fields.Monetary(related='menu_item_id.price', string="Unit Price", readonly=True)
    currency_id = fields.Many2one(related='menu_item_id.currency_id', readonly=True)

    @api.constrains('quantity')
    def _check_quantity(self):
        if any(wizard.quantity <= 0 for wizard in self):
            raise UserError(_('Quantity must be positive.'))

    def action_confirm_add_item(self):
        self.ensure_one()
        # Call the method on the order model
        self.order_id.add_menu_item_from_ui(self.menu_item_id.id, self.quantity)
        # No need to return anything, wizard closes automatically
        return {'type': 'ir.actions.act_window_close'}
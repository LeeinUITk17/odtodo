from odoo import models, fields, api, _
from odoo.exceptions import UserError # Import UserError
import uuid

class Order(models.Model):
    _name = 'restaurant_management.order'
    # ... (các trường khác giữ nguyên) ...
    _description = 'Restaurant Order'
    _order = 'created_at desc'

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True, index=True)
    name = fields.Char(string="Order Reference", required=True, copy=False, readonly=True, default=lambda self: _('New'), index=True)
    status = fields.Selection([
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELED', 'Canceled')
    ], string='Status', default='PENDING', required=True, tracking=True)
    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True, tracking=True)
    created_at = fields.Datetime(string='Created At', default=fields.Datetime.now, readonly=True)
    updated_at = fields.Datetime(string='Updated At', default=fields.Datetime.now, readonly=True)

    table_uuid = fields.Many2one('restaurant_management.table', string='Table', ondelete='set null', tracking=True,
                                 domain="[('branch_uuid', '=', branch_uuid)]")
    branch_uuid = fields.Many2one('restaurant_management.branch', string='Branch', required=True, ondelete='cascade', tracking=True)
    order_items = fields.One2many('restaurant_management.orderitem', 'order_uuid', string='Order Items')

    # --- NEW FIELD ---
    # This field is used to display available menu items in the form view's kanban
    available_menu_item_ids = fields.Many2many(
        'restaurant_management.menuitem',
        string="Available Menu Items",
        compute='_compute_available_menu_items',
        store=False,  # Do not store this field
        readonly=True # This field is just for display/selection
    )

    @api.depends('branch_uuid')
    def _compute_available_menu_items(self):
        """ Compute the list of menu items available for the selected branch """
        for order in self:
            if order.branch_uuid:
                # Adjust domain if you have soft delete or active field on menuitem
                domain = [('branch_uuid', '=', order.branch_uuid.id)] # , ('active', '=', True)
                order.available_menu_item_ids = self.env['restaurant_management.menuitem'].search(domain)
            else:
                order.available_menu_item_ids = self.env['restaurant_management.menuitem'].browse() # Empty recordset


    # --- NEW METHOD (Called via Wizard is safer) ---
    # This method adds or updates an order item based on the selected menu item
    # Note: Calling this directly from Kanban button requires careful context passing
    # Using a transient wizard (next step) is generally more robust for complex actions
    def add_menu_item_from_ui(self, menu_item_id, quantity=1):
        """ Adds or updates quantity for a menu item in the order. """
        self.ensure_one() # Ensure this runs on a single order record

        if self.status != 'PENDING':
             raise UserError(_("You can only add items to Pending orders."))

        if not menu_item_id:
            raise UserError(_("Menu item not specified."))

        menu_item = self.env['restaurant_management.menuitem'].browse(menu_item_id)
        if not menu_item.exists():
             raise UserError(_("Selected Menu Item does not exist."))

        # Find existing order item for this menu item
        existing_item = self.order_items.filtered(lambda item: item.menu_item_uuid.id == menu_item_id)

        if existing_item:
            # Increase quantity of existing item
            existing_item.quantity += quantity
        else:
            # Create a new order item
            self.env['restaurant_management.orderitem'].create({
                'order_uuid': self.id,
                'menu_item_uuid': menu_item_id,
                'quantity': quantity,
                # unitPrice will be computed based on the menu item
            })
        # Returning an action can help refresh the view, but might not be needed if UI updates automatically
        # return {'type': 'ir.actions.do_nothing'} # Basic way to signal success


    @api.depends('order_items.quantity', 'order_items.unitPrice')
    def _compute_total_price(self):
         # ... (keep existing logic) ...
        for order in self:
            order.total_price = sum(item.subtotal for item in order.order_items) # Use subtotal


    # ... (keep other methods like create, write, action_complete, etc.) ...
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('restaurant.order.sequence') or _('New')
        return super().create(vals_list)

    def write(self, vals):
        if 'updated_at' not in vals:
             vals['updated_at'] = fields.Datetime.now()
        return super(Order, self).write(vals)

    def action_complete(self):
        # ... keep existing ...
        allowed_statuses = ['PENDING']
        if any(rec.status not in allowed_statuses for rec in self):
            raise UserError(_("Only Pending orders can be marked as Completed."))
        return self.write({'status': 'COMPLETED'})

    def action_cancel(self):
        # ... keep existing ...
        allowed_statuses = ['PENDING', 'COMPLETED']
        if any(rec.status not in allowed_statuses for rec in self):
             raise UserError(_("Only Pending or Completed orders can be Canceled."))
        return self.write({'status': 'CANCELED'})

    def action_reset_to_pending(self):
        # ... keep existing ...
        allowed_statuses = ['COMPLETED', 'CANCELED']
        if any(rec.status not in allowed_statuses for rec in self):
            raise UserError(_("Only Completed or Canceled orders can be reset to Pending."))
        return self.write({'status': 'PENDING'})
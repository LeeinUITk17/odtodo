from odoo import models, api

class OrderService(models.AbstractModel):
    _name = 'order_management.order_service'
    _description = 'Order Service'

    @api.model
    def create_order(self, vals):
        """Create a new order."""
        return self.env['order_management.order'].create(vals)

    @api.model
    def read_order(self, uuid):
        """Read an order by UUID."""
        order = self.env['order_management.order'].search([('uuid', '=', uuid)], limit=1)
        if order:
            return order.read()
        return False

    @api.model
    def update_order(self, uuid, vals):
        """Update an existing order."""
        order = self.env['order_management.order'].search([('uuid', '=', uuid)], limit=1)
        if order:
            order.write(vals)
            return order.read()
        return False

    @api.model
    def delete_order(self, uuid):
        """Delete an order by UUID."""
        order = self.env['order_management.order'].search([('uuid', '=', uuid)], limit=1)
        if order:
            order.unlink()
            return True
        return False
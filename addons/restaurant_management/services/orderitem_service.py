from odoo import models, api

class OrderItemService(models.AbstractModel):
    _name = 'restaurant_management.orderitem_service'
    _description = 'Order Item Service'

    @api.model
    def create_orderitem(self, vals):
        return self.env['restaurant_management.orderitem'].create(vals)

    @api.model
    def read_orderitem(self, uuid):
        orderitem = self.env['restaurant_management.orderitem'].search([('uuid', '=', uuid)], limit=1)
        if orderitem:
            return orderitem.read()
        return False

    @api.model
    def update_orderitem(self, uuid, vals):
        orderitem = self.env['restaurant_management.orderitem'].search([('uuid', '=', uuid)], limit=1)
        if orderitem:
            orderitem.write(vals)
            return orderitem.read()
        return False

    @api.model
    def delete_orderitem(self, uuid):
        orderitem = self.env['restaurant_management.orderitem'].search([('uuid', '=', uuid)], limit=1)
        if orderitem:
            orderitem.unlink()
            return True
        return False
from odoo import models, api

class CustomerService(models.AbstractModel):
    _name = 'restaurant_management.customer_service'
    _description = 'Customer Service'

    @api.model
    def create_customer(self, vals):
        return self.env['restaurant_management.customer'].create(vals)

    @api.model
    def read_customer(self, uuid):
        customer = self.env['restaurant_management.customer'].search([('uuid', '=', uuid)], limit=1)
        if customer:
            return customer.read()
        return False

    @api.model
    def update_customer(self, uuid, vals):
        customer = self.env['restaurant_management.customer'].search([('uuid', '=', uuid)], limit=1)
        if customer:
            customer.write(vals)
            return customer.read()
        return False

    @api.model
    def delete_customer(self, uuid):
        customer = self.env['restaurant_management.customer'].search([('uuid', '=', uuid)], limit=1)
        if customer:
            customer.unlink()
            return True
        return False
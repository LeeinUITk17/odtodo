from odoo import models, api

class CustomerService(models.AbstractModel):
    _name = 'restaurant_management.customer_service'
    _description = 'Customer Service'

    @api.model
    def create_customer(self, vals):
        return self.env['restaurant_management.customer'].create(vals)

    @api.model
    def read_customer(self, customer_id):
        return self.env['restaurant_management.customer'].browse(customer_id).read()

    @api.model
    def update_customer(self, customer_id, vals):
        customer = self.env['restaurant_management.customer'].browse(customer_id)
        customer.write(vals)
        return customer

    @api.model
    def delete_customer(self, customer_id):
        customer = self.env['restaurant_management.customer'].browse(customer_id)
        customer.unlink()
        return True
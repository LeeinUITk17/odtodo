from odoo import http
from odoo.http import request

class CustomerController(http.Controller):

    @http.route('/customers', type='json', auth='user')
    def list_customers(self):
        customers = request.env['restaurant_management.customer'].search([])
        return customers.read()

    @http.route('/customers/<int:customer_id>', type='json', auth='user')
    def get_customer(self, customer_id):
        customer = request.env['restaurant_management.customer'].browse(customer_id)
        return customer.read()

    @http.route('/customers', type='json', auth='user', methods=['POST'])
    def create_customer(self, **kwargs):
        customer_service = request.env['restaurant_management.customer_service']
        customer = customer_service.create_customer(kwargs)
        return customer.read()

    @http.route('/customers/<int:customer_id>', type='json', auth='user', methods=['PUT'])
    def update_customer(self, customer_id, **kwargs):
        customer_service = request.env['restaurant_management.customer_service']
        customer = customer_service.update_customer(customer_id, kwargs)
        return customer.read()

    @http.route('/customers/<int:customer_id>', type='json', auth='user', methods=['DELETE'])
    def delete_customer(self, customer_id):
        customer_service = request.env['restaurant_management.customer_service']
        customer_service.delete_customer(customer_id)
        return {'status': 'success'}
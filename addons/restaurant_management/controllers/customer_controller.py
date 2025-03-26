from odoo import http
from odoo.http import request

class CustomerController(http.Controller):

    @http.route('/customers', type='json', auth='user')
    def list_customers(self):
        customers = request.env['restaurant_management.customer'].search([])
        return customers.read()

    @http.route('/customers/<string:uuid>', type='json', auth='user')
    def get_customer(self, uuid):
        customer_service = request.env['restaurant_management.customer_service']
        customer = customer_service.read_customer(uuid)
        return {'status': 'success', 'data': customer} if customer else {'status': 'error', 'message': 'Customer not found'}

    @http.route('/customers', type='json', auth='user', methods=['POST'])
    def create_customer(self, **kwargs):
        customer_service = request.env['restaurant_management.customer_service']
        customer = customer_service.create_customer(kwargs)
        return {'status': 'success', 'data': customer.read()} if customer else {'status': 'error', 'message': 'Failed to create customer'}

    @http.route('/customers/<string:uuid>', type='json', auth='user', methods=['PUT'])
    def update_customer(self, uuid, **kwargs):
        customer_service = request.env['restaurant_management.customer_service']
        customer = customer_service.update_customer(uuid, kwargs)
        return {'status': 'success', 'data': customer} if customer else {'status': 'error', 'message': 'Customer not found or update failed'}

    @http.route('/customers/<string:uuid>', type='json', auth='user', methods=['DELETE'])
    def delete_customer(self, uuid):
        customer_service = request.env['restaurant_management.customer_service']
        success = customer_service.delete_customer(uuid)
        return {'status': 'success'} if success else {'status': 'error', 'message': 'Customer not found or delete failed'}
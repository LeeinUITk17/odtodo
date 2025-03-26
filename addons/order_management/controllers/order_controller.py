from odoo import http
from odoo.http import request

class OrderController(http.Controller):

    @http.route('/api/orders', type='json', auth='user', methods=['POST'])
    def create_order(self, **kwargs):
        order_service = request.env['order_management.order_service']
        order = order_service.create_order(kwargs)
        return {'status': 'success', 'data': order.read()} if order else {'status': 'error', 'message': 'Failed to create order'}

    @http.route('/api/orders/<string:uuid>', type='json', auth='user', methods=['GET'])
    def get_order(self, uuid):
        order_service = request.env['order_management.order_service']
        order = order_service.read_order(uuid)
        return {'status': 'success', 'data': order} if order else {'status': 'error', 'message': 'Order not found'}

    @http.route('/api/orders/<string:uuid>', type='json', auth='user', methods=['PUT'])
    def update_order(self, uuid, **kwargs):
        order_service = request.env['order_management.order_service']
        order = order_service.update_order(uuid, kwargs)
        return {'status': 'success', 'data': order} if order else {'status': 'error', 'message': 'Order not found or update failed'}

    @http.route('/api/orders/<string:uuid>', type='json', auth='user', methods=['DELETE'])
    def delete_order(self, uuid):
        order_service = request.env['order_management.order_service']
        success = order_service.delete_order(uuid)
        return {'status': 'success'} if success else {'status': 'error', 'message': 'Order not found or delete failed'}
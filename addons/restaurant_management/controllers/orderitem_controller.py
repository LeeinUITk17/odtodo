from odoo import http
from odoo.http import request

class OrderItemController(http.Controller):

    @http.route('/api/orderitems', type='json', auth='user', methods=['POST'])
    def create_orderitem(self, **kwargs):
        orderitem_service = request.env['restaurant_management.orderitem_service']
        orderitem = orderitem_service.create_orderitem(kwargs)
        return {'status': 'success', 'data': orderitem.read()} if orderitem else {'status': 'error', 'message': 'Failed to create order item'}

    @http.route('/api/orderitems/<string:uuid>', type='json', auth='user', methods=['GET'])
    def get_orderitem(self, uuid):
        orderitem_service = request.env['restaurant_management.orderitem_service']
        orderitem = orderitem_service.read_orderitem(uuid)
        return {'status': 'success', 'data': orderitem} if orderitem else {'status': 'error', 'message': 'Order item not found'}

    @http.route('/api/orderitems/<string:uuid>', type='json', auth='user', methods=['PUT'])
    def update_orderitem(self, uuid, **kwargs):
        orderitem_service = request.env['restaurant_management.orderitem_service']
        orderitem = orderitem_service.update_orderitem(uuid, kwargs)
        return {'status': 'success', 'data': orderitem} if orderitem else {'status': 'error', 'message': 'Order item not found or update failed'}

    @http.route('/api/orderitems/<string:uuid>', type='json', auth='user', methods=['DELETE'])
    def delete_orderitem(self, uuid):
        orderitem_service = request.env['restaurant_management.orderitem_service']
        success = orderitem_service.delete_orderitem(uuid)
        return {'status': 'success'} if success else {'status': 'error', 'message': 'Order item not found or delete failed'}
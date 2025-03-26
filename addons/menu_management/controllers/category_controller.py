from odoo import http
from odoo.http import request

class CategoryController(http.Controller):

    @http.route('/api/categories', type='json', auth='user', methods=['POST'])
    def create_category(self, **kwargs):
        category_service = request.env['menu_management.category_service']
        category = category_service.create_category(kwargs)
        return {'status': 'success', 'data': category.read()} if category else {'status': 'error', 'message': 'Failed to create category'}

    @http.route('/api/categories/<string:uuid>', type='json', auth='user', methods=['GET'])
    def get_category(self, uuid):
        category_service = request.env['menu_management.category_service']
        category = category_service.read_category(uuid)
        return {'status': 'success', 'data': category} if category else {'status': 'error', 'message': 'Category not found'}

    @http.route('/api/categories/<string:uuid>', type='json', auth='user', methods=['PUT'])
    def update_category(self, uuid, **kwargs):
        category_service = request.env['menu_management.category_service']
        category = category_service.update_category(uuid, kwargs)
        return {'status': 'success', 'data': category} if category else {'status': 'error', 'message': 'Category not found or update failed'}

    @http.route('/api/categories/<string:uuid>', type='json', auth='user', methods=['DELETE'])
    def delete_category(self, uuid):
        category_service = request.env['menu_management.category_service']
        success = category_service.delete_category(uuid)
        return {'status': 'success'} if success else {'status': 'error', 'message': 'Category not found or delete failed'}
from odoo import http
from odoo.http import request

class BranchController(http.Controller):

    @http.route('/api/branches', type='json', auth='public', methods=['POST'])
    def create_branch(self, **post):
        branch_service = request.env['restaurant_management.branch_service']
        branch = branch_service.create_branch(post)
        return {'status': 'success', 'data': branch.read()} if branch else {'status': 'error', 'message': 'Failed to create branch'}
    
    @http.route('/api/branches', type='json', auth='public', methods=['GET'])
    def get_branches(self):
        branch_service = request.env['restaurant_management.branch_service']
        branches = branch_service.get_branches()
        return {'status': 'success', 'data': branches} if branches else {'status': 'error', 'message': 'No branches found'}
    
    @http.route('/api/branches/<string:uuid>', type='json', auth='public', methods=['GET'])
    def get_branch(self, uuid):
        branch_service = request.env['restaurant_management.branch_service']
        branch = branch_service.get_branch(uuid)
        return {'status': 'success', 'data': branch} if branch else {'status': 'error', 'message': 'Branch not found'}

    @http.route('/api/branches/<string:uuid>', type='json', auth='public', methods=['PUT'])
    def update_branch(self, uuid, **post):
        branch_service = request.env['restaurant_management.branch_service']
        branch = branch_service.update_branch(uuid, post)
        return {'status': 'success', 'data': branch} if branch else {'status': 'error', 'message': 'Branch not found or update failed'}

    @http.route('/api/branches/<string:uuid>', type='json', auth='public', methods=['DELETE'])
    def delete_branch(self, uuid):
        branch_service = request.env['restaurant_management.branch_service']
        success = branch_service.delete_branch(uuid)
        return {'status': 'success'} if success else {'status': 'error', 'message': 'Branch not found or delete failed'}
    
from odoo import http
from odoo.http import request, Response

class BranchController(http.Controller):

    @http.route('/api/branches', type='json', auth='public', methods=['POST'])
    def create_branch(self, **post):
        branch = request.env['restaurant_management.branch.service'].create_branch(post)
        return {'status': 'success', 'data': branch.read()} if branch else {'status': 'error'}

    @http.route('/api/branches/<int:branch_id>', type='json', auth='public', methods=['GET'])
    def get_branch(self, branch_id):
        branch = request.env['restaurant_management.branch.service'].get_branch(branch_id)
        return {'status': 'success', 'data': branch} if branch else {'status': 'error', 'message': 'Branch not found'}

    @http.route('/api/branches/<int:branch_id>', type='json', auth='public', methods=['PUT'])
    def update_branch(self, branch_id, **post):
        branch = request.env['restaurant_management.branch.service'].update_branch(branch_id, post)
        return {'status': 'success', 'data': branch} if branch else {'status': 'error', 'message': 'Branch not found'}

    @http.route('/api/branches/<int:branch_id>', type='json', auth='public', methods=['DELETE'])
    def delete_branch(self, branch_id):
        success = request.env['restaurant_management.branch.service'].delete_branch(branch_id)
        return {'status': 'success'} if success else {'status': 'error', 'message': 'Branch not found'}

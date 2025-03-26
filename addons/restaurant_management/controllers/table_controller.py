from odoo import http
from odoo.http import request

class TableController(http.Controller):

    @http.route('/tables', type='json', auth='user')
    def list_tables(self):
        tables = request.env['restaurant_management.table'].search([])
        return tables.read()

    @http.route('/tables/<string:uuid>', type='json', auth='user')
    def get_table(self, uuid):
        table_service = request.env['restaurant_management.table_service']
        table = table_service.read_table(uuid)
        return {'status': 'success', 'data': table} if table else {'status': 'error', 'message': 'Table not found'}

    @http.route('/tables', type='json', auth='user', methods=['POST'])
    def create_table(self, **kwargs):
        table_service = request.env['restaurant_management.table_service']
        table = table_service.create_table(kwargs)
        return {'status': 'success', 'data': table.read()} if table else {'status': 'error', 'message': 'Failed to create table'}

    @http.route('/tables/<string:uuid>', type='json', auth='user', methods=['PUT'])
    def update_table(self, uuid, **kwargs):
        table_service = request.env['restaurant_management.table_service']
        table = table_service.update_table(uuid, kwargs)
        return {'status': 'success', 'data': table} if table else {'status': 'error', 'message': 'Table not found or update failed'}

    @http.route('/tables/<string:uuid>', type='json', auth='user', methods=['DELETE'])
    def delete_table(self, uuid):
        table_service = request.env['restaurant_management.table_service']
        success = table_service.delete_table(uuid)
        return {'status': 'success'} if success else {'status': 'error', 'message': 'Table not found or delete failed'}
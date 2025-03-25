from odoo import http
from odoo.http import request

class TableController(http.Controller):

    @http.route('/tables', type='json', auth='user')
    def list_tables(self):
        tables = request.env['restaurant_management.table'].search([])
        return tables.read()

    @http.route('/tables/<int:table_id>', type='json', auth='user')
    def get_table(self, table_id):
        table = request.env['restaurant_management.table'].browse(table_id)
        return table.read()

    @http.route('/tables', type='json', auth='user', methods=['POST'])
    def create_table(self, **kwargs):
        table_service = request.env['restaurant_management.table_service']
        table = table_service.create_table(kwargs)
        return table.read()

    @http.route('/tables/<int:table_id>', type='json', auth='user', methods=['PUT'])
    def update_table(self, table_id, **kwargs):
        table_service = request.env['restaurant_management.table_service']
        table = table_service.update_table(table_id, kwargs)
        return table.read()

    @http.route('/tables/<int:table_id>', type='json', auth='user', methods=['DELETE'])
    def delete_table(self, table_id):
        table_service = request.env['restaurant_management.table_service']
        table_service.delete_table(table_id)
        return {'status': 'success'}
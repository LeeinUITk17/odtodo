from odoo import http
from odoo.http import request

class MenuItemController(http.Controller):

    @http.route('/api/menuitems', type='json', auth='user', methods=['POST'])
    def create_menuitem(self, **kwargs):
        menuitem_service = request.env['restaurant_management.menuitem_service']
        menuitem = menuitem_service.create_menuitem(kwargs)
        return {'status': 'success', 'data': menuitem.read()} if menuitem else {'status': 'error', 'message': 'Failed to create menu item'}

    @http.route('/api/menuitems/<string:uuid>', type='json', auth='user', methods=['GET'])
    def get_menuitem(self, uuid):
        menuitem_service = request.env['restaurant_management.menuitem_service']
        menuitem = menuitem_service.read_menuitem(uuid)
        return {'status': 'success', 'data': menuitem} if menuitem else {'status': 'error', 'message': 'Menu item not found'}

    @http.route('/api/menuitems/<string:uuid>', type='json', auth='user', methods=['PUT'])
    def update_menuitem(self, uuid, **kwargs):
        menuitem_service = request.env['restaurant_management.menuitem_service']
        menuitem = menuitem_service.update_menuitem(uuid, kwargs)
        return {'status': 'success', 'data': menuitem} if menuitem else {'status': 'error', 'message': 'Menu item not found or update failed'}

    @http.route('/api/menuitems/<string:uuid>', type='json', auth='user', methods=['DELETE'])
    def delete_menuitem(self, uuid):
        menuitem_service = request.env['restaurant_management.menuitem_service']
        success = menuitem_service.delete_menuitem(uuid)
        return {'status': 'success'} if success else {'status': 'error', 'message': 'Menu item not found or delete failed'}
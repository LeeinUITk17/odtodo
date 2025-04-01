from odoo import models, api

class MenuItemService(models.AbstractModel):
    _name = 'restaurant_management.menuitem_service'
    _description = 'Menu Item Service'

    @api.model
    def create_menuitem(self, vals):
        return self.env['restaurant_management.menuitem'].create(vals)

    @api.model
    def read_menuitem(self, uuid):
        menuitem = self.env['restaurant_management.menuitem'].search([('uuid', '=', uuid)], limit=1)
        if menuitem:
            return menuitem.read()
        return False

    @api.model
    def update_menuitem(self, uuid, vals):
        menuitem = self.env['restaurant_management.menuitem'].search([('uuid', '=', uuid)], limit=1)
        if menuitem:
            menuitem.write(vals)
            return menuitem.read()
        return False

    @api.model
    def delete_menuitem(self, uuid):
        menuitem = self.env['restaurant_management.menuitem'].search([('uuid', '=', uuid)], limit=1)
        if menuitem:
            menuitem.unlink()
            return True
        return False
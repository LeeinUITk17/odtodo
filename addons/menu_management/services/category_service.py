from odoo import models, api

class CategoryService(models.AbstractModel):
    _name = 'menu_management.category_service'
    _description = 'Category Service'

    @api.model
    def create_category(self, vals):
        return self.env['menu_management.category'].create(vals)

    @api.model
    def read_category(self, uuid):
        category = self.env['menu_management.category'].search([('uuid', '=', uuid)], limit=1)
        if category:
            return category.read()
        return False

    @api.model
    def update_category(self, uuid, vals):
        category = self.env['menu_management.category'].search([('uuid', '=', uuid)], limit=1)
        if category:
            category.write(vals)
            return category.read()
        return False

    @api.model
    def delete_category(self, uuid):
        category = self.env['menu_management.category'].search([('uuid', '=', uuid)], limit=1)
        if category:
            category.unlink()
            return True
        return False
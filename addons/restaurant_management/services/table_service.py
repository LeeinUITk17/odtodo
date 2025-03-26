from odoo import models, api

class TableService(models.AbstractModel):
    _name = 'restaurant_management.table_service'
    _description = 'Table Service'

    @api.model
    def create_table(self, vals):
        return self.env['restaurant_management.table'].create(vals)

    @api.model
    def read_table(self, uuid):
        table = self.env['restaurant_management.table'].search([('uuid', '=', uuid)], limit=1)
        if table:
            return table.read()
        return False

    @api.model
    def update_table(self, uuid, vals):
        table = self.env['restaurant_management.table'].search([('uuid', '=', uuid)], limit=1)
        if table:
            table.write(vals)
            return table.read()
        return False

    @api.model
    def delete_table(self, uuid):
        table = self.env['restaurant_management.table'].search([('uuid', '=', uuid)], limit=1)
        if table:
            table.unlink()
            return True
        return False
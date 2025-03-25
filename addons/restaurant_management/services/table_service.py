from odoo import models, api

class TableService(models.AbstractModel):
    _name = 'restaurant_management.table_service'
    _description = 'Table Service'

    @api.model
    def create_table(self, vals):
        return self.env['restaurant_management.table'].create(vals)

    @api.model
    def read_table(self, table_id):
        return self.env['restaurant_management.table'].browse(table_id).read()

    @api.model
    def update_table(self, table_id, vals):
        table = self.env['restaurant_management.table'].browse(table_id)
        table.write(vals)
        return table

    @api.model
    def delete_table(self, table_id):
        table = self.env['restaurant_management.table'].browse(table_id)
        table.unlink()
        return True
from odoo import api, models

class BranchService(models.AbstractModel):
    _name = 'restaurant_management.branch_service'
    _description = 'Branch Service'

    @api.model
    def create_branch(self, vals):
        return self.env['restaurant_management.branch'].create(vals)

    @api.model
    def get_branch(self, uuid):
        branch = self.env['restaurant_management.branch'].search([('uuid', '=', uuid)], limit=1)
        if branch:
            return branch.read()
        return False

    @api.model
    def update_branch(self, uuid, vals):
        branch = self.env['restaurant_management.branch'].search([('uuid', '=', uuid)], limit=1)
        if branch:
            branch.write(vals)
            return branch.read()
        return False

    @api.model
    def delete_branch(self, uuid):
        branch = self.env['restaurant_management.branch'].search([('uuid', '=', uuid)], limit=1)
        if branch:
            branch.unlink()
            return True
        return False
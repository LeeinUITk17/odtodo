from odoo import api, models

class BranchService(models.AbstractModel):
    _name = 'restaurant_management.branch.service'
    _description = 'Branch Service'

    @api.model
    def create_branch(self, vals):
        return self.env['restaurant_management.branch'].create(vals)

    @api.model
    def get_branch(self, branch_id):
        return self.env['restaurant_management.branch'].browse(branch_id).read()

    @api.model
    def update_branch(self, branch_id, vals):
        branch = self.env['restaurant_management.branch'].browse(branch_id)
        if branch.exists():
            branch.write(vals)
            return branch.read()
        return False

    @api.model
    def delete_branch(self, branch_id):
        branch = self.env['restaurant_management.branch'].browse(branch_id)
        if branch.exists():
            branch.unlink()
            return True
        return False

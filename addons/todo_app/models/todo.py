from odoo import models, fields

class Todo(models.Model):
    _name = 'todo.todo'
    _description = 'Todo Task'

    name = fields.Char(string='Task Name', required=True)
    description = fields.Text(string='Description')
    is_done = fields.Boolean(string='Done', default=False)

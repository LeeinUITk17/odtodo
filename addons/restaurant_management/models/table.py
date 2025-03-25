from odoo import models, fields, api

class Table(models.Model):
    _name = "restaurant_management.table"
    _description = "Restaurant Table"

    name = fields.Char(string="Table Name", required=True)
    area = fields.Selection([
        ('indoor', 'Indoor'),
        ('outdoor', 'Outdoor')
    ], string="Table Area", required=True)
    floor = fields.Char(string="Floor")
    capacity = fields.Integer(string="Capacity", required=True)
    status = fields.Selection([
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved')
    ], string="Status", default='available')
    
    branch_id = fields.Many2one('restaurant_management.branch', string="Branch", required=True, ondelete='cascade')
    order_ids = fields.One2many('order_management.order', 'table_id', string="Orders")
from odoo import models, fields, api, _
import uuid
import logging

_logger = logging.getLogger(__name__) 

class CustomerLog(models.Model):
    _name = 'restaurant_management.customer.log'
    _description = 'Customer Activity Log'
    _order = 'create_date desc'

    uuid = fields.Char(string="Log UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True, index=True)
    customer_id = fields.Many2one(
        'restaurant_management.customer',
        string='Customer',
        required=True,
        ondelete='cascade',
        index=True
    )
    log_type = fields.Selection([
        ('reservation_created', 'Reservation Created'),
        ('reservation_confirmed', 'Reservation Confirmed'),
        ('reservation_cancelled', 'Reservation Cancelled'),
        ('payment_paid', 'Invoice Paid'),
        ('payment_cancelled', 'Invoice Cancelled'),
        ('other', 'Other')
    ], string='Log Type', required=True, index=True)
    content = fields.Text(string='Details', required=True)
    reservation_id = fields.Many2one('restaurant_management.reservation', string='Related Reservation', readonly=True)
    invoice_id = fields.Many2one('restaurant_management.invoice', string='Related Invoice', readonly=True)
    order_id = fields.Many2one(related='invoice_id.order_uuid', string='Related Order', store=True, readonly=True)
    user_id = fields.Many2one('res.users', string='Performed By', default=lambda self: self.env.user, readonly=True)
    branch_id = fields.Many2one('restaurant_management.branch', string='Branch', readonly=True)

    @api.model
    def _create_log(self, customer, log_type, content, reservation=None, invoice=None, branch=None):
        if not customer:
            return False

        log_vals = {
            'customer_id': customer.id,
            'log_type': log_type,
            'content': content,
            'reservation_id': reservation.id if reservation else False,
            'invoice_id': invoice.id if invoice else False,
            'branch_id': branch.id if branch else (reservation.branch_uuid.id if reservation else (invoice.order_uuid.branch_uuid.id if invoice and invoice.order_uuid else False)),
        }
        try:
            return self.env['restaurant_management.customer.log'].sudo().create(log_vals)
        except Exception as e:
            _logger.error(f"Failed to create customer log: {e}", exc_info=True)
            return False



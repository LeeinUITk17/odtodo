from odoo import models, fields, api, _
from odoo.exceptions import UserError
import uuid

class Invoice(models.Model):
    _name = "restaurant_management.invoice"
    _description = "Invoice"
    _order = "created_at desc"

    order_uuid = fields.Many2one(
        "restaurant_management.order", string="Select Order",
        ondelete="restrict", index=True,
        domain="[('status', '=', 'COMPLETED'), ('invoice_count', '=', 0)]"
    )
    customer_uuid = fields.Many2one(
        "restaurant_management.customer", string="Customer (Name or Phone)",
        ondelete='restrict', index=True,
        help="Search by Name or Phone. Create new if not found."
    )
    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True, index=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id', store=True, string="Currency", readonly=True)
    total_price = fields.Monetary(string="Subtotal", compute='_compute_total_amounts', store=True, currency_field='currency_id')
    tax = fields.Monetary(string="Tax (10%)", compute='_compute_total_amounts', store=True, currency_field='currency_id', readonly=True)
    grand_total = fields.Monetary(string="Grand Total", compute='_compute_total_amounts', store=True, currency_field='currency_id')
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('online_payment', 'Online Payment')
    ], string="Payment Method")
    status = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ], string="Invoice Status", default="draft", required=True, index=True)
    created_at = fields.Datetime(string="Created At", default=fields.Datetime.now, readonly=True)
    updated_at = fields.Datetime(string="Updated At", default=fields.Datetime.now, readonly=True)
    coupon_uuid = fields.Char(string="Coupon Code")
    promotion_uuid = fields.Char(string="Promotion Applied")
    details = fields.One2many("restaurant_management.invoicedetail", "invoice_uuid", string="Invoice Details")

    @api.onchange('order_uuid')
    def _onchange_order_uuid(self):
        if not self.order_uuid:
            self.details = [(5, 0, 0)]
            self.customer_uuid = False
            self.tax = 0.0
            return {'domain': {'customer_uuid': []}}

        if hasattr(self.order_uuid, 'customer_uuid') and self.order_uuid.customer_uuid:
            self.customer_uuid = self.order_uuid.customer_uuid
        else:
            self.customer_uuid = False

        new_details = []
        for item in self.order_uuid.order_items:
            new_details.append((0, 0, {
                'product_uuid': item.menu_item_uuid.id,
                'quantity': item.quantity,
                'price': item.unitPrice,
            }))
        self.details = [(5, 0, 0)] + new_details

    @api.depends('details.amount')
    def _compute_total_amounts(self):
        for invoice in self:
            subtotal = sum(detail.amount for detail in invoice.details)
            calculated_tax = subtotal * 0.10
            invoice.total_price = subtotal
            invoice.tax = calculated_tax
            invoice.grand_total = subtotal + calculated_tax
    def write(self, vals):
        old_statuses = {rec.id: rec.status for rec in self}
        res = super(Invoice, self).write(vals)
        if 'status' in vals:
            for invoice in self:
                 # Chỉ tạo log nếu status thực sự thay đổi và có customer
                if invoice.customer_uuid and vals['status'] != old_statuses.get(invoice.id):
                    log_type = False
                    content = False
                    # Khi chuyển sang Paid
                    if vals['status'] == 'paid' and old_statuses.get(invoice.id) != 'paid':
                        log_type = 'payment_paid'
                        content = _("Invoice marked as Paid. Amount: %s %s.") % (
                            invoice.grand_total,
                            invoice.currency_id.symbol or invoice.currency_id.name
                        )
                    # Khi chuyển sang Cancelled (từ trạng thái không phải cancelled)
                    elif vals['status'] == 'cancelled' and old_statuses.get(invoice.id) != 'cancelled':
                        log_type = 'payment_cancelled'
                        content = _("Invoice Cancelled.")

                    if log_type and content:
                        self.env['restaurant_management.customer.log']._create_log(
                            customer=invoice.customer_uuid,
                            log_type=log_type,
                            content=content,
                            invoice=invoice,
                            branch=invoice.order_uuid.branch_uuid if invoice.order_uuid else None # Lấy branch qua order
                        )
            vals['updated_at'] = fields.Datetime.now()
        return res

    def action_post(self):
        if not self.details:
            raise UserError(_("Cannot post an invoice with no lines."))
        if not self.customer_uuid:
            raise UserError(_("Please select or create a customer before posting."))
        self.write({'status': 'posted'})
        return True

    def action_pay(self):
        if self.status != 'posted':
            raise UserError(_("Only posted invoices can be marked as paid."))
        self.write({'status': 'paid'})
        return True

    def action_cancel(self):
        if self.status == 'paid':
            raise UserError(_("Cannot cancel a paid invoice."))
        self.write({'status': 'cancelled'})
        return True

    def action_draft(self):
        self.write({'status': 'draft'})
        return True

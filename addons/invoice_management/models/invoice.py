# -*- coding: utf-8 -*-
from odoo import models, fields, api # Added api import
import uuid

class Invoice(models.Model):
    _name = "invoice_management.invoice"
    _description = "Invoice"
    _order = "created_at desc" # Add default order

    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), required=True, copy=False, readonly=True, index=True) # Added index

    # Dependencies: order_management, restaurant_management
    order_uuid = fields.Many2one("restaurant_management.order", string="Order", required=True, ondelete="restrict", index=True) # Changed ondelete to restrict for safety, added index
    customer_uuid = fields.Many2one("restaurant_management.customer", string="Customer", ondelete="set null", index=True) # Added index

    # Consider making total_price computed if details drive the price
    total_price = fields.Float(string="Total Price", compute='_compute_total_amounts', store=True) # Changed to compute
    total_price_manual = fields.Float(string="Total Price (Manual)") # Add manual field if needed override compute
    tax = fields.Float(string="Tax", compute='_compute_total_amounts', store=True) # Changed to compute if driven by details/config
    tax_manual = fields.Float(string="Tax (Manual)") # Add manual field if needed override compute

    # Grand total including tax
    grand_total = fields.Float(string="Grand Total", compute='_compute_total_amounts', store=True)

    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('online_payment', 'Online Payment')
        # Add more as needed
    ], string="Payment Method") # Making it not required, maybe set later? Or keep required if always known at creation
    status = fields.Selection([
        ('draft', 'Draft'), # Added Draft state
        ('posted', 'Posted'), # Renamed pending to posted/open?
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ], string="Invoice Status", default="draft", required=True, index=True) # Changed default to draft, added index

    created_at = fields.Datetime(string="Created At", default=fields.Datetime.now, readonly=True)
    updated_at = fields.Datetime(string="Updated At", default=fields.Datetime.now, readonly=True) # Added default, readonly

    # Consider using Many2one if Coupon/Promotion are models
    coupon_uuid = fields.Char(string="Coupon Code") # Renamed field
    promotion_uuid = fields.Char(string="Promotion Applied") # Renamed field

    details = fields.One2many("invoice_management.invoicedetail", "invoice_uuid", string="Invoice Details")
    # REMOVED //

    @api.depends('details.amount', 'tax_manual') # Add other tax sources if they exist
    def _compute_total_amounts(self):
        for invoice in self:
            subtotal = sum(detail.amount for detail in invoice.details)
            # Basic tax calculation (replace with your logic if complex)
            # If tax is manually set, use that, otherwise calculate if needed
            calculated_tax = invoice.tax_manual # Or calculate based on lines/products/config
            calculated_total = subtotal + calculated_tax

            invoice.total_price = subtotal # Typically total_price means pre-tax
            invoice.tax = calculated_tax
            invoice.grand_total = calculated_total
            # If you need to allow manual override for total_price too:
            # invoice.total_price = invoice.total_price_manual or subtotal

    # Override write to update 'updated_at'
    def write(self, vals):
        if 'updated_at' not in vals:
             vals['updated_at'] = fields.Datetime.now()
        return super(Invoice, self).write(vals)

    # Add methods for state transitions (post, pay, cancel)
    def action_post(self):
        self.write({'status': 'posted'})

    def action_pay(self):
        # Add logic here to register payment if needed
        self.write({'status': 'paid'})

    def action_cancel(self):
        self.write({'status': 'cancelled'})

    def action_draft(self):
        self.write({'status': 'draft'})
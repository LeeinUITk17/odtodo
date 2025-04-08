# -*- coding: utf-8 -*-
from odoo import models, api # Added api import

class InvoiceService(models.AbstractModel):
    _name = 'invoice_management.invoice_service'
    _description = 'Invoice Service Layer' # Updated description

    @api.model
    def create_invoice(self, vals):
        # Add validation or preprocessing if needed
        return self.env['invoice_management.invoice'].create(vals)

    @api.model
    def search_invoice_by_uuid(self, uuid):
         # Use search directly, returns recordset or empty
         return self.env['invoice_management.invoice'].search([('uuid', '=', uuid)], limit=1)

    @api.model
    def read_invoice(self, uuid):
        invoice = self.search_invoice_by_uuid(uuid)
        # read() returns a list of dicts, get first element if exists
        return invoice.read()[0] if invoice else False

    @api.model
    def update_invoice(self, uuid, vals):
        invoice = self.search_invoice_by_uuid(uuid)
        if invoice:
            # Add validation or preprocessing if needed
            invoice.write(vals)
            return invoice.read()[0] # Return updated data
        return False

    @api.model
    def delete_invoice(self, uuid):
        invoice = self.search_invoice_by_uuid(uuid)
        if invoice:
            invoice.unlink()
            return True
        return False
# REMOVED //
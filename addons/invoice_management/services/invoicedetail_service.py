# -*- coding: utf-8 -*-
from odoo import models, api # Added api import

class InvoiceDetailService(models.AbstractModel):
    _name = 'invoice_management.invoicedetail_service'
    _description = 'Invoice Detail Service Layer' # Updated description

    @api.model
    def create_invoicedetail(self, vals):
        # Add validation or preprocessing if needed
        return self.env['invoice_management.invoicedetail'].create(vals)

    @api.model
    def search_invoicedetail_by_uuid(self, uuid):
        # Use search directly, returns recordset or empty
        return self.env['invoice_management.invoicedetail'].search([('uuid', '=', uuid)], limit=1)

    @api.model
    def read_invoicedetail(self, uuid):
        invoicedetail = self.search_invoicedetail_by_uuid(uuid)
        # read() returns a list of dicts, get first element if exists
        return invoicedetail.read()[0] if invoicedetail else False

    @api.model
    def update_invoicedetail(self, uuid, vals):
        invoicedetail = self.search_invoicedetail_by_uuid(uuid)
        if invoicedetail:
            # Add validation or preprocessing if needed
            invoicedetail.write(vals)
            return invoicedetail.read()[0] # Return updated data
        return False

    @api.model
    def delete_invoicedetail(self, uuid):
        invoicedetail = self.search_invoicedetail_by_uuid(uuid)
        if invoicedetail:
            invoicedetail.unlink()
            return True
        return False
# REMOVED //
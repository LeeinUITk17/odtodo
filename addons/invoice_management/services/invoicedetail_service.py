from odoo import models, api

class InvoiceDetailService(models.AbstractModel):
    _name = 'invoice_management.invoicedetail_service'
    _description = 'Invoice Detail Service'

    @api.model
    def create_invoicedetail(self, vals):
        return self.env['invoice_management.invoicedetail'].create(vals)

    @api.model
    def read_invoicedetail(self, uuid):
        invoicedetail = self.env['invoice_management.invoicedetail'].search([('uuid', '=', uuid)], limit=1)
        if invoicedetail:
            return invoicedetail.read()
        return False

    @api.model
    def update_invoicedetail(self, uuid, vals):
        invoicedetail = self.env['invoice_management.invoicedetail'].search([('uuid', '=', uuid)], limit=1)
        if invoicedetail:
            invoicedetail.write(vals)
            return invoicedetail.read()
        return False

    @api.model
    def delete_invoicedetail(self, uuid):
        invoicedetail = self.env['invoice_management.invoicedetail'].search([('uuid', '=', uuid)], limit=1)
        if invoicedetail:
            invoicedetail.unlink()
            return True
        return False
from odoo import models, api

class InvoiceService(models.AbstractModel):
    _name = 'invoice_management.invoice_service'
    _description = 'Invoice Service'

    @api.model
    def create_invoice(self, vals):
        return self.env['invoice_management.invoice'].create(vals)

    @api.model
    def read_invoice(self, uuid):
        invoice = self.env['invoice_management.invoice'].search([('uuid', '=', uuid)], limit=1)
        if invoice:
            return invoice.read()
        return False

    @api.model
    def update_invoice(self, uuid, vals):
        invoice = self.env['invoice_management.invoice'].search([('uuid', '=', uuid)], limit=1)
        if invoice:
            invoice.write(vals)
            return invoice.read()
        return False

    @api.model
    def delete_invoice(self, uuid):
        invoice = self.env['invoice_management.invoice'].search([('uuid', '=', uuid)], limit=1)
        if invoice:
            invoice.unlink()
            return True
        return False
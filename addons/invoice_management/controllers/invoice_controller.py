from odoo import http
from odoo.http import request

class InvoiceController(http.Controller):

    @http.route('/api/invoices', type='json', auth='user', methods=['POST'])
    def create_invoice(self, **kwargs):
        invoice_service = request.env['invoice_management.invoice_service']
        invoice = invoice_service.create_invoice(kwargs)
        return {'status': 'success', 'data': invoice.read()} if invoice else {'status': 'error', 'message': 'Failed to create invoice'}

    @http.route('/api/invoices/<string:uuid>', type='json', auth='user', methods=['GET'])
    def get_invoice(self, uuid):
        invoice_service = request.env['invoice_management.invoice_service']
        invoice = invoice_service.read_invoice(uuid)
        return {'status': 'success', 'data': invoice} if invoice else {'status': 'error', 'message': 'Invoice not found'}

    @http.route('/api/invoices/<string:uuid>', type='json', auth='user', methods=['PUT'])
    def update_invoice(self, uuid, **kwargs):
        invoice_service = request.env['invoice_management.invoice_service']
        invoice = invoice_service.update_invoice(uuid, kwargs)
        return {'status': 'success', 'data': invoice} if invoice else {'status': 'error', 'message': 'Invoice not found or update failed'}

    @http.route('/api/invoices/<string:uuid>', type='json', auth='user', methods=['DELETE'])
    def delete_invoice(self, uuid):
        invoice_service = request.env['invoice_management.invoice_service']
        success = invoice_service.delete_invoice(uuid)
        return {'status': 'success'} if success else {'status': 'error', 'message': 'Invoice not found or delete failed'}
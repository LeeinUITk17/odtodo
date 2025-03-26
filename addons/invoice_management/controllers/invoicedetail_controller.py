from odoo import http
from odoo.http import request

class InvoiceDetailController(http.Controller):

    @http.route('/api/invoicedetails', type='json', auth='user', methods=['POST'])
    def create_invoicedetail(self, **kwargs):
        invoicedetail_service = request.env['invoice_management.invoicedetail_service']
        invoicedetail = invoicedetail_service.create_invoicedetail(kwargs)
        return {'status': 'success', 'data': invoicedetail.read()} if invoicedetail else {'status': 'error', 'message': 'Failed to create invoice detail'}

    @http.route('/api/invoicedetails/<string:uuid>', type='json', auth='user', methods=['GET'])
    def get_invoicedetail(self, uuid):
        invoicedetail_service = request.env['invoice_management.invoicedetail_service']
        invoicedetail = invoicedetail_service.read_invoicedetail(uuid)
        return {'status': 'success', 'data': invoicedetail} if invoicedetail else {'status': 'error', 'message': 'Invoice detail not found'}

    @http.route('/api/invoicedetails/<string:uuid>', type='json', auth='user', methods=['PUT'])
    def update_invoicedetail(self, uuid, **kwargs):
        invoicedetail_service = request.env['invoice_management.invoicedetail_service']
        invoicedetail = invoicedetail_service.update_invoicedetail(uuid, kwargs)
        return {'status': 'success', 'data': invoicedetail} if invoicedetail else {'status': 'error', 'message': 'Invoice detail not found or update failed'}

    @http.route('/api/invoicedetails/<string:uuid>', type='json', auth='user', methods=['DELETE'])
    def delete_invoicedetail(self, uuid):
        invoicedetail_service = request.env['invoice_management.invoicedetail_service']
        success = invoicedetail_service.delete_invoicedetail(uuid)
        return {'status': 'success'} if success else {'status': 'error', 'message': 'Invoice detail not found or delete failed'}
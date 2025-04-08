# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

class InvoiceDetailController(http.Controller):

    # Reusing helper from InvoiceController or define locally
    def _json_response(self, success=True, data=None, message=None, status_code=200):
        # ... (same implementation as above) ...
        body = {'status': 'success' if success else 'error'}
        if data is not None:
            body['data'] = data
        if message is not None:
            body['message'] = message
        return body

    @http.route('/api/invoicedetails', type='json', auth='user', methods=['POST'], csrf=False)
    def create_invoicedetail(self, **kwargs):
        try:
            # Add validation, e.g., check if invoice_uuid exists
            if 'invoice_uuid' in kwargs:
                invoice = request.env['invoice_management.invoice'].search([('uuid', '=', kwargs['invoice_uuid'])], limit=1)
                if not invoice:
                    return self._json_response(success=False, message="Parent invoice not found", status_code=404)

            invoicedetail_service = request.env['invoice_management.invoicedetail_service']
            detail_record = invoicedetail_service.create_invoicedetail(kwargs)
            data = detail_record.read(['uuid', 'product_uuid', 'quantity', 'amount'])[0]
            return self._json_response(data=data, status_code=201)
        except Exception as e:
            request.env.cr.rollback()
            return self._json_response(success=False, message=f"Failed to create invoice detail: {str(e)}", status_code=500)


    @http.route('/api/invoicedetails/<string:uuid>', type='json', auth='user', methods=['GET'], csrf=False)
    def get_invoicedetail(self, uuid):
        try:
            invoicedetail_service = request.env['invoice_management.invoicedetail_service']
            detail_record = invoicedetail_service.search_invoicedetail_by_uuid(uuid)
            if not detail_record:
                 return self._json_response(success=False, message='Invoice detail not found', status_code=404)
            data = detail_record.read(['uuid', 'invoice_uuid', 'product_uuid', 'quantity', 'price', 'discount_amount', 'amount'])[0]
            return self._json_response(data=data)
        except Exception as e:
            return self._json_response(success=False, message=f"Failed to retrieve invoice detail: {str(e)}", status_code=500)


    @http.route('/api/invoicedetails/<string:uuid>', type='json', auth='user', methods=['PUT'], csrf=False)
    def update_invoicedetail(self, uuid, **kwargs):
        try:
            invoicedetail_service = request.env['invoice_management.invoicedetail_service']
            detail_record = invoicedetail_service.search_invoicedetail_by_uuid(uuid)
            if not detail_record:
                 return self._json_response(success=False, message='Invoice detail not found', status_code=404)

            updated_data = invoicedetail_service.update_invoicedetail(uuid, kwargs)
            return self._json_response(data=updated_data)
        except Exception as e:
            request.env.cr.rollback()
            return self._json_response(success=False, message=f"Failed to update invoice detail: {str(e)}", status_code=500)


    @http.route('/api/invoicedetails/<string:uuid>', type='json', auth='user', methods=['DELETE'], csrf=False)
    def delete_invoicedetail(self, uuid):
        try:
            invoicedetail_service = request.env['invoice_management.invoicedetail_service']
            detail_record = invoicedetail_service.search_invoicedetail_by_uuid(uuid)
            if not detail_record:
                 return self._json_response(success=False, message='Invoice detail not found', status_code=404)

            success = invoicedetail_service.delete_invoicedetail(uuid)
            if success:
                return self._json_response(message='Invoice detail deleted successfully')
            else:
                return self._json_response(success=False, message='Invoice detail deletion failed', status_code=500)
        except Exception as e:
            request.env.cr.rollback()
            return self._json_response(success=False, message=f"Failed to delete invoice detail: {str(e)}", status_code=500)
# REMOVED //
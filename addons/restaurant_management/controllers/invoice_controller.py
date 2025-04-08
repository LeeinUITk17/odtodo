# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json # Import json for potential manual handling if needed

class InvoiceController(http.Controller):

    # Helper to return JSON response
    def _json_response(self, success=True, data=None, message=None, status_code=200):
        body = {'status': 'success' if success else 'error'}
        if data is not None:
            body['data'] = data
        if message is not None:
            body['message'] = message
        # Note: type='json' handles response wrapping, but setting status code requires Response object
        # For simplicity with type='json', we rely on the dictionary structure for now.
        return body

    @http.route('/api/invoices', type='json', auth='user', methods=['POST'], csrf=False) # Added csrf=False for non-browser clients
    def create_invoice(self, **kwargs):
        try:
            # Basic validation: Ensure required fields for invoice model are present?
            # e.g., if order_uuid is needed:
            # if 'order_uuid' not in kwargs:
            #    return self._json_response(success=False, message="Missing 'order_uuid'", status_code=400)

            invoice_service = request.env['invoice_management.invoice_service']
            # The service create method returns the recordset
            invoice_record = invoice_service.create_invoice(kwargs)
            # Read the specific fields you want to return
            data = invoice_record.read(['uuid', 'status', 'grand_total'])[0] # Example fields
            return self._json_response(data=data, status_code=201) # 201 Created
        except Exception as e:
            # Log the exception e
            request.env.cr.rollback() # Rollback transaction on error
            return self._json_response(success=False, message=f"Failed to create invoice: {str(e)}", status_code=500)

    @http.route('/api/invoices/<string:uuid>', type='json', auth='user', methods=['GET'], csrf=False)
    def get_invoice(self, uuid):
        try:
            invoice_service = request.env['invoice_management.invoice_service']
            # Use search directly for potentially better error handling/checking
            invoice_record = invoice_service.search_invoice_by_uuid(uuid)
            if not invoice_record:
                 return self._json_response(success=False, message='Invoice not found', status_code=404) # 404 Not Found
            # Read specific fields, include details maybe?
            data = invoice_record.read(['uuid', 'status', 'grand_total', 'customer_uuid', 'order_uuid', 'details'])[0] # Example fields
            # If details are included, read their relevant fields too
            if data.get('details'):
                 detail_ids = data['details']
                 detail_data = request.env['invoice_management.invoicedetail'].browse(detail_ids).read(['uuid', 'product_uuid', 'quantity', 'amount'])
                 data['details'] = detail_data # Replace IDs with data
            return self._json_response(data=data)
        except Exception as e:
            # Log the exception e
            return self._json_response(success=False, message=f"Failed to retrieve invoice: {str(e)}", status_code=500)


    @http.route('/api/invoices/<string:uuid>', type='json', auth='user', methods=['PUT'], csrf=False)
    def update_invoice(self, uuid, **kwargs):
        try:
            invoice_service = request.env['invoice_management.invoice_service']
            # Search first to ensure it exists before calling update service
            invoice_record = invoice_service.search_invoice_by_uuid(uuid)
            if not invoice_record:
                 return self._json_response(success=False, message='Invoice not found', status_code=404)

            # The update service returns the read() data directly in this implementation
            updated_data = invoice_service.update_invoice(uuid, kwargs)
            return self._json_response(data=updated_data)
        except Exception as e:
            # Log the exception e
            request.env.cr.rollback()
            return self._json_response(success=False, message=f"Failed to update invoice: {str(e)}", status_code=500)


    @http.route('/api/invoices/<string:uuid>', type='json', auth='user', methods=['DELETE'], csrf=False)
    def delete_invoice(self, uuid):
        try:
            invoice_service = request.env['invoice_management.invoice_service']
            # Search first to ensure it exists
            invoice_record = invoice_service.search_invoice_by_uuid(uuid)
            if not invoice_record:
                 return self._json_response(success=False, message='Invoice not found', status_code=404)

            success = invoice_service.delete_invoice(uuid) # Service handles unlink
            if success:
                return self._json_response(message='Invoice deleted successfully') # No data to return on successful delete
            else:
                # This path might not be reachable if search succeeded but delete failed internally
                return self._json_response(success=False, message='Invoice deletion failed', status_code=500)
        except Exception as e:
             # Log the exception e
            request.env.cr.rollback()
            # Check for specific database constraint errors (e.g., restrict)
            # from psycopg2 import errors
            # if isinstance(e.pgcode, errors.ForeignKeyViolation):
            #    return self._json_response(success=False, message='Cannot delete invoice, it is referenced elsewhere.', status_code=409) # 409 Conflict
            return self._json_response(success=False, message=f"Failed to delete invoice: {str(e)}", status_code=500)
# REMOVED //
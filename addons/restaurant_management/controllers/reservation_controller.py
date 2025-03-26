from odoo import http
from odoo.http import request

class ReservationController(http.Controller):

    @http.route('/reservations', type='json', auth='user')
    def list_reservations(self):
        reservations = request.env['restaurant_management.reservation'].search([])
        return reservations.read()

    @http.route('/reservations/<string:uuid>', type='json', auth='user')
    def get_reservation(self, uuid):
        reservation_service = request.env['restaurant_management.reservation_service']
        reservation = reservation_service.read_reservation(uuid)
        return {'status': 'success', 'data': reservation} if reservation else {'status': 'error', 'message': 'Reservation not found'}

    @http.route('/reservations', type='json', auth='user', methods=['POST'])
    def create_reservation(self, **kwargs):
        reservation_service = request.env['restaurant_management.reservation_service']
        reservation = reservation_service.create_reservation(kwargs)
        return {'status': 'success', 'data': reservation.read()} if reservation else {'status': 'error', 'message': 'Failed to create reservation'}

    @http.route('/reservations/<string:uuid>', type='json', auth='user', methods=['PUT'])
    def update_reservation(self, uuid, **kwargs):
        reservation_service = request.env['restaurant_management.reservation_service']
        reservation = reservation_service.update_reservation(uuid, kwargs)
        return {'status': 'success', 'data': reservation} if reservation else {'status': 'error', 'message': 'Reservation not found or update failed'}

    @http.route('/reservations/<string:uuid>', type='json', auth='user', methods=['DELETE'])
    def delete_reservation(self, uuid):
        reservation_service = request.env['restaurant_management.reservation_service']
        success = reservation_service.delete_reservation(uuid)
        return {'status': 'success'} if success else {'status': 'error', 'message': 'Reservation not found or delete failed'}
from odoo import http
from odoo.http import request

class ReservationController(http.Controller):

    @http.route('/reservations', type='json', auth='user')
    def list_reservations(self):
        reservations = request.env['restaurant_management.reservation'].search([])
        return reservations.read()

    @http.route('/reservations/<int:reservation_id>', type='json', auth='user')
    def get_reservation(self, reservation_id):
        reservation = request.env['restaurant_management.reservation'].browse(reservation_id)
        return reservation.read()

    @http.route('/reservations', type='json', auth='user', methods=['POST'])
    def create_reservation(self, **kwargs):
        reservation_service = request.env['restaurant_management.reservation_service']
        reservation = reservation_service.create_reservation(kwargs)
        return reservation.read()

    @http.route('/reservations/<int:reservation_id>', type='json', auth='user', methods=['PUT'])
    def update_reservation(self, reservation_id, **kwargs):
        reservation_service = request.env['restaurant_management.reservation_service']
        reservation = reservation_service.update_reservation(reservation_id, kwargs)
        return reservation.read()

    @http.route('/reservations/<int:reservation_id>', type='json', auth='user', methods=['DELETE'])
    def delete_reservation(self, reservation_id):
        reservation_service = request.env['restaurant_management.reservation_service']
        reservation_service.delete_reservation(reservation_id)
        return {'status': 'success'}
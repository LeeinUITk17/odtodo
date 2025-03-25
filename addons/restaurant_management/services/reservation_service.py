from odoo import models, api

class ReservationService(models.AbstractModel):
    _name = 'restaurant_management.reservation_service'
    _description = 'Reservation Service'

    @api.model
    def create_reservation(self, vals):
        return self.env['restaurant_management.reservation'].create(vals)

    @api.model
    def read_reservation(self, reservation_id):
        return self.env['restaurant_management.reservation'].browse(reservation_id).read()

    @api.model
    def update_reservation(self, reservation_id, vals):
        reservation = self.env['restaurant_management.reservation'].browse(reservation_id)
        reservation.write(vals)
        return reservation

    @api.model
    def delete_reservation(self, reservation_id):
        reservation = self.env['restaurant_management.reservation'].browse(reservation_id)
        reservation.unlink()
        return True
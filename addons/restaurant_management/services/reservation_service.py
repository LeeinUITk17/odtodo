from odoo import models, api

class ReservationService(models.AbstractModel):
    _name = 'restaurant_management.reservation_service'
    _description = 'Reservation Service'

    @api.model
    def create_reservation(self, vals):
        return self.env['restaurant_management.reservation'].create(vals)

    @api.model
    def read_reservation(self, uuid):
        reservation = self.env['restaurant_management.reservation'].search([('uuid', '=', uuid)], limit=1)
        if reservation:
            return reservation.read()
        return False

    @api.model
    def update_reservation(self, uuid, vals):
        reservation = self.env['restaurant_management.reservation'].search([('uuid', '=', uuid)], limit=1)
        if reservation:
            reservation.write(vals)
            return reservation.read()
        return False

    @api.model
    def delete_reservation(self, uuid):
        reservation = self.env['restaurant_management.reservation'].search([('uuid', '=', uuid)], limit=1)
        if reservation:
            reservation.unlink()
            return True
        return False
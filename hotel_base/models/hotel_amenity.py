from odoo import fields, models


class HotelAmenity(models.Model):
    _name = "hotel.amenity"
    _description = "Hotel Amenity"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char(required=True, tracking=True)
    active = fields.Boolean(default=True)
    description = fields.Text()

    _sql_constraints = [
        ("hotel_amenity_name_uniq", "unique(name)", "Amenity name must be unique."),
    ]
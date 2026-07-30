from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HotelRoomCategory(models.Model):
    _name = "hotel.room.category"
    _description = "Hotel Room Category"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char(required=True, tracking=True)
    code = fields.Char(required=True, tracking=True)
    active = fields.Boolean(default=True)

    property_id = fields.Many2one(
        "hotel.property",
        string="Property",
        required=True,
        index=True,
        ondelete="cascade",
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        related="property_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )

    description = fields.Html()
    capacity_adult = fields.Integer(default=1, required=True)
    capacity_child = fields.Integer(default=0, required=True)
    base_price = fields.Monetary(currency_field="currency_id")
    extra_bed_allowed = fields.Boolean(default=False)
    extra_bed_price = fields.Monetary(currency_field="currency_id")
    currency_id = fields.Many2one(
        "res.currency",
        related="property_id.currency_id",
        store=True,
        readonly=True,
    )

    amenity_ids = fields.Many2many(
        "hotel.amenity",
        "hotel_room_category_amenity_rel",
        "room_category_id",
        "amenity_id",
        string="Amenities",
    )
    tax_ids = fields.Many2many(
        "hotel.tax",
        "hotel_room_category_tax_rel",
        "room_category_id",
        "tax_id",
        string="Taxes",
        domain="[('company_id', '=', company_id)]",
    )

    _sql_constraints = [
        ("hotel_room_category_code_property_uniq", "unique(code, property_id)", "Room category code must be unique per property."),
        ("hotel_room_category_name_property_uniq", "unique(name, property_id)", "Room category name must be unique per property."),
    ]

    @api.constrains("capacity_adult", "capacity_child", "base_price", "extra_bed_price")
    def _check_values(self):
        for rec in self:
            if rec.capacity_adult < 1:
                raise ValidationError(_("Adult capacity must be at least 1."))
            if rec.capacity_child < 0:
                raise ValidationError(_("Child capacity cannot be negative."))
            if rec.base_price < 0:
                raise ValidationError(_("Base price cannot be negative."))
            if rec.extra_bed_price < 0:
                raise ValidationError(_("Extra bed price cannot be negative."))

    @api.constrains("code")
    def _check_code(self):
        for rec in self:
            if " " in (rec.code or ""):
                raise ValidationError(_("Room category code cannot contain spaces."))
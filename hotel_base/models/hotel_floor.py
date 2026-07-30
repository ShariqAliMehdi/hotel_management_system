from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HotelFloor(models.Model):
    _name = "hotel.floor"
    _description = "Hotel Floor"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sequence, name"

    name = fields.Char(required=True, tracking=True)
    code = fields.Char(required=True, tracking=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    property_id = fields.Many2one(
        "hotel.property",
        string="Property",
        required=True,
        index=True,
        ondelete="cascade",
    )
    building_id = fields.Many2one(
        "hotel.building",
        string="Building",
        required=True,
        index=True,
        ondelete="cascade",
        domain="[('property_id', '=', property_id)]",
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        related="property_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )

    _sql_constraints = [
        ("hotel_floor_code_building_uniq", "unique(code, building_id)", "Floor code must be unique per building."),
        ("hotel_floor_name_building_uniq", "unique(name, building_id)", "Floor name must be unique per building."),
    ]

    @api.constrains("property_id", "building_id")
    def _check_building_property(self):
        for rec in self:
            if rec.building_id and rec.building_id.property_id != rec.property_id:
                raise ValidationError(_("Building must belong to the selected property."))

    @api.constrains("code")
    def _check_code(self):
        for rec in self:
            if " " in (rec.code or ""):
                raise ValidationError(_("Floor code cannot contain spaces."))
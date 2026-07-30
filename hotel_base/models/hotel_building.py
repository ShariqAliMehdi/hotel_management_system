from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HotelBuilding(models.Model):
    _name = "hotel.building"
    _description = "Hotel Building"
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
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        related="property_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )

    floor_ids = fields.One2many(
        "hotel.floor",
        "building_id",
        string="Floors",
    )
    floor_count = fields.Integer(compute="_compute_floor_count")

    _sql_constraints = [
        ("hotel_building_code_property_uniq", "unique(code, property_id)", "Building code must be unique per property."),
        ("hotel_building_name_property_uniq", "unique(name, property_id)", "Building name must be unique per property."),
    ]

    @api.depends("floor_ids")
    def _compute_floor_count(self):
        for rec in self:
            rec.floor_count = len(rec.floor_ids)

    @api.constrains("code")
    def _check_code(self):
        for rec in self:
            if " " in (rec.code or ""):
                raise ValidationError(_("Building code cannot contain spaces."))

    def action_view_floors(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Floors",
            "res_model": "hotel.floor",
            "view_mode": "list,form",
            "domain": [("building_id", "=", self.id)],
            "context": {
                "default_property_id": self.property_id.id,
                "default_building_id": self.id,
            },
        }
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HotelSeason(models.Model):
    _name = "hotel.season"
    _description = "Hotel Season"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_start, name"

    name = fields.Char(required=True, tracking=True)
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
    date_start = fields.Date(required=True, tracking=True)
    date_end = fields.Date(required=True, tracking=True)
    season_type = fields.Selection(
        [
            ("regular", "Regular"),
            ("peak", "Peak"),
            ("festival", "Festival"),
            ("off", "Off Season"),
        ],
        default="regular",
        required=True,
        tracking=True,
    )
    price_factor = fields.Float(
        default=1.0,
        help="Multiplier for room price calculations in downstream modules.",
    )
    notes = fields.Text()

    _sql_constraints = [
        ("hotel_season_name_property_uniq", "unique(name, property_id)", "Season name must be unique per property."),
    ]

    @api.constrains("date_start", "date_end", "price_factor")
    def _check_dates(self):
        for rec in self:
            if rec.date_end < rec.date_start:
                raise ValidationError(_("End date must be greater than or equal to start date."))
            if rec.price_factor <= 0:
                raise ValidationError(_("Price factor must be greater than zero."))
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HotelProperty(models.Model):
    _name = "hotel.property"
    _description = "Hotel Property"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char(
        string="Property Name",
        required=True,
        tracking=True,
    )
    code = fields.Char(
        string="Reference",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _("New"),
        tracking=True,
        index=True,
    )
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
        index=True,
        ondelete="restrict",
    )

    partner_id = fields.Many2one(
        "res.partner",
        string="Contact",
        tracking=True,
    )
    street = fields.Char()
    street2 = fields.Char()
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string="State")
    zip = fields.Char(string="ZIP")
    country_id = fields.Many2one("res.country", string="Country")
    phone = fields.Char()
    email = fields.Char()
    website = fields.Char()

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        related="company_id.currency_id",
        store=True,
        readonly=True,
    )

    checkin_time = fields.Float(
        string="Default Check-In Time",
        default=14.0,
        help="Time in 24-hour float format, e.g. 14.5 = 14:30",
    )
    checkout_time = fields.Float(
        string="Default Check-Out Time",
        default=12.0,
        help="Time in 24-hour float format, e.g. 11.5 = 11:30",
    )

    building_ids = fields.One2many(
        "hotel.building",
        "property_id",
        string="Buildings",
    )
    floor_ids = fields.One2many(
        "hotel.floor",
        "property_id",
        string="Floors",
    )
    room_category_ids = fields.One2many(
        "hotel.room.category",
        "property_id",
        string="Room Categories",
    )
    amenity_ids = fields.Many2many(
        "hotel.amenity",
        "hotel_property_amenity_rel",
        "property_id",
        "amenity_id",
        string="Default Amenities",
    )
    tax_ids = fields.Many2many(
        "hotel.tax",
        "hotel_property_tax_rel",
        "property_id",
        "tax_id",
        string="Applicable Taxes",
    )
    season_ids = fields.One2many(
        "hotel.season",
        "property_id",
        string="Seasons",
    )

    building_count = fields.Integer(compute="_compute_counts")
    floor_count = fields.Integer(compute="_compute_counts")
    room_category_count = fields.Integer(compute="_compute_counts")
    season_count = fields.Integer(compute="_compute_counts")

    _sql_constraints = [
        ("hotel_property_code_uniq", "unique(code)", "Property reference must be unique."),
        ("hotel_property_name_company_uniq", "unique(name, company_id)", "Property name must be unique per company."),
    ]

    @api.depends("building_ids", "floor_ids", "room_category_ids", "season_ids")
    def _compute_counts(self):
        for rec in self:
            rec.building_count = len(rec.building_ids)
            rec.floor_count = len(rec.floor_ids)
            rec.room_category_count = len(rec.room_category_ids)
            rec.season_count = len(rec.season_ids)

    @api.constrains("checkin_time", "checkout_time")
    def _check_time_range(self):
        for rec in self:
            if rec.checkin_time < 0 or rec.checkin_time >= 24:
                raise ValidationError(_("Check-In Time must be between 0 and 24."))
            if rec.checkout_time < 0 or rec.checkout_time >= 24:
                raise ValidationError(_("Check-Out Time must be between 0 and 24."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("code", _("New")) == _("New"):
                vals["code"] = self.env["ir.sequence"].next_by_code("hotel_base.hotel_property") or _("New")
        records = super().create(vals_list)
        for record in records:
            if not record.partner_id:
                partner = self.env["res.partner"].create({
                    "name": record.name,
                    "phone": record.phone,
                    "email": record.email,
                    "street": record.street,
                    "street2": record.street2,
                    "city": record.city,
                    "zip": record.zip,
                    "state_id": record.state_id.id,
                    "country_id": record.country_id.id,
                    "company_id": record.company_id.id,
                    "is_company": True,
                })
                record.partner_id = partner.id
        return records

    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            if rec.partner_id:
                rec.partner_id.write({
                    "name": rec.name,
                    "phone": rec.phone,
                    "email": rec.email,
                    "street": rec.street,
                    "street2": rec.street2,
                    "city": rec.city,
                    "zip": rec.zip,
                    "state_id": rec.state_id.id,
                    "country_id": rec.country_id.id,
                })
        return res

    def action_view_buildings(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Buildings",
            "res_model": "hotel.building",
            "view_mode": "list,form",
            "domain": [("property_id", "=", self.id)],
            "context": {"default_property_id": self.id},
        }

    def action_view_floors(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Floors",
            "res_model": "hotel.floor",
            "view_mode": "list,form",
            "domain": [("property_id", "=", self.id)],
            "context": {"default_property_id": self.id},
        }

    def action_view_room_categories(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Room Categories",
            "res_model": "hotel.room.category",
            "view_mode": "list,form",
            "domain": [("property_id", "=", self.id)],
            "context": {"default_property_id": self.id},
        }

    def action_view_seasons(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Seasons",
            "res_model": "hotel.season",
            "view_mode": "list,form",
            "domain": [("property_id", "=", self.id)],
            "context": {"default_property_id": self.id},
        }

    def _cron_validate_season_overlaps(self):
        properties = self.search([("active", "=", True)])
        for property_rec in properties:
            seasons = property_rec.season_ids.filtered(lambda s: s.active).sorted(key=lambda s: (s.date_start or fields.Date.today(), s.date_end or fields.Date.today()))
            for index, season in enumerate(seasons):
                for next_season in seasons[index + 1:]:
                    if season.date_end and next_season.date_start and season.date_end >= next_season.date_start:
                        body = _(
                            "Season overlap detected between <b>%s</b> and <b>%s</b>."
                        ) % (season.name, next_season.name)
                        property_rec.message_post(body=body)
                        break
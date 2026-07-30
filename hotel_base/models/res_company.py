from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    hotel_property_ids = fields.One2many(
        "hotel.property",
        "company_id",
        string="Hotel Properties",
    )
    hotel_default_property_id = fields.Many2one(
        "hotel.property",
        string="Default Hotel Property",
        domain="[('company_id', '=', id)]",
    )
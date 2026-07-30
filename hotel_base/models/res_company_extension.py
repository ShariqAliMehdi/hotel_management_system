from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    hotel_property_ids = fields.One2many(
        comodel_name="hotel.property",
        inverse_name="company_id",
        string="Hotel Properties",
    )

    hotel_default_currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Default Hotel Currency",
        default=lambda self: self.env.company.currency_id.id,
    )

    hotel_default_tax_id = fields.Many2one(
        comodel_name="hotel.tax",
        string="Default Hotel Tax",
    )

    @api.onchange("hotel_default_currency_id")
    def _onchange_default_currency(self):
        if self.hotel_default_currency_id:
            for prop in self.hotel_property_ids:
                if not prop.currency_id:
                    prop.currency_id = self.hotel_default_currency_id.id
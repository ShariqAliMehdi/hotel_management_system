from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HotelTax(models.Model):
    _name = "hotel.tax"
    _description = "Hotel Tax"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char(required=True, tracking=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
        index=True,
        ondelete="cascade",
    )
    amount_type = fields.Selection(
        [
            ("percent", "Percentage"),
            ("fixed", "Fixed Amount"),
        ],
        required=True,
        default="percent",
        tracking=True,
    )
    amount = fields.Float(required=True, default=0.0, tracking=True)
    price_include = fields.Boolean(string="Included in Price", default=False)

    _sql_constraints = [
        ("hotel_tax_name_company_uniq", "unique(name, company_id)", "Tax name must be unique per company."),
    ]

    @api.constrains("amount", "amount_type")
    def _check_amount(self):
        for rec in self:
            if rec.amount_type == "percent" and (rec.amount < 0 or rec.amount > 100):
                raise ValidationError(_("Percentage tax must be between 0 and 100."))
            if rec.amount_type == "fixed" and rec.amount < 0:
                raise ValidationError(_("Fixed tax cannot be negative."))
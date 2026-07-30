from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestHotelBase(TransactionCase):

    def setUp(self):
        super().setUp()
        self.company = self.env.company
        self.property = self.env["hotel.property"].create({
            "name": "Test Hotel",
            "company_id": self.company.id,
        })

    def test_property_sequence_generated(self):
        self.assertTrue(self.property.code)
        self.assertNotEqual(self.property.code, "New")

    def test_building_property_validation(self):
        second_property = self.env["hotel.property"].create({
            "name": "Another Hotel",
            "company_id": self.company.id,
        })
        building = self.env["hotel.building"].create({
            "name": "Building A",
            "code": "BA",
            "property_id": self.property.id,
        })
        with self.assertRaises(ValidationError):
            self.env["hotel.floor"].create({
                "name": "Floor 1",
                "code": "F1",
                "property_id": second_property.id,
                "building_id": building.id,
            })

    def test_room_category_capacity_validation(self):
        with self.assertRaises(ValidationError):
            self.env["hotel.room.category"].create({
                "name": "Invalid Category",
                "code": "INV",
                "property_id": self.property.id,
                "capacity_adult": 0,
            })

    def test_season_date_validation(self):
        with self.assertRaises(ValidationError):
            self.env["hotel.season"].create({
                "name": "Bad Season",
                "property_id": self.property.id,
                "date_start": "2025-12-31",
                "date_end": "2025-01-01",
                "price_factor": 1.0,
            })
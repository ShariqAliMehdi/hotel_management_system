from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import date


class TestHotelBase(TransactionCase):
    def setUp(self):
        super().setUp()
        self.Property = self.env["hotel.property"]
        self.Building = self.env["hotel.building"]
        self.Floor = self.env["hotel.floor"]
        self.RoomType = self.env["hotel.room.type"]
        self.Amenity = self.env["hotel.amenity"]
        self.Tax = self.env["hotel.tax"]
        self.Season = self.env["hotel.seasonal.calendar"]

        self.company = self.env.company

    def test_property_display_name(self):
        prop = self.Property.create({
            "company_id": self.company.id,
            "name": "Test Property",
            "currency_id": self.company.currency_id.id,
        })
        self.assertIn("Test Property", prop.display_name)

    def test_floor_dates_times_constraints(self):
        prop = self.Property.create({
            "company_id": self.company.id,
            "name": "Time Check Property",
            "currency_id": self.company.currency_id.id,
            "default_checkin_time": 10.0,
            "default_checkout_time": 10.0,  # invalid (equal)
        })
        with self.assertRaises(ValidationError):
            prop._check_times()

    def test_room_type_capacity_constraints(self):
        prop = self.Property.create({
            "company_id": self.company.id,
            "name": "Capacity Prop",
            "currency_id": self.company.currency_id.id,
        })
        with self.assertRaises(ValidationError):
            self.RoomType.create({
                "property_id": prop.id,
                "name": "Bad Type",
                "capacity_adults": 0,
                "capacity_children": 0,
                "base_rate": 10.0,
            })

    def test_seasonal_calendar_dates(self):
        prop = self.Property.create({
            "company_id": self.company.id,
            "name": "Season Prop",
            "currency_id": self.company.currency_id.id,
        })
        with self.assertRaises(ValidationError):
            self.Season.create({
                "property_id": prop.id,
                "name": "Invalid Season",
                "season_type": "standard",
                "date_from": date(2026, 2, 2),
                "date_to": date(2026, 1, 1),
            })
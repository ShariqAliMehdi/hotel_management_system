# Hotel Base (Odoo 19)

Core configuration models for the Hotel Management ERP:
- Hotel Properties (stored in `hotel.property`, linked to `res.company`)
- Buildings, Floors
- Room Types and Amenities
- Hotel Taxes and Seasonal Calendars

## Installation
1. Copy `hotel_base` into your Odoo addons path.
2. Update apps list and install **Hotel Base**.
3. Load demo data if desired.

## Notes
- Multi-company is enforced using record rules based on `res.company` / `user.company_id`.
from . import db
from datetime import datetime

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    continent = db.Column(db.String(50), nullable=False)
    travel_status = db.Column(db.String(20), nullable=False, default="Wishlist")  # Options: Visited, Planned, Wishlist
    # One-to-many relationship: a country can have many travel entries
    entries = db.relationship("Entry", backref="country", lazy=True)

    def __repr__(self):
        return f"<Country {self.name}>"

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey("country.id"), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=True)  # 1 to 5
    travel_date = db.Column(db.Date, nullable=True)
    photo_filename = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Entry {self.city} in {self.country.name}>"
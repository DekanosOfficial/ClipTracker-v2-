#### models.py
from database import db
from datetime import datetime, timezone, timedelta

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20))

    phone_no = db.Column(db.String(20))

    visit_count = db.Column(db.Integer, default=0)

    cycle_start_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_visit_date = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    visits = db.relationship("Visit", backref="customer",lazy=True, cascade="all, delete-orphan")

    def __init__(self, first_name, last_name=None, phone_no=None, visit_count=0, cycle_start_date=None):
        self.first_name=first_name
        self.last_name=last_name
        self.phone_no=phone_no
        self.visit_count=visit_count
        self.cycle_start_date=cycle_start_date


class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    visited_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    discount_applied = db.Column(db.String(20), default="none")
    notes = db.Column(db.String(200))

    def __init__(self, customer_id, visited_at=None, discount_applied="none", notes=None):
        self.customer_id=customer_id
        self.visited_at=visited_at or datetime.now(timezone.utc)
        self.discount_applied=discount_applied
        self.notes=notes
        
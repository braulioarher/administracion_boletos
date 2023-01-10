from db import db

class TicketModel(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    is_sold = db.Column(db.Boolean, unique=False, default=False)
    is_redeemed = db.Column(db.Boolean, unique=False, default=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), unique=False, nullable=False)
    event = db.relationship("EventModel", back_populates="tickets")
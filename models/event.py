from db import db

class EventModel(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    start_date = db.Column(db.datetime, nullable=False)
    end_date = db.Column(db.datetime, nullable=False)
    tickets = db.relationship("EventModel", back_populates="event", lazy="dynamic", cascade="all, delete-orphan")
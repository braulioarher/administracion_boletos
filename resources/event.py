from datetime import datetime
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from app import db
from models import EventModel, TicketModel
from schemas import EventSchema

blp = Blueprint("events", __name__, description="Operations on events")

@blp.route("/event/<string:event_id>")
class Event(MethodView):

    blp.response(200, EventSchema)
    def get(self, event_id):
        event_data = EventModel.query.get_or_404(event_id)
        total_tickets = db.session.query(EventModel.id).join(TicketModel, TicketModel.event_id == EventModel.id).count()
        sold_tickets = db.session.query(EventModel.id).join(TicketModel, TicketModel.event_id == EventModel.id).filter(TicketModel.is_sold==True).count()
        redeemed_tickets = db.session.query(EventModel.id).join(TicketModel, TicketModel.event_id == EventModel.id).filter(TicketModel.is_redeemed==True).count()

        event = {
            "name": event_data.name,
            "start_date": event_data.start_date,
            "end_date": event_data.end_date,
            "boletos_totales": total_tickets,
            "boletos_venditos": sold_tickets,
            "boletos_canjeados": redeemed_tickets
        }
        return event

    def delete(self, event_id):
        event = EventModel.query.get_or_404(event_id)
        sold_tickets = db.session.query(EventModel.id).join(TicketModel, TicketModel.event_id == EventModel.id).filter(TicketModel.is_sold==True).count()
        if event.end_date < datetime.now() and sold_tickets > 0:
            abort(500, message="Error, no puedes borrar evento ya que tiene boletos vendidos")
        db.session.delete(event)
        db.session.commit()
        return {"message": "Evento borrado"}

@blp.route("/events")
class EventList(MethodView):
    @blp.response(200, EventSchema(many=True))
    def get(self):
        events = EventModel.query.all()
        return events

    @blp.arguments(EventSchema)
    @blp.response(200, EventSchema)
    def post(self, event_data):
        event = EventModel(name=event_data["name"], start_date=event_data["start_date"], end_date=event_data["end_date"])
        tickets = event_data["tickets_num"] 
        if event_data["start_date"] < datetime.now():
            abort(500, message="La fecha del evento no puede ser menor a la de hoy")
        if event_data["start_date"] > event_data["end_date"]:
            abort(500, message="La fecha de inicio del evento no puede ser mayor a la del final")
        if 1 < event_data["tickets_num"] > 300:
            abort(500, message="El rango de boletos a crear debe ser entre 1 y 300")
        try:
            db.session.add(event)
            db.session.commit()
            data_added = EventModel.query.filter_by(name=event_data["name"]).first()
            for i in range(tickets):
                ticket = TicketModel(id=str(data_added.id)+str(i), is_sold=False, is_redeemed=False, event_id=data_added.id)
                db.session.add(ticket)
                db.session.commit()
                
        except SQLAlchemyError:
            abort(500, message="Un error ocurrio al insertar el evento")

        return event, 201
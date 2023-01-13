from datetime import datetime
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from app import db
from models import EventModel, TicketModel
from schemas import EventSchema, EventUpdateSchema, EventDetailSchema

blp = Blueprint("events", __name__, description="Operations on events")

# Declaracion de ruta para los recursos de un evento en particular
@blp.route("/event/<string:event_id>")
class Event(MethodView):

    @blp.response(200, EventDetailSchema)
    def get(self, event_id):
        event_data = EventModel.query.get_or_404(event_id)
        total_tickets = db.session.query(EventModel.id).join(TicketModel, TicketModel.event_id == EventModel.id).count()
        sold_tickets = db.session.query(EventModel.id).join(TicketModel, TicketModel.event_id == EventModel.id).filter(TicketModel.is_sold==True).count()
        redeemed_tickets = db.session.query(EventModel.id).join(TicketModel, TicketModel.event_id == EventModel.id).filter(TicketModel.is_redeemed==True).count()

        event = {
            "id": event_data.id,
            "name": event_data.name,
            "start_date": event_data.start_date,
            "end_date": event_data.end_date,
            "boletos_totales": total_tickets,
            "boletos_venditos": sold_tickets,
            "boletos_canjeados": redeemed_tickets,
        }
        return event

    # Recurso para eliminar evento en base a su id
    def delete(self, event_id):
        # Verifica el evento exista en la db
        event = EventModel.query.get_or_404(event_id)
        sold_tickets = db.session.query(EventModel.id).join(TicketModel, TicketModel.event_id == EventModel.id).filter(TicketModel.is_sold==True).count()
        # Validacion para no borrar un evento con boletos vendidos y que no haya ocurrido
        if event.end_date < datetime.now() and sold_tickets > 0:
            abort(500, message="Error, no puedes borrar evento ya que tiene boletos vendidos")
        db.session.delete(event)
        db.session.commit()
        return {"message": "Evento borrado"}

    @blp.arguments(EventUpdateSchema)
    @blp.response(200, EventUpdateSchema)
    def put(self, event_data, event_id):
        event = EventModel.query.get(event_id)
        # Valida que el evento exista
        if event:
            # Valida fechas y numero de boletos antes de agregar/disminuir
            if event_data["start_date"] < event.start_date:
                abort(500, message="La fecha de inicio del evento no puede ser menor a la ya gurdada")
            if event_data["start_date"] > event_data["end_date"]:
                abort(500, message="La fecha de inicio del evento no puede ser mayor a la del final")
            total_tickets = db.session.query(EventModel.id).join(TicketModel, TicketModel.event_id == EventModel.id).count()
            sold_tickets = db.session.query(EventModel.id).join(TicketModel, TicketModel.event_id == EventModel.id).filter(TicketModel.is_sold==True).count()
            # Revisa que el payload de event_data contenga tickets_num
            if "tickets_num" in event_data:
                # Validaciones para Agregar/Eliminar Tickets
                if sold_tickets >= event_data["tickets_num"]:
                    abort(500, message="No puedes disminur la cantidad de boletos ya que es menor a los ya vendidos")
                # Agrega/Elimina boletos
                if total_tickets < event_data["tickets_num"]:
                    event.name = event_data["name"]
                    event.start_date = event_data["start_date"]
                    event.end_date = event_data["end_date"]

                    for i in range(total_tickets, event_data["tickets_num"]):
                        ticket = TicketModel(id=str(event_id) + str(i), is_sold=False, is_redeemed=False, event_id=event_id)
                        try:
                            db.session.add(ticket)
                            db.session.commit()
                        except SQLAlchemyError:
                            abort(500, message="Un error ocurrio al insertar el Ticket")
                    db.session.add(event)
                    db.session.commit()
                    return event
                else:
                    event.name = event_data["name"]
                    event.start_date = event_data["start_date"]
                    event.end_date = event_data["end_date"]
                    for i in range(total_tickets-1, event_data["tickets_num"]-1, -1):
                        ticket = TicketModel.query.get_or_404(str(event_id) + str(i))
                        db.session.delete(ticket)
                        db.session.commit()
                    db.session.add(event)
                    db.session.commit()
                    return event
            else:
                event.name = event_data["name"]
                event.start_date = event_data["start_date"]
                event.end_date = event_data["end_date"]
                db.session.add(event)
                db.session.commit()
                return event
        else:
            abort(500, message="El evento que quieres actualizar no existe")

# Declaracion de ruta para recurso de crear y ver eventos
@blp.route("/events")
class EventList(MethodView):
    # Recurso que trae todos los eventos disponibles
    @blp.response(200, EventSchema(many=True))
    def get(self):
        events = EventModel.query.all()
        return events

    # Recurso para crear un evento
    @blp.arguments(EventSchema)
    @blp.response(200, EventSchema)
    def post(self, event_data):
        event = EventModel(name=event_data["name"], start_date=event_data["start_date"], end_date=event_data["end_date"])
        tickets = event_data["tickets_num"]
        # Validaciones de fechas y numeros de boletos para crear evento
        if event_data["start_date"] < datetime.now():
            abort(500, message="La fecha del evento no puede ser menor a la de hoy")
        if event_data["start_date"] > event_data["end_date"]:
            abort(500, message="La fecha de inicio del evento no puede ser mayor a la del final")
        if 1 < event_data["tickets_num"] > 300:
            abort(500, message="El rango de boletos a crear debe ser entre 1 y 300")
        # Agregando evento a la db
        try:
            db.session.add(event)
            db.session.commit()
            data_added = EventModel.query.filter_by(name=event_data["name"]).first()
            for i in range(tickets):
                ticket = TicketModel(id=str(data_added.id)+str(i), is_sold=False, is_redeemed=False, event_id=data_added.id)
                db.session.add(ticket)
                db.session.commit()
        # En caso de error al agregar evento aborta     
        except SQLAlchemyError:
            abort(500, message="Un error ocurrio al insertar el evento")

        return event, 201
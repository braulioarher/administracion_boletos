from datetime import datetime

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from app import db
from models import EventModel, TicketModel
from schemas import PlainTicketSchema

blp = Blueprint("tickets", __name__, description="Operations on tickets")

# Ruta para recurso de vender boleto segun su id
@blp.route("/ticket/sell/<string:ticket_id>")
class VenderTicket(MethodView):
    
    @blp.response(200, PlainTicketSchema)
    def put(self, ticket_id):
        ticket = TicketModel.query.get_or_404(ticket_id)
        if ticket.is_sold == True:
            abort(403, message="Este boleto ya ha sido vendido")

        ticket.is_sold = True
        db.session.add(ticket)
        db.session.commit()

        return ticket, 201

# Ruta de recurso para canjear boleto
@blp.route("/ticket/redeem/<string:ticket_id>")
class CanjearTicket(MethodView):
    
    @blp.response(200, PlainTicketSchema)
    def put(self, ticket_id):
        ticket = TicketModel.query.get_or_404(ticket_id)
        event = EventModel.query.get_or_404(ticket.event_id)
        if event.start_date <= datetime.now() <= event.end_date:
            if ticket.is_sold == False:
                abort(403, message="No se puede canjear boleto ya que no ha sido vendido")
            if ticket.is_redeemed == True:
                abort(403, message="Error este boleto ya ha sido cajeado")

            ticket.is_redeemed = True
            db.session.add(ticket)
            db.session.commit()

            return ticket, 201
        else: 
            abort(403, message=f"Solo puedes cajear el boleto durante el evento")

        
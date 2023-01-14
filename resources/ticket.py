from datetime import datetime
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from app import db
from models import EventModel, TicketModel
from schemas import PlainTicketSchema

blp = Blueprint("tickets", __name__, description="Operations on tickets")

@blp.route("/ticket/sell/<string:ticket_id>")
class VenderTicket(MethodView):
    
    @blp.response(200, PlainTicketSchema)
    def put(self, ticket_id):
        ticket = TicketModel.query.get_or_404(ticket_id)
        ticket.is_sold = True
        db.session.add(ticket)
        db.session.commit()

        return ticket
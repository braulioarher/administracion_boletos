from marshmallow import Schema, fields

# Esquemas para validar la informacion proveniente del cliente
class PlainEventSchema(Schema):
    class Meta:
        ordered = True 

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    tickets_num = fields.Int(required=True)

class PlainTicketSchema(Schema):
    id = fields.Int(dump_only=True)
    is_sold = fields.Bool(required=True)
    is_redeemed = fields.Bool(required=True)

class EventSchema(PlainEventSchema):
    tickets = fields.List(fields.Nested(PlainTicketSchema()), dump_only=True)

class EventDetailSchema(PlainEventSchema):
    boletos_totales = fields.Int(dump_only=True)
    boletos_venditos = fields.Int(dump_only=True)
    boletos_canjeados = fields.Int(dump_only=True)

class EventUpdateSchema(Schema):
    name = fields.Str(required=True)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    tickets_num = fields.Int(required=False)
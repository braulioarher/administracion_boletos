from marshmallow import Schema, fields

class PlainEventSchema(Schema):
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

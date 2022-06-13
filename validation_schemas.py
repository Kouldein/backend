from marshmallow import Schema, fields
from marshmallow.validate import Length, Range


class UserSchema(Schema):
    username = fields.String(validate=Length(min=4))
    firstName = fields.String(validate=Length(min=3))
    lastName = fields.String(validate=Length(min=3))
    password = fields.String(validate=Length(min=8))
    email = fields.Email()
    phone = fields.Number()


class EventsSchema(Schema):
    header = fields.String()
    description = fields.String()
    date = fields.DateTime()

class InputEventsSchema(Schema):
    eventId = fields.Integer(strict=True)

class LoginSchema(Schema):
    username = fields.String()
    password = fields.String()
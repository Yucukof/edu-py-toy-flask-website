from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Str()
    username = fields.Str()
    password = fields.Str()
    is_anonymous = fields.Boolean()
    is_authenticated = fields.Boolean()
    is_active = fields.Boolean()
    is_admin = fields.Boolean()

from marshmallow import Schema, fields


class ClueSchema(Schema):
    id = fields.Integer()
    text = fields.Str()

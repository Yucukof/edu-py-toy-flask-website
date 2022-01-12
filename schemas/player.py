from marshmallow import Schema, fields


class PlayerSchema(Schema):
    user_id = fields.Integer()
    current_streak = fields.Integer()
    max_streak = fields.Integer()
    success = fields.Integer()
    failed = fields.Integer()
    total = fields.Integer()
    last_riddle = fields.Integer()

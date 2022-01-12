from marshmallow import Schema, fields, post_load

from models import User, Category
from schemas.category import CategorySchema
from schemas.clue import ClueSchema
from schemas.user import UserSchema


class RiddleSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    riddle = fields.Str()
    solution = fields.Boolean()
    explanation = fields.Str()
    difficulty = fields.Integer()
    created = fields.DateTime()

    user_id = fields.Integer()
    category_id = fields.Integer()

    category = fields.Nested(CategorySchema)
    clues = fields.List(fields.Nested(ClueSchema))
    creator = fields.Nested(UserSchema)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

    @post_load
    def make_category(self, data, **kwargs):
        return Category(**data)


class RiddlePagination(Schema):
    page = fields.Integer()
    pages = fields.Integer()
    per_page = fields.Integer()
    has_next = fields.Boolean()
    has_prev = fields.Boolean()
    next_num = fields.Integer()
    prev_num = fields.Integer()
    total = fields.Integer()
    items = fields.List(fields.Nested(RiddleSchema))

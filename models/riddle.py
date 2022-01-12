from datetime import datetime

from flask_login import current_user

from app import db


class Riddle(db.Model):
    """
    L'objet représenant une énigme.
    Comporte un lien vers les tables des utilisateurs (Users) et des indices (Clues)
    """

    # Core fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    riddle = db.Column(db.String(255), nullable=False)
    solution = db.Column(db.Boolean, nullable=False)
    explanation = db.Column(db.String(255))
    difficulty = db.Column(db.Integer, nullable=False, default=1)
    created = db.Column(db.TIMESTAMP(timezone=False), default=datetime.now())

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    # Relationships
    category = db.relationship("Category", backref=db.backref('riddles', lazy=True, cascade="all, delete-orphan"))
    creator = db.relationship("User", backref=db.backref('riddles', lazy=True, cascade="all, delete-orphan"))

    def __init__(self, name, riddle, solution, category_id, difficulty, explanation):
        self.name = name
        self.riddle = riddle
        self.solution = solution
        self.difficulty = difficulty
        self.explanation = explanation
        self.category_id = category_id if category_id else 1
        self.user_id = current_user.id
        self.created = datetime.now()

    def __repr__(self):
        return '<Riddle {}>'.format(self.name)

    def get_id(self):
        return self.id

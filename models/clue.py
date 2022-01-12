from app import db


class Clue(db.Model):
    """
    L'objet représentant un indice.
    Comporte un lien vers la table des énigmes (Riddle)
    """
    # Core attributes
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)

    # Foreign key attributes
    riddle_id = db.Column(db.Integer, db.ForeignKey('riddle.id'))

    # Relationships
    riddle = db.relationship("Riddle", backref=db.backref('clues', lazy=True, cascade="all, delete-orphan"))

    def __init__(self, text, riddle):
        self.text = text
        self.riddle_id = riddle

    def __repr__(self):
        return '<Clue {}>'.format(self.text)

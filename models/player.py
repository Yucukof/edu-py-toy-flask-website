from app import db


class Player(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    current_streak = db.Column(db.Integer, default=0)
    max_streak = db.Column(db.Integer, default=0)
    success = db.Column(db.Integer, default=0)
    failed = db.Column(db.Integer, default=0)
    total = db.Column(db.Integer, default=0)
    last_riddle = db.Column(db.Boolean, default=True)

    user = db.relationship("User"
                           , backref=db.backref('player'
                                                , lazy=False
                                                , uselist=False
                                                , cascade="all, delete-orphan")
                           )

    def __repr__(self):
        return '<Player "{}">'.format(self.user.username)

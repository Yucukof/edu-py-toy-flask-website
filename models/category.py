from app import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '{}'.format(self.name)


def get_all():
    return Category.query.all()


def get():
    return Category.query

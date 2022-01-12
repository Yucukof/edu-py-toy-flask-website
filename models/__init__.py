# https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
# https://docs.sqlalchemy.org/en/14/index.html
# https://docs.sqlalchemy.org/en/14/orm/loading_objects.html
# https://docs.sqlalchemy.org/en/13/core/sqlelement.html

from flask import current_app
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker

from app import db
from models.category import Category
# noinspection PyUnresolvedReferences
from models.clue import Clue
from models.player import Player
from models.riddle import Riddle
from models.user import User


def create_db(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
    app.config.from_mapping(
        SQLALCHEMY_ENGINE=engine
    )

    db.init_app(app)
    db.create_all()

    if User.query.all().__len__() == 0:
        admin = User("admin", "admin")
        admin.is_admin = True
        admin.player = Player()
        db.session.add(admin)

        user = User("user", "user")
        user.player = Player()
        db.session.add(user)

    if Category.query.all().__len__() == 0:
        query = insert(Category).values(
            id=1,
            name=u'Cinema'
        )
        db.session.execute(query)

        query = insert(Category).values(
            id=2,
            name=u'Sport'
        )
        db.session.execute(query)

        query = insert(Category).values(
            id=3,
            name=u'Histoire'
        )
        db.session.execute(query)

    default_user = User.query.filter_by(username='user').one_or_none()

    if Riddle.query.all().__len__() == 0:
        query = insert(Riddle).values(
            name=u'Tennis',
            riddle=u'Au tennis, tu peux recevoir une pénalité si on sent que tu n\'es pas à fond.',
            solution=True,
            explanation=u'Cela s\'appelle le \"lack of effort warning\"',
            category_id=2,
            difficulty=2,
            user_id=default_user.id
        )
        db.session.execute(query)

        query = insert(Riddle).values(
            name=u'My Name is Bond',
            riddle=u'Lorsqu\'il incarnait James Bond en 1995 et 2002, Pierce Brosnan n\'avait pas le droit de se montrer en smoking dans d\'autres films.',
            solution=False,
            explanation=u'Cette information a longtemps circulé mais ce n\'est qu\'une rumeur totalement infondée.',
            category_id=1,
            difficulty=1,
            user_id=default_user.id
        )
        db.session.execute(query)

        query = insert(Riddle).values(
            name=u'Accident',
            riddle=u'Un mécanicien qui jouait au golf sur une piste d\'atterrissage a détruit 5 avions de chasse à cause d\'un swing loupé.',
            solution=True,
            explanation=u'Il a tapé sur un pigeon, qui tomba sur le cockpit d\'un pilote qui perdit le contrôle et s\'encastra d\'autres avions.',
            difficulty=3,
            user_id=default_user.id
        )
        db.session.execute(query)

        query = insert(Riddle).values(
            name=u'Oscar',
            riddle=u'La femme de Georges Lucas a gagné plus d\'oscars que lui.',
            solution=True,
            explanation=u'Elle a gagné l\'oscar du meilleur montage pour Star Wars, lui n\'a jamais rien eu.',
            category_id=1,
            difficulty=3,
            user_id=default_user.id
        )
        db.session.execute(query)

        query = insert(Riddle).values(
            name=u'Dauphins dans la vague',
            riddle=u'Les dauphins se droguent régulièrement.',
            solution=True,
            explanation=u'Ces derniers utiliseraient le fugu, un poisson qui libère de la tétrodotoxine pour en tirer des effets euphorisants.',
            difficulty=4,
            user_id=default_user.id
        )
        db.session.execute(query)

        query = insert(Riddle).values(
            name=u'Poésie',
            riddle=u'Le mot "poétereau" qui a été supprimé du dictionnaire - heureusement - car c\'était un mot pour désigner un poète hétéro.',
            solution=False,
            explanation=u'C\'était un mot pour désigner un poète médiocre',
            difficulty=4,
            user_id=default_user.id
        )
        db.session.execute(query)

        query = insert(Riddle).values(
            name=u'La guerre',
            riddle=u'La guerre de six jours a en réalité 8 jours.',
            solution=False,
            explanation=u'Elle a bien duré 6 jours.',
            category_id=3,
            difficulty=4,
            user_id=default_user.id
        )
        db.session.execute(query)

        query = insert(Riddle).values(
            name=u'Bonjour',
            riddle=u'Un bonjour malaisien consiste à embrasser l\'intérieur de la main de sa fille, puis claquer dans ses mains.',
            solution=False,
            explanation=u'C\'est le bonjour zambien.',
            difficulty=4,
            user_id=default_user.id
        )
        db.session.execute(query)

        query = insert(Riddle).values(
            name=u'El Torero',
            riddle=u'La couleur rouge rend les taureaux agressifs.',
            solution=False,
            explanation=u'C\'est le mouvement de la cape qui les énerve',
            difficulty=4,
            user_id=default_user.id
        )
        db.session.execute(query)

    if Clue.query.all().__len__() == 0:
        query = insert(Clue).values(
            riddle_id=1,
            text=u'Tu n\'es pas à fond si tu joues sans raquette.'
        )
        db.session.execute(query)

        query = insert(Clue).values(
            riddle_id=1,
            text=u'Cela n\'a rien à voir avec des paris truqués.'
        )
        db.session.execute(query)

        db.session.commit()
        return db


def get_engine():
    return create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])


def get_session():
    return sessionmaker(bind=get_engine())

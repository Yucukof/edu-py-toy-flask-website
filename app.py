import os

from flask import Flask, redirect, url_for, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

last_riddle = None

db = None
login_manager = None
engine = None


# https://flask.palletsprojects.com/en/1.1.x/
# https://flask-assets.readthedocs.io/en/latest/

# noinspection PyUnresolvedReferences
def create_app(test_config=None):
    global db, login_manager
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    database = os.path.join(app.instance_path, 'data.db')
    # noinspection PyUnresolvedReferences
    from config import ProductionConfig
    app.config.from_object('config.ProductionConfig')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=database,
        TEMPLATES_AUTO_RELOAD=True,
        SQLALCHEMY_DATABASE_URI='sqlite:///' + database,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    )
    # Configure logging
    from logging.config import fileConfig
    fileConfig('logging.cfg')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Configure Database
    db = SQLAlchemy(app)
    from models import create_db
    create_db(app)
    Migrate(app, db)

    # Configure Authentication
    login_manager = LoginManager(app)
    from controllers import auth
    auth.init_login(app)

    # Register Blueprints
    from controllers import riddle, auth, clue
    app.register_blueprint(auth.bp)
    app.register_blueprint(clue.bp)

    # Configure Root
    @app.route('/')
    def hello_world():
        return redirect(url_for('.info_page'))

    @app.route('/infos')
    def info_page():
        return render_template("infos.html")

    @app.route('/login')
    def login():
        return redirect(url_for('auth.login'))

    @app.route('/logout')
    def logout():
        return redirect(url_for('auth.logout'))

    @app.errorhandler(404)
    def not_found(code):
        return render_template('maintenance/404.html')

    @app.errorhandler(501)
    def not_implemented(code):
        return render_template('maintenance/501.html')

    if __name__ == '__main__':
        create_app()
        app.run(debug=True)

    return app

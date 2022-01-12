import logging.config
import urllib.parse

from flask import render_template, redirect, abort, flash, Blueprint, request, url_for
from flask_login import login_user, logout_user, login_required, current_user

from app import login_manager, db
from forms.auth import LoginForm, RegisterForm
from models import Player
from models.user import User

# https://flask-login.readthedocs.io/en/latest/
# https://pythonbasics.org/flask-login/

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Configure logging
logging.config.fileConfig('logging.cfg')


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


# Configure Authentication
def init_login(app):
    login_manager.init_app(app)
    login_manager.login_view = "login"


@bp.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    next_page = get_next_page(request) or url_for('.success', new_connection=not current_user.is_authenticated)

    if current_user.is_authenticated:
        logging.debug("User is already authenticated.")
        logging.debug('Redirecting to %s', next_page)
        return redirect(next_page)

    if form.validate_on_submit():
        username = form.username.data.lower()
        user = User.query.filter_by(username=username).one_or_none()

        if user:
            password = form.password.data
            if not user.check_password(password):
                message = 'Le mot de passe est erroné'
                flash(message, "Error")
                return render_template('auth/login.html', form=form)

            login_user(user, remember=request.form.get('remember'))

            logging.debug('Redirecting to %s', next_page)
            return redirect(next_page)
        else:
            message = str.format("L'utilisateur [{}] n'existe pas.", username)
            flash(message, "Error")
            return render_template('auth/login.html', form=form)

    new_username = request.args.get('new_username')
    if new_username:
        form.username.data = new_username
        message = str.format("Utilisateur [{}] enregistré avec succès", new_username)
        flash(message, "Success")
        return render_template('auth/login.html', form=form)

    return render_template('auth/login.html', form=form)


@bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'GET':
        return render_template('auth/register.html', form=form)

    if form.validate_on_submit():
        username = request.form.get('username').lower()
        password = request.form.get('password')

        user = User.query.filter_by(username=username).one_or_none()
        if user:
            flash('User already exists', "Error")
            message = str.format('Username [{}] is already used', username)

            flash(message, "Error")
            return render_template('auth/register.html', form=form, username=username)
        else:
            u = User(username, password)
            u.player = Player()
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('.login', new_username=username))
    else:
        return render_template('auth/register.html', form=form)


@bp.route("/success")
@login_required
def success():
    new_connection = request.args.get('new_connection') != 'False'
    return render_template('auth/success.html', new_connection=new_connection)


@bp.route("/logout")
def logout():
    # On déconnecte l'utilisateur courant (s'il y en a un)
    logout_user()
    # Puis, on redirige vers la page de départ (qui redirigera ailleurs si nécessaire)
    return redirect(url_for('.login'))


@login_manager.unauthorized_handler
def unauthorized():
    logging.debug("User is not authenticated. Redirecting to login...")
    return redirect(url_for('auth.login'))


def get_next_page(request):
    # Récupérer la page ciblée par la requête
    next_page = request.args.get('next')
    # Vérifier si l'URL est sécurisée
    if next_page and not is_safe_url(next_page):
        # Sinon, retourner une erreur
        return abort(400)
    # Si oui, retourner la page
    return next_page


def is_safe_url(target):
    ref_url = urllib.parse.urlparse(request.host_url)
    test_url = urllib.parse.urlparse(urllib.parse.urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

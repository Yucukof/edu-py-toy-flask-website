import logging.config

from flask import (
    Blueprint, request, render_template, redirect, abort, url_for, jsonify, flash
)
from flask_login import login_required, current_user
from sqlalchemy import func, select
from werkzeug.exceptions import NotFound

from app import db
from forms.category import CategoryForm
from forms.clue import ClueForm
from forms.response import ResponseForm
from forms.riddle import RiddleForm
from models import get_engine, Category
from models.riddle import Riddle
from schemas.player import PlayerSchema
from schemas.riddle import RiddlePagination, RiddleSchema

bp = Blueprint('riddle', __name__, url_prefix='/riddle')

# Configure logging
logging.config.fileConfig('logging.cfg')

last_riddle = None
is_resolved = False


def fetch_riddle_by_random():
    connection = get_engine().connect()
    query = select(Riddle).order_by(func.random()).limit(1)
    riddle = connection.execute(query).one_or_none()
    logging.debug("Random riddle is %s", riddle)
    return riddle


def fetch_riddle_by_id(riddle_id):
    logging.debug("Retrieving ID %s", riddle_id)
    query = Riddle.query.filter(Riddle.id == riddle_id)
    if not current_user.is_admin:
        query = query.filter(User=current_user)
    return query.one_or_none()


def fetch_riddle_all():
    return Riddle.query.all()


def check_response(response, riddle):
    if response is None:
        pass
    if riddle is None:
        pass
    try:
        return riddle.solution == response
    except TypeError:
        return False


def handle_response(response, form):
    global last_riddle

    logging.debug("Handling response [%s]", response)
    status = check_response(response, last_riddle)

    if status is True:
        logging.debug("SUCCESS")
        global is_resolved
        is_resolved = True
        return redirect(url_for('.riddle_success'))
    else:
        logging.debug("FAILURE")
        return render_template('riddle/current.html', riddle=last_riddle, response=form)


@bp.route('<int:riddle_id>', methods=['GET', 'POST'])
@login_required
def riddle_by_id(riddle_id):
    global last_riddle, is_resolved
    form = ResponseForm()

    if not riddle_id:
        return redirect(bp.url_prefix + '/random')

    new_riddle = fetch_riddle_by_id(riddle_id)
    if new_riddle is None:
        return redirect(bp.url_prefix + '/random')
    last_riddle = new_riddle
    is_resolved = False

    response = None
    if request.method == 'GET':
        response = request.args.get("solution")
    if form.validate_on_submit():
        response = request.form.get("solution")

    if response:
        return handle_response(response, form)

    logging.debug("New riddle [%s]", new_riddle.name)
    form.id = riddle_id
    return render_template('riddle/current.html', riddle=new_riddle, response=form)


@bp.route('', methods=['GET', 'POST'])
@bp.route('random')
@login_required
def riddle_random():
    logging.debug("Page access")
    global last_riddle, is_resolved
    form = ResponseForm()

    if last_riddle is None:
        logging.info("Returning new random riddle...")
        new_riddle = fetch_riddle_by_random()
        form.id = new_riddle.id

        if new_riddle is None:
            abort(404)

        is_resolved = False
        last_riddle = new_riddle
        return redirect(bp.url_prefix + '/' + str(new_riddle.id))

    response = None
    if request.method == 'GET':
        response = request.args.get("solution")
    if request.method == 'POST':
        response = request.form.get('solution')

    if response is not None:
        return handle_response(response, form)
    else:
        logging.debug("No answer received, returning last riddle")
        return render_template('riddle/current.html', riddle=last_riddle, response=form)


@bp.route('success')
@login_required
def riddle_success():
    global last_riddle, is_resolved

    if is_resolved is not True:
        abort(404)

    resolved_riddle = last_riddle
    last_riddle = None
    form = RiddleForm()

    return render_template('riddle/success.html', resolved_riddle=resolved_riddle, riddle=None, form=form)


@bp.route('new', methods=['GET', 'POST'])
@login_required
def new_riddle():
    riddle_form = RiddleForm()
    clue_form = ClueForm()
    logging.debug("Generating new riddle")

    if riddle_form.validate_on_submit():
        logging.debug("Using request form from POST...")

        name = riddle_form.name.data
        riddle = riddle_form.riddle.data
        solution = riddle_form.solution.data
        difficulty = riddle_form.difficulty.data
        category = riddle_form.category.data
        explanation = riddle_form.explanation.data

        logging.debug("Inserting riddle...")

        new_riddle = Riddle(name=name,
                            riddle=riddle,
                            solution=solution,
                            category_id=category.id if category else None,
                            difficulty=difficulty,
                            explanation=explanation)
        new_riddle.category = category
        db.session.add(new_riddle)
        db.session.commit()

        logging.debug("Riddle inserted with ID %i", new_riddle.id)
        return redirect(url_for('.new_riddle', riddle=new_riddle.id))

    riddle_id = request.args.get("riddle")
    if riddle_id:
        riddle = Riddle.query.filter_by(id=riddle_id).one_or_none()
    else:
        riddle = None

    categories = Category.query.all()

    return render_template('riddle/new.html'
                           , riddle=riddle
                           , form=riddle_form
                           , clue_form=clue_form
                           , categories=categories
                           )


@bp.route('list', methods=['GET', 'POST'])
@login_required
def list_riddle():
    clue_form = ClueForm()
    category_form = CategoryForm()

    return render_template('riddle/list.html'
                           , current_user=current_user
                           , clue_form=clue_form
                           , category_form=category_form)


@bp.route('list-category', methods=['GET', 'POST'])
def list_riddle_by_category():
    current_user_id = current_user.get_id()
    category_id = request.args.get("category_id")
    page = request.args.get("page")
    page_number = int(page) if page else 1

    query = Riddle.query
    if not current_user.is_admin:
        query = query.filter_by(user_id=current_user_id)
    if category_id:
        category = Category.query \
            .filter_by(id=category_id) \
            .one_or_none()
        if category:
            query = query.filter_by(category=category)
        else:
            query = query.filter_by(category=None)

    schema = RiddlePagination()
    while page_number >= 1:
        try:
            query = query.order_by(Riddle.id) \
                .paginate(page_number, per_page=5)

            json = schema.dumps(query)
            return jsonify(json)

        except NotFound:
            page_number = page_number - 1


@bp.route('delete/<int:riddle_id>', methods=['GET', 'DELETE'])
@login_required
def delete_riddle_by_id(riddle_id):
    global last_riddle

    if riddle_id:
        logging.debug("Suppression de l'énigme [%s]", riddle_id)
        Riddle.query.filter_by(id=riddle_id).delete()

        if last_riddle and last_riddle.id == int(riddle_id):
            last_riddle = None

    return redirect(url_for('.riddle_random'))


@bp.route('delete', methods=['POST'])
@login_required
def delete_riddle():
    global last_riddle

    riddle_id = int(request.form.get("riddle_id"))

    return delete_riddle_by_id(riddle_id)


@bp.route('game-1', methods=['GET'])
def game_1():
    return render_template('riddle/game.html', response_form=ResponseForm())


@bp.route('game-2', methods=['GET'])
def game_2():
    if current_user.is_anonymous:
        return abort(403)
    if current_user.player.max_streak >= 3:
        return render_template('riddle/game2.html')
    flash("Thou are not ready!", "Error")
    return redirect(url_for(".game_1"))


@bp.route('json/<int:riddle_id>', methods=['GET'])
def fetch_json_riddle_by_id(riddle_id):
    riddle = fetch_riddle_by_id(riddle_id)
    schema = RiddleSchema()
    json = schema.dumps(riddle)
    return json


@bp.route('json/player', methods=['GET'])
def fetch_json_player():
    schema = PlayerSchema()
    if not current_user.is_anonymous:
        player = current_user.player
        json = schema.dumps(player)
        return json
    return jsonify("")


@bp.route('json/random', methods=['GET'])
def fetch_json_riddle_by_random():
    riddle_id = request.args.get('current_id')

    riddle = Riddle.query \
        .filter(Riddle.id != riddle_id) \
        .order_by(func.random()) \
        .limit(1) \
        .one_or_none()
    logging.debug("Random riddle is %s", riddle)

    if not current_user.is_anonymous:
        player = current_user.player
        player.total += 1
        if not player.last_riddle:
            player.failed += 1
            player.current_streak = 0
        player.last_riddle = False

    schema = RiddleSchema()
    return schema.dumps(riddle)


@bp.route('/update', methods=['POST'])
def update_difficulty():
    form = request.form
    riddle_id = form['riddle_id']
    increment = form['increment']

    riddle = fetch_riddle_by_id(riddle_id)
    if riddle:
        new_difficulty = riddle.difficulty + int(increment)
        if 1 <= new_difficulty <= 5:
            riddle.difficulty = new_difficulty

            return jsonify(success=True)

    return jsonify(success=False)


@bp.route('/submit', methods=['POST'])
def submit_response():
    response = ResponseForm(request.form)

    if response.validate_on_submit():
        riddle_id = response.id.data
        riddle = Riddle.query.filter(Riddle.id == riddle_id).one_or_none()

        if riddle:
            solution = response.value.data
            validation = check_response(solution, riddle)

            if not current_user.is_anonymous:
                player = current_user.player
                player.last_riddle = True

                if validation:
                    player.success += 1
                    current_streak = player.current_streak + 1
                    max_streak = player.max_streak

                    player.current_streak = current_streak
                    if current_streak > max_streak:
                        player.max_streak = current_streak
                else:
                    player.failed += 1
                    player.current_streak = 0

            return jsonify(validation)

    return jsonify(False)

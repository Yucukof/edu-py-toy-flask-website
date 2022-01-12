from flask import render_template, request, redirect, flash, abort
from flask_login import login_required, current_user

from app import db
from forms.clue import ClueForm
from models import Riddle, Clue
from riddle import bp


@bp.route('/<riddle_id>/clues', methods=['GET', 'POST'])
@login_required
def clues_by_riddle_id(riddle_id):
    # Step 1 - récupérer l'énigme
    riddle = Riddle.query.filter_by(id=riddle_id).one_or_none()
    # Step 2 - récupérer les indices
    clues = riddle.clues
    return render_template('clue/list.html', riddle=riddle, clues=clues, response=None)


@bp.route('/clues/add', methods=['POST'])
@login_required
def clues_add():
    riddle_id = request.form.get('riddle_id')
    if not riddle_id:
        abort(400, "Invalid request arguments")

    return add_clue(riddle_id=riddle_id)


@bp.route('/<riddle_id>/clues/add', methods=['GET', 'POST'])
@login_required
def add_clue(riddle_id):
    form = ClueForm()

    if form.validate_on_submit():
        # Step 1 - récupérer l'énigme
        riddle = Riddle.query.filter_by(id=riddle_id).one_or_none()
        if riddle:
            # Step 2 - Construire l'indice
            clue = Clue(text=form.text.data, riddle=riddle_id)
            db.session.add(clue)

    return redirect(request.referrer)


@bp.route('/clues/remove/', methods=['GET'])
@login_required
def clues_remove():
    riddle_id = request.args.get("riddle_id")
    number = request.args.get("number")

    if not (riddle_id and number):
        abort(400, "Invalid request arguments")

    return remove_clue(riddle_id=riddle_id, number=number)


@bp.route('/<int:riddle_id>/clues/remove/<int:number>', methods=['GET'])
@login_required
def remove_clue(riddle_id, number):
    riddle = Riddle.query \
        .filter_by(id=riddle_id) \
        .one_or_none()

    if riddle and (riddle.creator == current_user or current_user.is_admin):
        clues = riddle.clues
        if clues:
            # Step 2 - supprimer l'indice
            try:
                clue = clues[int(number) - 1]
                Clue.query.where(Clue.id == clue.id).delete()
            except TypeError:
                flash("Not a number")

    return redirect(request.referrer)

from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user, logout_user
from .models import User, Notes
from . import db
import json
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Notes(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template('home.html',user =current_user)


@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    db_note = Notes.query.get(noteId)
    if db_note:
        if db_note.user_id == current_user.id:
            db.session.delete(db_note)
            db.session.commit()
            return json.dumps('Note was deleted')
        


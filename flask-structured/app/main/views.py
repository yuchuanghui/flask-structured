from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User
from flask_login import login_required


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = NameForm()
    if form.validate_on_submit():
        username = User.query.filter_by(username=form.name.data).first()
        if username is None:
            user = User(username=form.name.data)
            # if app.config['FLASKY_ADMIN']:
            #     send_email(app.config['FLASKY_ADMIN'], 'New User')
            db.session.add(user)
            db.session.commit()
            session['name'] = form.name.data
            session['known'] = False

        else:
            session['known'] = True
            # form.name.data = ''
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form,
                           name=session.get('name'),
                           known=session.get('known', False),
                           current_time=datetime.utcnow())

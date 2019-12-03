from flask import render_template, redirect, url_for, Blueprint, request
from flask_login import current_user, login_user, logout_user, login_required
from models import User, Text, Activity
from forms import LoginForm, RegistrationForm, SpellCheckForm, HistoryForm, LogsForm
from database import db
import subprocess
import os
import re
from datetime import datetime

blue = Blueprint('blue', __name__)


@blue.route('/')
@blue.route('/index')
@login_required
def index():
    return render_template('index.html', title='AppSec - Assignments 2 and 3')


@blue.route('/login', methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #    return redirect(url_for('blue.spell_check'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data, form.phone.data):
            return render_template('login.html', title='Log In', form=form, connection_status='Incorrect')
        login_user(user, remember=form.remember_me.data)
        activity = Activity(user_id=user.id)
        db.session.add(activity)
        db.session.commit()
        return render_template('login.html', title='Log In', form=form, connection_status='Success')
    return render_template('login.html', title='Log In', form=form)


@blue.route('/logout')
def logout():
    user = User.query.filter_by(username=current_user.username).first()
    activity = Activity.query.filter_by(user_id=user.id).order_by(Activity.id.desc()).first()
    activity.log_out = datetime.utcnow()
    db.session.commit()
    logout_user()
    return redirect(url_for('blue.login'))


@blue.route('/register', methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #    return redirect(url_for('blue.spell_check'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, phone=form.phone.data)
        if User.query.filter_by(username=form.username.data).first() is not None:
            return render_template('register.html', title='Register', form=form, registration_status='Failure')
        user.set_password(form.password.data, form.phone.data)
        db.session.add(user)
        db.session.commit()
        return render_template('register.html', title='Register', form=form, registration_status='Success')
    return render_template('register.html', title='Register', form=form)


@blue.route('/spell_check', methods=['GET', 'POST'])
@login_required
def spell_check():
    form = SpellCheckForm()
    if form.validate_on_submit() and request.method == 'POST':
        file = open("input.txt", "w")
        file.write(form.text_to_check.data)
        file.close()
        command = ["./spell_check", "input.txt", "wordlist.txt"]
        sub = subprocess.Popen(command, stdout=subprocess.PIPE)
        misspelled = sub.communicate()[0].decode("utf-8").replace("\n", ", ")[:-2]
        os.remove("input.txt")
        supplied_text = form.text_to_check.data
        form.text_to_check.data = ""

        # Requirements for assignment 3
        # Adding submitted text to database
        user = User.query.filter_by(username=current_user.username).first()
        text = Text(before_spellcheck=supplied_text, after_spellcheck=misspelled, user_id=user.id)
        db.session.add(text)
        db.session.commit()
        return render_template('spell_check.html', title='Spell Check', form=form, input=supplied_text, output=misspelled)
    else:
        return render_template('spell_check.html', title='Spell Check', form=form)


@blue.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    user = User.query.filter_by(username=current_user.username).first()
    form = HistoryForm()
    if user.username == 'admin':
        if form.validate_on_submit() and request.method == 'POST':
            requested_user = User.query.filter_by(username=form.username.data).first()
            text_history = requested_user.texts.all()
            return render_template('history.html', title='History', form=form, total_queries=len(text_history), user=requested_user, texts=text_history)
        else:
            return render_template('history.html', title='History', form=form)
    else:
        text_history = user.texts.all()
        return render_template('history.html', title='History', form=form, total_queries=len(text_history), user=user, texts=text_history)


@blue.route('/history/<query_id>', methods=['GET'])
@login_required
def history_query(query_id):
    user = User.query.filter_by(username=current_user.username).first()
    current_text_id = re.findall('\d+', query_id)
    if user.username == 'admin':
        current_text = Text.query.filter_by(id=current_text_id[0]).first()
    else:
        current_text = Text.query.filter_by(id=current_text_id[0], user_id=user.id).first()

    if current_text is None:
        return redirect(url_for('blue.history'))
    else:
        return render_template('query.html', title='Query', user=user, text=current_text)


@blue.route('/login_history', methods=['GET', 'POST'])
@login_required
def login_history():
    if current_user.username == 'admin':
        form = LogsForm()
        if form.validate_on_submit() and request.method == 'POST':
            requested_user = User.query.filter_by(username=form.username.data).first()
            logs_history = requested_user.activities.all()
            return render_template('login_history.html', title='Login History', form=form, user=requested_user, activities=logs_history)
        else:
            return render_template('login_history.html', title='Login History', form=form)
    else:
        return render_template('index.html', title='AppSec - Assignments 2 and 3')

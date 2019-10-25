from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_login import current_user, login_user, logout_user, login_required
from models import User
from forms import LoginForm, RegistrationForm, SpellCheckForm
from database import db
import subprocess
import os

blue = Blueprint('blue', __name__)


@blue.route('/')
@blue.route('/index')
@login_required
def index():
    return render_template('index.html', title='AppSec - Assignment 2')


@blue.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blue.spell_check'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data, form.phone.data):
            return render_template('login.html', title='Log In', form=form, connection_status='Incorrect')
        login_user(user, remember=form.remember_me.data)
        return render_template('login.html', title='Log In', form=form, connection_status='Success')
    return render_template('login.html', title='Log In', form=form)


@blue.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('blue.index'))


@blue.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('blue.spell_check'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, phone=form.phone.data)
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
        misspelled = sub.communicate()[0].replace("\n", ", ")[:-2]
        os.remove("input.txt")
        supplied_text = form.text_to_check.data
        form.text_to_check.data = ""
        return render_template('spell_check.html', title='Spell Check', form=form, input=supplied_text, output=misspelled)
    else:
        return render_template('spell_check.html', title='Spell Check', form=form)

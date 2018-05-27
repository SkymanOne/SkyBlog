from app import app
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user
from werkzeug.urls import url_parse
from app.models import User
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='My Blog', name='German', text='# Hello')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid data')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).decode_netloc() != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)


# TODO: create admin a panel's route

@app.route('/links')
def links():
    return 'links'


@app.route('/topics')
def topics():
    return 'topics'


@app.route('/about')
def about():
    return 'about'

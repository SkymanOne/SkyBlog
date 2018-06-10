from app import app, db
from app.models import *
from flask import render_template, flash, redirect, url_for, request, json, jsonify
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.urls import url_parse
from app.models import User
from app.forms import *
from app.db_acces import *


@app.route('/')
@app.route('/index')
def index():
    # TODO: create getting certain count of posts
    posts_list = Post.query.select_from().order_by(-Post.id).limit(10)
    text = posts_list[0].body
    return render_template('index.html', text=text)


@app.route('/<int:count>', methods=['POST'])
def get_more_posts(count):

    return jsonify(count)


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


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def write_new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        post = create_new_post(form.title.data, form.short.data, form.content.data, datetime.utcnow(),
                               User.query.get(1))
        if post is not None:
            for t in separate_topics(form.topics.data):
                topic = create_or_get_topic(t)
                topic.posts.append(post)
            db.session.commit()
            return "Success!"
        else:
            flash('Error of creating')
            return render_template('new_post.html', form=form)

    return render_template('new_post.html', form=form)


@app.route('/links')
def links():
    return 'links'


@app.route('/topics')
def topics():
    return 'topics'


@app.route('/topics/<topic_name>')
def info_of_topic(topic_name):
    return 'some {}'.format(topic_name)


@app.route('/about')
def about():
    return 'about'


def separate_topics(string):
    list_of_topics = string.split(' ')
    return list_of_topics

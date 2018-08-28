from app import app, db
from app.models import *
from flask import render_template, flash, redirect, url_for, request, json, jsonify
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.urls import url_parse
from app.models import User
from app.forms import *
from app.db_acces import *

post_schema = PostSchema(many=True)


@app.route('/')
@app.route('/index')
def index():
    posts_list = Post.query.order_by(-Post.id).limit(10)
    try:
        text = posts_list[0].body
    except IndexError:
        text = ''
    return render_template('index.html', posts=posts_list)


@app.route('/<int:count>', methods=['POST', 'GET'])
def get_more_posts(count):
    list_of_posts = Post.query.filter(Post.id > count).limit(5)
    return jsonify({'posts': post_schema.dump(list_of_posts).data})


@app.route('/<string:title>', methods=['GET'])
def post_page(title):
    post = get_post(title)
    if post is not None:
        return render_template('post.html', title=post.title, short=post.short,
                               content=post.body)
    else:
        return "404"


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
            return redirect('/success')
        else:
            flash('Error of creating')
            return render_template('new_post.html', form=form)
    else:
        return render_template('new_post.html', form=form)


@app.route('/success')
def success():
    result_title = 'Success!'
    result_text = 'Your post was created successful'
    return render_template('result.html', result_title=result_title, result_text=result_text)


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

from app import app, db
from app.models import *
from flask import render_template, flash, redirect, url_for, request, json, jsonify
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.urls import url_parse
from app.models import User
from sqlalchemy import desc
from app.forms import *
from app.db_acces import *

post_schema = PostSchema(many=True)
# TODO: make 404 page


@app.route('/')
@app.route('/index')
def index():
    count_of_posts = Post.query.count()
    if count_of_posts < 3:
        redirect(url_for('write_new_post'))
    posts_list = Post.query.order_by(-Post.id).limit(3)
    return render_template('index.html', posts=posts_list)


@app.route('/api/<int:count>', methods=['GET', 'POST'])
def get_more_posts(count):
    count_of_rows = Post.query.filter(Post.id).count()
    filter_number = count_of_rows - (count - 5 + 3)
    list_of_posts = Post.query.filter(Post.id < filter_number).order_by(desc(Post.id)).limit(4)
    return jsonify({'posts': post_schema.dump(list_of_posts).data})


@app.route('/<path:url>', methods=['GET'])
def post_page(url):
    post = get_post(url)
    if post is not None:
        return render_template('post.html', title=post.title, short=post.short,
                               content=post.body, time=post.time.date(), url=post.url)
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
    form = PostForm()
    if form.validate_on_submit():
        post = create_new_post(form.title.data, form.short.data, form.body.data, datetime.utcnow(),
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


@app.route('/edit/<string:url>', methods=['GET'])
@login_required
def get_edit_post(url):
    post = get_post(url)
    if post is not None:
        form = PostForm(obj=post)
        old_url = post.url
        post_topics_list = list()
        for t in post.topics:
            post_topics_list.append(t.name)
        form.topics.data = ' '.join(post_topics_list)
        db.session.commit()
        return render_template('edit.html', form=form)
    else:
        return "404"


@app.route('/edit/<string:url>', methods=['POST'])
@login_required
def post_edit_post(url):
    form = PostForm()
    post = get_post(url)
    old_url = post.url
    if form.validate_on_submit():
        edit_post_data(old_url, form.title.data, form.short.data, form.body.data)
        for t in separate_topics(form.topics.data):
            topic = create_or_get_topic(t)
            topic.posts.append(post)
        db.session.commit()
        return redirect('/success')
    return render_template('edit.html', form=form)


@app.route('/delete/<string:url>', methods=['GET'])
@login_required
def delete_post(url):
    post = get_post(url)
    if post is not None:
        form = DeleteForm()
        return render_template('delete.html', form=form, name=post.title)
    else:
        return '404'


@app.route('/delete/<string:url>', methods=['POST'])
@login_required
def post_delete_post(url):
    form = DeleteForm()
    if form.validate_on_submit():
        post = get_post(url)
        title = post.title
        if title == form.confirmation.data:
            result = delete_post_from_db(post.url)
            db.session.commit()
            if result:
                result_title = 'Done!'
                result_text = 'The post is successfully deleted'
            else:
                result_text = 'Fail!'
                result_text = 'Something happend wrong'
            return render_template('result.html', result_title=result_title, result_text=result_text)
    return render_template('delete.html', form=form, name=post.title)


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


# Help methods


def separate_topics(string):
    list_of_topics = string.split(' ')
    return list_of_topics

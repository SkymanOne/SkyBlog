from app.models import *
from app import db


def adapt_url(text):
    for ch in ['\\', '`', '*', '{', '}', '[', ']', '(', ')', '>', '#', '+', '-', '.', '!', '?', '$', ' ', '\'', '@']:
            text = text.replace(ch, '_')
    return text


def create_new_post(title, short, body, time, author):
    try:
        url = adapt_url(title)
        new_post = Post(title=title, url=url, short=short, body=body,
                        time=time, author=author)
        db.session.add(new_post)
        db.session.commit()
    except:
        return False
    return new_post


def edit_post_data(url, title, short, body):
    post = get_post(url)
    if post is not None:
        post.title = title
        post.url = adapt_url(title)
        post.short = short
        post.body = body
        for t in post.topics:
            post.topics.remove(t)
        db.session.commit()
        return post
    else:
        return None


def delete_post_from_db(url):
    post = get_post(url)
    if post is not None:
        post.topics = []
        db.session.delete(post)
        db.session.commit()
        return True
    else:
        return False


def get_topic(name):
    return Topic.query.filter_by(name=name).first()


def get_list_of_topics():
    return Topic.query.order_by()


def get_list_of_topics_by_search(data):
    return Topic.query.filter(Topic.name.startswith(data)).all()


def get_list_of_posts_by_search(data):
    return Post.query.filter(Post.title.startswith(data)).all()


def create_or_get_topic(name):
    topic = get_topic(name)
    if topic is None:
        topic = Topic(name=name)
        db.session.add(topic)
        db.session.commit()
    return topic


def get_post(url):
    return Post.query.filter_by(url=url).first()


def get_list_of_posts(topic):
    return topic.posts

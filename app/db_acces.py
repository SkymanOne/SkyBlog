from app.models import *
from app import db


def create_new_post(title, short, body, time, author):
    try:
        new_post = Post(title=title, short=short, body=body,
                        time=time, author=author)
        db.session.add(new_post)
        db.session.commit()
    except:
        return False
    return new_post


def get_topic(name):
    try:
        topic = Topic.query.filter_by(name=name).first_or_404()
    except exceptions.NotFound:
        return None
    else:
        return topic


def create_or_get_topic(name):
    topic = get_topic(name)
    if topic is None:
        topic = Topic(name=name)
        db.session.add(topic)
        db.session.commit()
    return topic

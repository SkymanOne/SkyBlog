from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from app import login
from app import ma


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    login = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author')

    def set_password(self, pas):
        self.password_hash = generate_password_hash(pas)

    def check_password(self, pas):
        return check_password_hash(self.password_hash, pas)

    def __repr__(self):
        return '<User {}>'.format(self.login)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


post_topic = db.Table('post_topic',
                      db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                      db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'))
                      )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, unique=True)
    url = db.Column(db.String(220), unique=True)
    short = db.Column(db.String(300))
    body = db.Column(db.Text())
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    topics = db.relationship('Topic', secondary=post_topic, backref='posts', lazy='dynamic')


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class TopicSchema(ma.ModelSchema):
    class Meta:
        model = Topic


class PostSchema(ma.ModelSchema):
    topics = ma.Nested(TopicSchema, many=True)

    class Meta:
        model = Post

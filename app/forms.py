from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms import validators


class LoginForm(FlaskForm):
    login = StringField('Login', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.Length(min=6, max=35)])
    remember_me = BooleanField('Remember me', default=False)
    submit = SubmitField('Sign In')


class NewPostForm(FlaskForm):
    title = StringField('Title', [validators.required()])
    short = StringField('Short description')
    content = StringField('Content', [validators.required()])
    topics = StringField('Topics')
    submit = SubmitField('Publish')

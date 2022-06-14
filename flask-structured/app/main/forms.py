from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField

class NameForm(FlaskForm):
    name = StringField('What is your name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    body = PageDownField("'What's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    body = PageDownField("What do you want to say?", validators=[DataRequired()])
    submit = SubmitField('Submit')

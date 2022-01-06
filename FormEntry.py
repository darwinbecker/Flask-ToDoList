
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea, TextInput
from wtforms import StringField


# form fields
class FormItem(FlaskForm):
    id = StringField("id", widget=TextInput())
    title = StringField("title", widget=TextInput(), validators=[DataRequired()])
    text = StringField("text", widget=TextArea())
    due = StringField("due", widget=TextInput())
    search = StringField("search", widget=TextInput())


class AddEntryForm(FlaskForm):
    title = StringField("title", widget=TextInput(), validators=[DataRequired()])
    text = StringField("text", widget=TextArea())
    due = StringField("due", widget=TextInput())


class DeleteEntryForm(FlaskForm):
    id = StringField("id", widget=TextInput(), validators=[DataRequired()])


class SearchEntryForm(FlaskForm):
    search = StringField("search", widget=TextInput(), validators=[DataRequired()])
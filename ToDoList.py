#flask web-app by Rey Alite & Darwin Becker

from flask import Flask, render_template, redirect, request, g
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea, TextInput, CheckboxInput
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# database
engine = create_engine("sqlite:///:memory:", echo=True)
Base = declarative_base()


# table: items
# stores all new entries
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    text = Column(String(500))
    due = Column(String(10))

    def __repr__(self):
        return "<Item(title='%s', text='%s', due='%s" % (
            self.title, self.text, self.due)


# table: doneItems
# stores all finished entries
class DoneItem(Base):
    __tablename__ = "doneItems"

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    text = Column(String(500))
    due = Column(String(10))

    def __repr__(self):
        return "<Item(title='%s', text='%s', due='%s" % (
            self.title, self.text, self.due)


# Base.metadata.create_all(engine)

def get_db():
    if not hasattr(g, "sqlite_db"):
        con = sqlite3.connect("ToDo-Database.db")
        g.sqlite_db = con
    return g.sqlite_db


# form fields
class AddEntryForm(FlaskForm):
    title = StringField("title", widget=TextInput(), validators=[DataRequired()])
    text = StringField("text", widget=TextArea())
    due = StringField("due", widget=TextInput())
    search = StringField("search", widget=TextInput())


class DeleteEntryForm(FlaskForm):
    id = StringField("id", widget=TextInput(), validators=[DataRequired()])


class SearchEntryForm(FlaskForm):
    search = StringField("search", widget=TextInput(), validators=[DataRequired()])


# flask app
app = Flask(__name__, static_url_path="/static")
app.secret_key = 'auth Key'  # not being used yet
db_search = []

# homepage
# shows all active entries and all finished entries
@app.route("/", methods=["GET", "POST"])
def say_hello():
    form = AddEntryForm()
    search = form.search.data

    # connect to database
    con = get_db()
    cur = con.cursor()

    # database -> displays all new entries
    cur.execute('select * from items')
    db_entries = [{
        "id": row[0],
        "title": row[1],
        "text": row[2],
        "due": row[3]
    } for row in cur.fetchall()]

    con.commit()

    # database -> displays all finished entries
    cur.execute('select * from doneItems')
    db_done = [{
        "id": row[0],
        "title": row[1],
        "text": row[2],
        "due": row[3]
    } for row in cur.fetchall()]

    con.commit()

    # database -> being able to search an entry by its title or by its due
    cur.execute('select * from items where UPPER(title) LIKE UPPER(?) or UPPER(due) LIKE UPPER(?)', (search, search))
    db_search = [{
        "id": row[0],
        "title": row[1],
        "text": row[2],
        "due": row[3]
    } for row in cur.fetchall()]

    con.commit()

    # index.html is the mainpage
    # the mainpage displays everything, there is just 1 HTML-file
    return render_template("index.html", entries=db_entries, done=db_done, search=db_search, form=form)


# adds form input into the database
@app.route("/add", methods=["POST"])
def add_entry():
    form = AddEntryForm()
    title = form.title.data
    text = form.text.data
    due = form.due.data

    con = get_db()
    cur = con.cursor()
    cur.execute('insert into items(title, text, due) values (?, ?, ?)', (title, text, due))
    con.commit()

    return redirect("/")


# deletes a new/unfinished entry in the database
@app.route("/delete", methods=["POST"])
def delete():
    form = DeleteEntryForm()
    id = form.id.data

    con = get_db()
    cur = con.cursor()
    cur.execute('delete from items where (id = ?)', (id,))

    con.commit()

    return redirect("/")


# deletes an finished entry in the database
@app.route("/deleteDone", methods=["POST"])
def delete_done():
    form = DeleteEntryForm()
    id = form.id.data

    con = get_db()
    cur = con.cursor()
    cur.execute('delete from doneItems where (id = ?)', (id))

    con.commit()

    return redirect("/")


# being able to set the state of an entry to 'finished'
@app.route("/done", methods=["POST"])
def done_entry():
    form = DeleteEntryForm()
    id = form.id.data

    con = get_db()
    cur = con.cursor()
    cur.execute(
        'insert into doneItems(title, text, due) select items.title, items.text, items.due from items where items.id = ?',
        (id,))

    con.commit()
    delete()

    return redirect("/")


# being able to set the state of an entry to 'new'
@app.route("/undone", methods=["POST"])
def undone_entry():
    form = DeleteEntryForm()
    id = form.id.data

    con = get_db()
    cur = con.cursor()
    cur.execute(
        'insert into items(title, text, due) select doneItems.title, doneItems.text, doneItems.due from doneItems where doneItems.id = ?',
        (id))

    con.commit()
    delete_done()

    return redirect("/")


# testing route for debugging
@app.route("/test", methods=["POST"])
def test():
    con = get_db()
    cur = con.cursor()
    cur.execute('select * from items')
    db_done = [{
        "id": row[0],
        "title": row[1],
        "text": row[2],
        "due": row[3]
    } for row in cur.fetchall()]
    con.commit()

    print(db_done)

    return redirect("/")


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "sqlite_db"): g.sqlite_db.close()


#app.run(debug=True)

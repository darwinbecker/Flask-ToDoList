#flask web-app by Rey Alite & Darwin Becker

from flask import Flask, render_template, redirect, g

from FormEntry import FormItem, AddEntryForm, DeleteEntryForm, SearchEntryForm
from Database import get_db

# flask app
app = Flask(__name__, static_url_path="/static")
app.secret_key = 'auth Key'  # not being used yet

# homepage
# shows all active entries and all finished entries
@app.route("/", methods=["GET", "POST"])
def say_hello():
    # connect to database
    con = get_db()
    cur = con.cursor()

    # database -> displays all new entries
    cur.execute('select * from items')
    db_entries = [{
        "id": row[0],
        "title": row[1],
        "text": row[2],
        "due": row[3],
        "done": row[4]
    } for row in cur.fetchall()]
    con.commit()

    search = FormItem().search.data
    db_search = []
    db_done = []
    db_todo = []
    for entry in db_entries:
        if not search is None:
            if search.lower() in entry["title"].lower() or search.lower() in entry["due"].lower():
                db_search.append(entry)

        if entry["done"] == 1:
            db_done.append(entry)
        else:
            db_todo.append(entry)

    # index.html is the mainpage
    # the mainpage displays everything, there is just 1 HTML-file
    return render_template("index.html", todo=db_todo, done=db_done, search=db_search, form=FormItem())



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
def delete_entry():
    form = DeleteEntryForm()
    item_id = form.id.data

    con = get_db()
    cur = con.cursor()
    cur.execute('delete from items where (id = ?)', item_id)

    con.commit()

    return redirect("/")


# find an entry in the database
@app.route("/search", methods=["POST"])
def search_entry():
    form = SearchEntryForm()
    search = form.search.data

    con = get_db()
    cur = con.cursor()
    cur.execute('select * from items where UPPER(title) LIKE UPPER(?) or UPPER(due) LIKE UPPER(?)', (search, search))

    con.commit()

    return redirect("/")


# deletes an finished entry in the database
@app.route("/deleteDone", methods=["POST"])
def delete_done():
    form = DeleteEntryForm()
    item_id = form.id.data

    con = get_db()
    cur = con.cursor()
    cur.execute('delete from items where (id = ?)', item_id)

    con.commit()

    return redirect("/")


# being able to set the state of an entry to 'finished'
@app.route("/done", methods=["POST"])
def done_entry():
    form = DeleteEntryForm()
    item_id = form.id.data

    con = get_db()
    cur = con.cursor()
    cur.execute('update items set done = true where items.id = ?', item_id)

    con.commit()

    return redirect("/")


# being able to set the state of an entry to 'new'
@app.route("/undone", methods=["POST"])
def undone_entry():
    form = DeleteEntryForm()
    item_id = form.id.data

    con = get_db()
    cur = con.cursor()
    cur.execute('update items set done = false where items.id = ?', item_id)
    con.commit()

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

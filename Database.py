import sqlite3
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from flask import g

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
    done = Column(Integer, default=False)

    def __repr__(self):
        return "<Item(title='%s', text='%s', due='%s" % (
            self.title, self.text, self.due)


def get_db():
    if not hasattr(g, "sqlite_db"):
        con = sqlite3.connect("ToDo-Database.db")
        g.sqlite_db = con
    return g.sqlite_db

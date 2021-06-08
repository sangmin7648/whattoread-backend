from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()


class User(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)


class BookShelf(db.Model):
    user_id = db.Column(db.String, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    book_id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(100), nullable=False)


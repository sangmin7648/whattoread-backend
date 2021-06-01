from flask import Flask

from model import *
from service import UserService, BookshelfService
from view import create_endpoints

import config


class Services:
    pass


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    # Persistence Layer
    user_dao = UserDAO(User, db)
    bookshelf_dao = BookshelfDAO(BookShelf, db)

    # Business Layer
    services = Services
    services.user_service = UserService(user_dao)
    services.bookshelf_service = BookshelfService(bookshelf_dao)

    # Presentation Layer
    create_endpoints(app, services)

    return app

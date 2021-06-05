from flask import Flask
from elasticsearch import Elasticsearch
from flask_cors import CORS

from model import *
from service import UserService, BookshelfService, ElasticsearchService
from view import create_endpoints

import config


class Services:
    pass


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    es = Elasticsearch('localhost:9200')

    # Persistence Layer
    user_dao = UserDAO(User, db)
    bookshelf_dao = BookshelfDAO(BookShelf, db)
    elasticsearch_dao = ElasticsearchDAO(es)

    # Business Layer
    services = Services
    services.user_service = UserService(user_dao)
    services.bookshelf_service = BookshelfService(bookshelf_dao)
    services.elasticsearch_service = ElasticsearchService(elasticsearch_dao)

    # Presentation Layer
    create_endpoints(app, services)

    return app

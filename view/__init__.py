import jwt
from flask import request, jsonify, Response, g
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get('Authorization')
        if not access_token: return Response(status=401)
        try:
            payload = jwt.decode(access_token, "dev", 'HS256')
        except jwt.InvalidTokenError:
            payload = None
        if payload is None: return Response(status=401)
        user_id = payload['user_id']
        g.user_id = user_id
        return f(*args, **kwargs)
    return decorated_function


def create_endpoints(app, services, nlp_model):
    user_service = services.user_service
    bookshelf_service = services.bookshelf_service
    elasticsearch_service = services.elasticsearch_service

    @app.route("/ping", methods=['GET'])
    def ping():
        return "pong"

    @app.route("/search", methods=['GET'])
    def search():
        user_input = request.args.get('user_input')
        processed_input_list = nlp_model(user_input)
        result = elasticsearch_service.search(processed_input_list)
        return result

    @app.route("/book_detail/<int:book_id>", methods=['GET'])
    def book_detail(book_id):
        result = elasticsearch_service.get_book_by_id(book_id)
        return result

    @app.route("/signup", methods=['POST'])
    def signup():
        new_user = request.json
        result = user_service.create_new_user(new_user)
        return result

    @app.route("/login", methods=['POST'])
    def login():
        credential = request.json
        authorized = user_service.login(credential)
        if not authorized:
            return '', 401
        user_id = credential['id']
        token = user_service.generate_access_token(user_id)
        return jsonify({
            'user_id': user_id,
            'access_token': token
        })

    @app.route("/bookshelf", methods=['POST', 'DELETE', 'GET'])
    @login_required
    def bookshelf():
        user_id = g.user_id
        if request.method == 'POST':
            book_id = request.json['book_id']
            result = bookshelf_service.put_to_bookshelf(user_id, book_id)
            return result
        if request.method == 'DELETE':
            book_id = request.json['book_id']
            result = bookshelf_service.delete_from_bookshelf(user_id, book_id)
            return result
        return jsonify(bookshelf_service.get_bookshelf(user_id))


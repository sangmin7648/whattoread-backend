class UserDAO:
    def __init__(self, model, db):
        self.model = model
        self.db = db

    def get_user(self, user_id):
        return self.model.query.filter_by(id=user_id).first()

    def insert_user(self, new_user):
        id = new_user['id']
        name = new_user['name']
        password = new_user['password']
        email = new_user['email']
        user = self.model(id=id, name=name, password=password, email=email)
        self.db.session.add(user)
        self.db.session.commit()

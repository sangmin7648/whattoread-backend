from datetime import datetime, timedelta
import jwt


class UserService:
    def __init__(self, user_dao):
        self.user_dao = user_dao

    def create_new_user(self, new_user):
        id = new_user['id']
        user = self.user_dao.get_user(id)
        if user is not None:
            return "이미 사용자가 존재합니다", 409
        self.user_dao.insert_user(new_user)
        return "사용자를 생성했습니다", 200

    def login(self, credential):
        id = credential['id']
        password = credential['password']
        user = self.user_dao.get_user(id)
        authorized = user and password == user.password
        return authorized

    def generate_access_token(self, user_id):
        sec_in_day = 60*60*24
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=sec_in_day)
        }
        token = jwt.encode(payload, "dev", 'HS256')
        return token

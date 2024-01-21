# app/models.py
from flask_pymongo import PyMongo
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

mongo = PyMongo()


class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        return mongo.db.users.find_one({'username': username})

    @classmethod
    def find_by_id(cls, user_id):
        return mongo.db.users.find_one({'_id': user_id})

    @classmethod
    def create_user(cls, username, password):
        # hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        hashed_password = generate_password_hash(password)
        user_id = mongo.db.users.insert({'username': username, 'password': hashed_password})
        return cls(username, hashed_password, user_id)

# app/models.py
from flask import Flask
from flask_pymongo import PyMongo
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


app = Flask(__name__, template_folder="template/")
app.config.update(
    MONGO_URI='mongodb://localhost:27017/flask',
    MONGO_USERNAME='',
    MONGO_PASSWORD='',
    # MONGO_DBNAME='user'
)
app.debug = True
mongo = PyMongo(app)


class User(UserMixin):
    def __init__(self, user_id, username, password, email):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email

    @classmethod
    def find_by_username(cls, username):
        return mongo.db.users.find_one({'username': username})

    @classmethod
    def find_by_id(cls, user_id):
        return mongo.db.users.find_one({'_id': user_id})

    @classmethod
    def create_user(cls, username, password, email):
        # hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        hashed_password = generate_password_hash(password)
        user_id = mongo.db.users.insert({
            'username': username, 'password': hashed_password, 'email': email
        })
        return User(user_id, username, hashed_password, email)

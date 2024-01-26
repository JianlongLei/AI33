from flask import Flask
from pymongo import MongoClient

from dao_model import User

# connect to mongodb
app = Flask(__name__)
app.debug = True
client = MongoClient('mongodb://localhost:27017/')
db = client['flask']

# post_collection = db['post']


class UserDAO:
    @staticmethod
    def create_user(username, email, password):
        user = User(username=username, email=email, password=password)
        user.save()

    @staticmethod
    def get_user_by_email(email):
        user = User.objects(email=email).first()
        return user

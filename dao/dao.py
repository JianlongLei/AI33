from flask import Flask
from pymongo import MongoClient
from bson import ObjectId

from dao_model import User

# connect to mongodb
app = Flask(__name__)
app.debug = True
client = MongoClient('mongodb://localhost:27017/')
db = client['flask']


class UserDao:
    @staticmethod
    def create_user(name, psw, descr):
        # prevent repeated username
        cursor = UserDao.find_user_by_name(name)
        size = len(list(cursor))
        if size > 0:
            return False

        user = {'name': name, 'password': psw, 'description': descr}
        result = db['user'].insert_one(user)
        return result.acknowledged

    @staticmethod
    def find_user(oid: ObjectId):
        result = db['user'].find_one({'_id': oid})
        oid = result['_id']
        # print(isinstance(oid, str))
        # print(oid.generation_time)
        # print(str(oid))
        user = User(user_id=str(oid), name=result['name'], psw=result['password'], description=result['description'])
        return user

    @staticmethod
    def find_user_by_name(username: str):
        query = db['user'].find({'name': username})
        return query

# class PostDao:

from flask import Flask
from pymongo import MongoClient
from bson import ObjectId
from gridfs import GridFS

from dao_model import *

# connect to mongodb
app = Flask(__name__)
app.debug = True
client = MongoClient('mongodb://localhost:27017/')
db = client['flask']
fs = GridFS(db, collection='image')


class UserDao:
    @staticmethod
    def create_user(name, psw, descr):
        # prevent repeated username
        cursor = UserDao.find_users_by_name(name)
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
        user = User(user_id=str(oid), name=result['name'], psw=result['password'], description=result['description'])
        return user

    @staticmethod
    def find_users_by_name(username: str):
        query = db['user'].find({'name': username})
        return query

    @staticmethod
    def delete_user_by_id(oid: ObjectId):
        result = db['user'].delete_one({'_id': oid})
        return result

    @staticmethod
    def delete_user_by_name(name: str):
        result = db['user'].delete_one({'name': name})
        return result


class PostDao:
    @staticmethod
    def create_post(uid, content):
        post = {'user': uid, 'content': content}
        result = db['post'].insert_one(post)
        return result.acknowledged

    @staticmethod
    def find_posts_by_uid(uid: str):
        query = db['post'].find({'user': uid})
        posts = []
        for result in query:
            # parse post
            oid = result['_id']
            uid = result['user_id']
            content = result['content']
            posts.append(Post(post_id=str(oid), user_id=uid, content=content, created_date=oid.generation_time))
        return posts

    @staticmethod
    def find_post(oid: ObjectId):
        result = db['post'].find_one({'_id': oid})
        oid = result['_id']
        uid = result['user_id']
        content = result['content']
        post = Post(post_id=str(oid), user_id=uid, content=content, created_date=oid.generation_time)
        return post

    @staticmethod
    def delete_post(oid: ObjectId):
        result = db['post'].delete_one({'_id': oid})
        return result


class ImageDao:
    @staticmethod
    def create_image(image_name: str, image_data):
        image = {'name': image_name, 'data': image_data}
        result = db['post'].insert_one(image)
        return result.acknowledged

    @staticmethod
    def find_image(oid: ObjectId):
        result = db['image'].find_one({'_id': oid})
        oid = result['_id']
        name = result['name']
        base64_data = result['data']
        image = Image(image_id=str(oid), name=name, data=base64_data)
        return image

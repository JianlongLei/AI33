import os
import time

from bson import ObjectId
from pymongo.cursor import Cursor
from pymongo.results import InsertOneResult
from motor.motor_asyncio import AsyncIOMotorClient

from dao_model import *
from server.const import Constant

# connect to mongodb

client = AsyncIOMotorClient(
    Constant.app_settings.get('mongodb_url'),
    username=Constant.app_settings.get('db_username'),
    password=Constant.app_settings.get('db_password'),
    uuidRepresentation="standard",
)
db = client.college
fs = db.get_collection('image')


class UserDao:
    @staticmethod
    def create_user(name, psw, email):
        # prevent repeated username
        cursor = UserDao.find_users_by_name(name)
        size = len(list(cursor))
        if size > 0:
            return InsertOneResult(inserted_id=None, acknowledged=False)

        user = {'name': name, 'password': psw, 'email': email}
        result = db['user'].insert_one(user)
        return result

    @staticmethod
    def find_user(oid: ObjectId):
        result = db['user'].find_one({'_id': oid})
        if result is None:
            return None

        oid = result['_id']
        user = User(user_id=str(oid), name=result['name'], psw=result['password'], description=result['description'])
        return user

    @staticmethod
    def find_users_by_name(username: str):
        query = db['user'].find({'name': username})
        users = []
        for result in query:
            # parse user
            oid = result['_id']
            name = result['name']
            psw = result['password']
            descr = result['email']
            users.append(User(user_id=str(oid), name=name, psw=psw, description=descr))

        return users

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
    def create_post(uid, content, img_url):
        oid = ObjectId(uid)
        user = UserDao.find_user(oid)
        if user is None:
            return InsertOneResult(inserted_id=None, acknowledged=False)

        post = {'user': uid, 'content': content, 'created_date': time.time(), 'img_url': img_url}
        result = db['post'].insert_one(post)
        return result

    @staticmethod
    def find_posts_by_uid(uid: str):
        query = db['post'].find({'user': uid})
        posts = PostDao.parse_post_query(query)
        return posts

    @staticmethod
    def find_posts():
        query = db['post'].find()
        posts = PostDao.parse_post_query(query)
        return posts

    @staticmethod
    def find_post(oid: ObjectId):
        result = db['post'].find_one({'_id': oid})
        oid = result['_id']
        uid = result['user_id']
        content = result['content']
        img_url = result['img_url']
        post = Post(post_id=str(oid), user_id=uid, content=content, created_date=oid.generation_time, img_url=img_url)
        return post

    @staticmethod
    def delete_post(oid: ObjectId):
        result = db['post'].delete_one({'_id': oid})
        return result

    @staticmethod
    def find_all(order: int):
        if order == 1 or -1:
            query = db['post'].find().sort('_id', order)
        else:
            query = db['post'].find()
        posts = PostDao.parse_post_query(query)
        return posts

    @staticmethod
    def parse_post_query(query: Cursor):
        posts = []
        for result in query:
            # parse post
            oid = result['_id']
            uid = result['user_id']
            content = result['content']
            img_url = result['img_url']
            posts.append(
                Post(post_id=str(oid), user_id=uid, content=content, created_date=oid.generation_time, img_url=img_url))
        return posts


class ImageDao:
    @staticmethod
    def create_image(image_name: str, image_data):
        image = {'name': image_name, 'data': image_data}
        result = db['image'].insert_one(image)
        return result

    @staticmethod
    def find_image(oid: ObjectId):
        result = db['image'].find_one({'_id': oid})
        oid = result['_id']
        name = result['name']
        base64_data = result['data']
        image = Image(image_id=str(oid), name=name, data=base64_data)
        return image

    @staticmethod
    def delete_image(oid: ObjectId):
        result = db['image'].delete_one({'_id': oid})
        return result

import os

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from dao.dao_model import UserModel, PostModel, PostCollection


app_settings = {
    'db_name': os.getenv('MONGO_DB'),
    'mongodb_url': os.getenv('MONGO_URL'),
    'db_username': os.getenv('MONGO_USER'),
    'db_password': os.getenv('MONGO_PASSWORD'),
}

all_env_vars = os.environ
print(all_env_vars)
# connect to mongodb

# client = AsyncIOMotorClient(
#     app_settings.get('mongodb_url'),
#     username=app_settings.get('db_username'),
#     password=app_settings.get('db_password'),
#     uuidRepresentation="standard",
# )
# client = AsyncIOMotorClient("mongodb://localhost:27017/")
# dns = "mongodb-service"
# dns = "my-mongo-container"
ip = "10.96.1.1"
client = AsyncIOMotorClient(f"mongodb://{ip}:27017/")

db = client.ai33
users_collection = db.get_collection('users')
posts_collection = db.get_collection('posts')


def fix_object_id(sample: dict) -> dict:
    sample['id'] = str(sample['_id'])
    del [sample['_id']]
    return sample


class UserDao:
    @staticmethod
    async def create_user(user_info: UserModel):
        new_user = await users_collection.insert_one(
            user_info.model_dump(by_alias=True, exclude=["id"])
        )
        print(f'User created: {new_user}')
        created_user = await users_collection.find_one(
            {"_id": new_user.inserted_id}
        )
        print(f'Created user: {created_user}')
        if created_user is None:
            return fix_object_id(new_user)
        return fix_object_id(created_user)

    @staticmethod
    async def find_user(oid: ObjectId):
        result = await users_collection.find_one({'_id': oid})
        if result is None:
            return None
        return fix_object_id(result)

    @staticmethod
    async def find_users_by_name(username: str):
        result = await users_collection.find_one({'username': username})
        if result is None:
            return None
        return fix_object_id(result)

    @staticmethod
    def delete_user_by_id(oid: ObjectId):
        result = db['user'].delete_one({'_id': oid})
        return fix_object_id(result)

    @staticmethod
    def delete_user_by_name(name: str):
        result = db['user'].delete_one({'username': name})
        return fix_object_id(result)


class PostDao:
    @staticmethod
    async def create_post(post_info: PostModel):
        new_post = await posts_collection.insert_one(
            post_info.model_dump(by_alias=True, exclude=["id"])
        )
        created_post = await posts_collection.find_one(
            {'_id': new_post.inserted_id}
        )
        return fix_object_id(created_post)

    @staticmethod
    async def find_posts_by_uid(uid: str):
        posts = await posts_collection.find({'user_id': uid}).to_list(100)
        fixed_list = list()
        for post in posts:
            fixed_list.append(fix_object_id(post))
        return PostCollection(posts=fixed_list)

    @staticmethod
    async def find_posts():
        posts = await posts_collection.find().to_list(100)
        fixed_list = list()
        for post in posts:
            fixed_list.append(fix_object_id(post))
        return PostCollection(posts=fixed_list)

    @staticmethod
    def find_post(oid: ObjectId):
        result = db['post'].find_one({'_id': oid})
        oid = result['_id']
        uid = result['user_id']
        content = result['content']
        img_url = result['img_url']
        post = PostModel(post_id=str(oid), user_id=uid, content=content, created_date=oid.generation_time,
                         img_url=img_url)
        return post

    @staticmethod
    def delete_post(oid: ObjectId):
        result = db['post'].delete_one({'_id': oid})
        return result

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

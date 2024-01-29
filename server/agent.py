from bson import ObjectId
from image_generator import *
from server.dao.dao import UserDao, PostDao, ImageDao

user_dao = UserDao()
post_dao = PostDao()
image_dao = ImageDao()


def get_image_bytes(image: str):
    print("Getting image...")
    return image


def generate_image(prompt: str):
    return create_image(prompt)


def save_post(
        user_id: str,
        content: str,
        image_id: str
):
    result = post_dao.create_post(uid=user_id, content=content, img_url=image_id)
    return result


def get_posts_by_uid(user_id: str):
    result = post_dao.find_posts_by_uid(uid=user_id)
    return result


def check_user_validation(
        username: str,
        password: str
):
    users = user_dao.find_users_by_name(username=username)
    for user in users:
        if user.password == password:
            return user
    return None


def get_user_by_id(user_id: str):
    oid = ObjectId(user_id)
    user = user_dao.find_user(oid)
    return user


def create_user(
        username: str,
        password: str,
        email: str
):
    result = user_dao.create_user(username, password, email)
    return result

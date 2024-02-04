from bson import ObjectId
from image_generator import *
from dao.dao import UserDao, PostDao, ImageDao
from dao.dao_model import UserModel, PostModel
from pathlib import Path

user_dao = UserDao()
post_dao = PostDao()
image_dao = ImageDao()
logger = logging.getLogger(__name__)


def get_image_path(image_id: str):
    image = Path(get_image(image_id))
    logger.info(f"Getting image {image_id} from {file_path(image_id)}")
    return image


async def generate_image(prompt: str):
    result = await create_image(prompt)
    logger.info(f"Generated image {prompt} to {file_path(result)}")
    return result


def save_post(
        post: PostModel
):
    result = post_dao.create_post(post)
    return result


async def get_posts_by_uid(user_id: str):
    result = await post_dao.find_posts_by_uid(uid=user_id)
    return result


async def get_all_posts():
    result = await post_dao.find_posts()
    return result


async def check_user_validation(
        username: str,
        password: str
):
    user = await user_dao.find_users_by_name(username=username)
    print(user)
    if isinstance(user, dict) and user['password'] == password:
        user['password'] = ''
        return user
    return None


async def get_user_by_id(user_id: str):
    oid = ObjectId(user_id)
    user = await user_dao.find_user(oid)
    return user


async def create_user(
        user_info: UserModel
):
    result = await user_dao.create_user(user_info)
    return result


async def get_user_by_name(username: str):
    result = await user_dao.find_users_by_name(username=username)
    return result

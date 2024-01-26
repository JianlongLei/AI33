from model import *
from image_generator import *


def init_db():
    print("Initializing database...")


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
    print("Creating post...")


def check_user_validation(
        user_name: str,
        user_password: str
):
    return True


def get_user_by_id(user_id: str):
    return None


def create_user(
        username: str,
        password: str,
        email: str
):
    return None

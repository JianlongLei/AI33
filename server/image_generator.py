import os
import uuid

import requests
import logging

logger = logging.getLogger(__name__)

api_key = os.getenv('X_API_KEY')
def image_generator(prompt: str):
    r = requests.post('https://clipdrop-api.co/text-to-image/v1',
                      files={
                          'prompt': (None, prompt, 'text/plain')
                      },
                      headers={
                          'x-api-key': api_key}
                      )
    if (r.ok):
        logger.info(f'Image successfully generated.')
        return r.content
    else:
        logger.error(r)
        return None


def save_image(image_byte: bytes):
    image_id = generate_image_id()
    with open(file_path(image_id), 'wb') as file:
        file.write(image_byte)
    return image_id


def get_image(image_id: str):
    # with open(file_path(image_id), "rb") as image_file:
    #     image_bytes = image_file.read()
    # return image_bytes
    return file_path(image_id)


def generate_image_id():
    return str(uuid.uuid4())


def file_path(image_id: str):
    return "/images/" + image_id + ".png"
    # return os.getcwd() + "/images/" + image_id + ".png"


async def create_image(prompt: str):
    return save_image(image_generator(prompt))

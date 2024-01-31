import os
import uuid

import requests


def image_generator(prompt: str):
    r = requests.post('https://clipdrop-api.co/text-to-image/v1',
                      files={
                          'prompt': (None, prompt, 'text/plain')
                      },
                      headers={
                          'x-api-key': '8661fb24acb685550f5d890e440d361aba8f8667cad3a1338bdecc55b1e6d3bbda4e7bd1331daf0aebe9005d199d1ef5'}
                      )
    if (r.ok):
        return r.content
    else:
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
    return os.getcwd() + "/images/" + image_id + ".png"


async def create_image(prompt: str):
    return save_image(image_generator(prompt))

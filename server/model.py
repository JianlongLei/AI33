from pydantic import BaseModel
from typing import Union


class Post(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


class User(BaseModel):
    name: str
    description: str
    uid: Union[str, None] = None


class Image(BaseModel):
    id: str
    image_src: str
from pydantic import BaseModel
from typing import Union


class Post(BaseModel):
    user_id: str
    content: str


class User(BaseModel):
    user_id: str
    name: str
    description: str
    uid: Union[str, None] = None


class Register(BaseModel):
    username: str
    password: str
    email: str


class Login(BaseModel):
    username: str
    password: str


class Logout(BaseModel):
    user_id: str


class Image(BaseModel):
    id: str
    image_src: str

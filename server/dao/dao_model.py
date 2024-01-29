from pydantic import BaseModel


class Post(BaseModel):
    post_id: str  # prime key
    user_id: str
    content: str
    created_date: str
    img_url: str


class User(BaseModel):
    user_id: str  # prime key
    name: str
    psw: str  # password
    email: str


class Image(BaseModel):
    image_id: str  # prime key
    name: str
    data: str

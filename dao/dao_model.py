from pydantic import BaseModel


class Post(BaseModel):
    post_id: str  # prime key
    user_id: str
    content: str


class User(BaseModel):
    user_id: str  # prime key
    name: str
    description: str


class Image(BaseModel):
    id: str  # prime key
    image_src: str

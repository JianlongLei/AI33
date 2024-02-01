from typing import List

from pydantic import BaseModel, Field

from dao.dao_model import UserModel, PostModel


class UserResponse(BaseModel):
    status: str = Field(...)
    message: str | None = Field(default=None)
    user: UserModel | None = Field(default=None)


class PostResponse(BaseModel):
    status: str = Field(...)
    message: str | None = Field(default=None)
    post: PostModel | None = Field(default=None)


class PostCollectionResponse(BaseModel):
    status: str = Field(...)
    message: str | None = Field(default=None)
    posts: List[PostModel] | None = Field(default=None)

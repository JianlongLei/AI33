from bson import ObjectId
from typing_extensions import Annotated
from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field, EmailStr, BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class PostModel(BaseModel):
    # The primary key for the StudentModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses
    id: Optional[PyObjectId] | str = Field(alias="_id", default=None)  # prime key
    user_id: str = Field(...)
    title: str | None = Field(default=None)
    content: str = Field(...)
    created_date: str | None = Field(default=None)
    img_url: str | None = Field(default=None)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "user_id": "abcde",
                "title": "A nice day",
                "content": "Enjoy your time on a beach",
                "created_date": "11231123",
                "img_url": "/image/1234"
            }
        },
    )


class UserModel(BaseModel):
    # The primary key for the StudentModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] | str = Field(alias="_id", default=None)  # prime key
    username: str = Field(...)
    password: str = Field(...)
    email: EmailStr | None = Field(default=None)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "username": "Jane Doe",
                "password": "<PASSWORD>",
                "email": "jdoe@example.com",
            }
        },
    )


class PostCollection(BaseModel):
    posts: List[PostModel]


class Image(BaseModel):
    image_id: str  # prime key
    name: str
    data: str

import datetime
from fastapi import FastAPI, Body, HTTPException

from typing import Annotated

from starlette import status
from starlette.responses import FileResponse

from agent import *
from const import *
from dao.dao_model import UserModel, PostCollection, PostModel
from tools import *

app = FastAPI()


@app.get(
    "/posts/{user_id}",
    response_description="Get all posts from a specific user",
    response_model=PostCollection,
    response_model_by_alias=False,
)
async def read_item(
        user_id: Annotated[str, Path(title="The Id of the user")],
):
    posts = await get_posts_by_uid(user_id)
    return posts


@app.put(
    "/homepage/",
    response_description="Get all posts from all user",
    response_model=PostCollection,
    response_model_by_alias=False,
)
async def homepage():
    result = await get_all_posts()
    return result


@app.get(
    "/image/{image_id}",
    response_description="get an image with image id",
)
async def get_image(
        image_id: Annotated[str, Path(title="The Id of the image")]
):
    image_path = get_image_path(image_id)
    if not image_path.is_file():
        result = FAIL_RESULT
        result["message"] = "Image not found"
        return FAIL_RESULT
    return FileResponse(image_path, media_type="image/png")


@app.post(
    "/login/",
    response_description="Login to your account",
    response_model=UserModel,
)
async def login(
        user_info: UserModel = Body(...)
):
    result = await check_user_validation(user_info.name, user_info.psw)
    if result:
        return result
    return FAIL_RESULT


@app.post(
    "/register/",
    response_description="Register a new user",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def register(
        user_info: UserModel = Body(...)
):
    if check_email_validation(user_info.email):
        user = await get_user_by_name(user_info.name)
        if isinstance(user, dict):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User exists"
            )
        created_user = await create_user(user_info)
        return created_user
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email"
        )


@app.post(
    "/logout/",
    response_description="logout the user",
)
async def logout(
        id: str = Body(..., embed=True)
):
    user = await get_user_by_id(id)
    print(user)
    if isinstance(user, dict):
        return SUCCESS_RESULT
    return FAIL_RESULT


@app.post(
    "/create/post/",
    response_description="create a new post",
    response_model=PostModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_post(
        post: PostModel
):
    print("start")
    user = await get_user_by_id(post.user_id)
    print(user)
    if not isinstance(user, dict):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    image_id = await generate_image(post.content)
    print(image_id)
    if image_id is None:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Image create failed"
        )
    now = datetime.datetime.now()
    post.created_date = now.strftime("%d/%m/%Y %H:%M:%S")
    post.img_url = "/image/" + image_id
    print(post)
    result = await save_post(post)
    print(result)
    return result

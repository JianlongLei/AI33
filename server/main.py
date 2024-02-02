import datetime
from fastapi import FastAPI, Body

from typing import Annotated

from starlette import status
from starlette.responses import FileResponse

from agent import *
from const import *
from dao.dao_model import UserModel, PostModel
from model import UserResponse, PostResponse, PostCollectionResponse
from tools import *

app = FastAPI()


@app.get(
    "/posts/{user_id}",
    response_description="Get all posts from a specific user",
    response_model=PostCollectionResponse,
    response_model_by_alias=False,
)
async def read_item(
        user_id: Annotated[str, Path(title="The Id of the user")],
):
    posts = await get_posts_by_uid(user_id)
    response = PostCollectionResponse(status=SUCCESS)
    response.posts = posts.posts
    return response


@app.get(
    "/homepage/",
    response_description="Get all posts from all user",
    response_model=PostCollectionResponse,
    response_model_by_alias=False,
)
async def homepage():
    result = await get_all_posts()
    response = PostCollectionResponse(status=SUCCESS)
    response.posts = result.posts
    return response


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
    response_model=UserResponse,
)
async def login(
        user_info: UserModel = Body(...)
):
    print(user_info)
    result = await check_user_validation(user_info.username, user_info.password)
    response = UserResponse(status=SUCCESS)
    if isinstance(result, dict):
        response.status = SUCCESS
        result['password'] = ''
        response.user = result
        return response
    response.status = FAIL
    return response


@app.post(
    "/register/",
    response_description="Register a new user",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def register(
        user_info: UserModel = Body(...)
):
    response = UserResponse(status=SUCCESS)
    if check_email_validation(user_info.email):
        user = await get_user_by_name(user_info.username)
        if isinstance(user, dict):
            response.status = FAIL
            response.message = "User exists"
            return response
        created_user = await create_user(user_info)
        created_user['password'] = ''
        response.status = SUCCESS
        response.user = created_user
        return response
    else:
        response.status = FAIL
        response.message = "Invalid email"
        return response


@app.post(
    "/logout/",
    response_description="logout the user",
)
async def logout(
        id: str = Body(..., embed=True)
):
    user = await get_user_by_id(id)
    if isinstance(user, dict):
        return SUCCESS_RESULT
    return FAIL_RESULT


@app.post(
    "/create/post/",
    response_description="create a new post",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_post(
        post: PostModel
):
    response = PostResponse(status=SUCCESS)
    user = await get_user_by_id(post.user_id)
    if not isinstance(user, dict):
        response.status = FAIL
        response.message = "User does not exist"
        return response
    image_id = await generate_image(post.content)
    if image_id is None:
        response.status = FAIL
        response.message = "Image create failed"
        return response
    now = datetime.datetime.now()
    post.created_date = now.strftime("%d/%m/%Y %H:%M:%S")
    post.img_url = "/image/" + image_id
    result = await save_post(post)
    response.status = SUCCESS
    response.post = result
    return response

from fastapi import Depends, FastAPI, Path
from fastapi.openapi.models import Response
from fastapi.security import OAuth2PasswordBearer

from typing import Annotated

from agent import *
from server.const import *
from server.tools import *

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/posts/{user_id}")
def read_item(
        token: Annotated[str, Depends(oauth2_scheme)],
        user_id: Annotated[str, Path(title="The Id of the user")],
        last_post_id: Annotated[str, Path(title="The last Id of previous posts result")],
        page_size: Annotated[int, Path(title="The page size of this query wants")] = 10
):
    return {"user_id": user_id, "last_post_id": last_post_id, "page_size": page_size}


@app.put("/homepage/")
def homepage(
        token: Annotated[str, Depends(oauth2_scheme)],
        last_post_id: Annotated[str, Path(title="The last Id of previous posts result")],
        page_size: Annotated[int, Path(title="The page size of this query wants")] = 10
):
    # return {"last_post_id": last_post_id, "page_size": page_size}
    user = User()
    user.name = "a"
    user.description = "b"
    user.uid = "c"
    return user


@app.get("/image/{image_id}")
def get_image(
        token: Annotated[str, Depends(oauth2_scheme)],
        image_id: Annotated[str, Path(title="The Id of the image")]
):
    image_bytes: bytes = get_image_bytes(image_id)
    return Response(content=image_bytes, media_type="image/png")


@app.post("/login/")
def login(
        user_info: Login
):
    if check_user_validation(user_info.username, user_info.password):
        return SUCCESS_RESULT
    return FAIL_RESULT


@app.post("/register/")
def register(
        user_info: Register
):
    if check_email_validation(user_info.email):
        create_user(user_info.username, user_info.password, user_info.email)
    else:
        result = FAIL_RESULT
        result[MESSAGE] = "invalid email"
        return result
    return {"username": user_info.username, "password": user_info.password, "email": user_info.email}


@app.post("/logout/")
def logout(
        user_info: Logout
):
    if get_user_by_id(user_info.user_id):
        return SUCCESS_RESULT
    return FAIL_RESULT


@app.post("/create/post/")
def create_post(
        token: Annotated[str, Depends(oauth2_scheme)],
        post: Post
):
    image_id = generate_image(post.content)
    save_post(post.user_id, post.content, image_id)
    return {"user_id": post.user_id, "content": post.content, "image_url": image_id}

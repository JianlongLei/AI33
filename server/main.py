from fastapi import FastAPI
from fastapi.openapi.models import Response

from model import *
from agent import *

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/posts/{user_id}")
def read_item(user_id: str, last_post_id: str, page_size: int = 10):
    return {"user_id": user_id, "last_post_id": last_post_id, "page_size": page_size}


@app.put("/homepage/")
def update_item(last_post_id: str, page_size: int = 10):
    return {"last_post_id": last_post_id, "page_size": page_size}


@app.get("/image/{image_id}")
def get_image(image_id: str):
    image_bytes: bytes = get_image_bytes(image_id)
    return Response(content=image_bytes, media_type="image/png")


@app.post("/login/")
def login(username: str, password: str):
    return {"username": username, "password": password}


@app.post("/register/")
def register(username: str, password: str, email: str):
    return {"username": username, "password": password, "email": email}


@app.post("/logout/")
def logout(user_id: str):
    return {"user_id": user_id}


@app.post("/create/post/")
def create_post(user_id: str, content: str):
    return {"user_id": user_id, "content": content}

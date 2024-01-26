import base64
from io import BytesIO

from PIL import Image
from bson import ObjectId

from dao import *

user_dao = UserDao()
post_dao = PostDao()
image_dao = ImageDao()


# def test_find():
#     user = user_dao.find_user(ObjectId('65ad2deae1bc7a3d038a81bf'))
#     print(user)
#
#
# def test_insert():
#     res = user_dao.create_user(name="assa", psw="psw", descr="test user")
#     print(res)
#
#
# def test_insert_image(image_path):
#     with open(image_path, 'rb') as image_file:
#         image_data = base64.b64encode(image_file.read())
#         # print(image_data)
#         image = base64.b64decode(image_data)
#         print(image)
#         image = Image.open(BytesIO(image))
#         image.show()


def test_user():
    res1 = user_dao.create_user(name="123", psw="psw", descr="test user")
    res2 = user_dao.create_user(name="123", psw="psw", descr="test user")
    print(f"Expected results: {True}, {False}; Actual results: {res1}, {res2}")

    users = user_dao.find_users_by_name(username="123")
    num = len(users)
    print(f"Expected result: {1}; Actual result: {num}")

    user1 = users[0]
    oid = ObjectId(user1.user_id)
    user2 = user_dao.find_user(oid)
    res3 = user1 == user2
    print(f"Expected result: {True}; Actual result: {res3}")

    d_res1 = user_dao.delete_user_by_name(name="123")
    d_res2 = user_dao.delete_user_by_id(oid)
    print(f"Expected results: {1}, {0}; Actual results: {d_res1.deleted_count}, {d_res2.deleted_count}")


def test_post():
    pass


def test_img():
    img_path = "astronaut_rides_horse.png"
    with open(img_path, 'rb') as image_file:
        bs64data = base64.b64encode(image_file.read())
        image_file.close()
    result = image_dao.create_image(image_name=img_path, image_data=bs64data)
    oid = result.inserted_id

    img = image_dao.find_image(oid)
    img_data = base64.b64decode(img.data)
    print(len(bs64data))
    print(len(img_data))
    # base64 format may be too large to store in mongodb
    res1 = bs64data == img_data
    print(f"Expected result: {True}; Actual result: {res1}")

    result = image_dao.delete_image(oid)
    print(result)


if __name__ == '__main__':
    # test_user()
    test_post()
    test_img()

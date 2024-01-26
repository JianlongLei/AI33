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


def user_test():
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


if __name__ == '__main__':
    # app.run()
    # test_find()
    # test_insert()
    # cursor = user_dao.find_user_by_name("asxsa")
    # print(cursor is None)
    # print(cursor)
    # results = list(cursor)
    # print(results)
    # print(len(results))
    # path = "astronaut_rides_horse.png"
    # test_insert_image(path)
    user_test()



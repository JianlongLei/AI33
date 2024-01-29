import os

SUCCESS = "success"
FAIL = "failed"
SUCCESS_RESULT = {"status": SUCCESS}
FAIL_RESULT = {"status": FAIL}
MESSAGE = "message"


class Constant:
    version = "0.1.0"
    title = "Constant"

    app_settings = {
        'db_name': os.getenv('MONGO_DB'),
        'mongodb_url': os.getenv('MONGO_URL'),
        'db_username': os.getenv('MONGO_USER'),
        'db_password': os.getenv('MONGO_PASSWORD'),
    }

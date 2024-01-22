from flask import Flask
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.testing import db

app = Flask(__name__, template_folder="template/")
app.config.update(
    MONGO_URI='mongodb://localhost:27017/flask',
    MONGO_USERNAME='',
    MONGO_PASSWORD='',
    # MONGO_DBNAME='user'
)
app.debug = True
mongo = PyMongo(app)


class Post:

    def __init__(self, post_id, title, content, author, date):
        self.post_id = post_id
        self.title = title
        self.content = content
        self.author = author
        self.date = date

    @classmethod
    def create_book(cls, title, content, author, date):
        post_id = mongo.db.post.insert({
            'title': title,
            'author': author,
            'content': content,
            'date': date
        })
        return cls(post_id, title, content, author, date)

    @classmethod
    def get_top_ten_posts(cls):
        # Retrieve the top ten books sorted by publication year in descending order
        top_ten_posts = mongo.db.post.find().sort('date', -1).limit(10)
        print(top_ten_posts)
        for post in top_ten_posts:
            print(post)
        # return None
        return [cls(post["_id"], post['title'], post['author'], post['content'], post['date']) ]
    # id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(100), nullable=False)
    # content = db.Column(db.Text, nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

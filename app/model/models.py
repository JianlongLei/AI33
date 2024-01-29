# from lib2to3.pytree import Base
#
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
#
# from sqlalchemy import Integer, String
# from sqlalchemy.orm import Mapped, mapped_column
#
# # db = SQLAlchemy(model_class=Base)
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password_hash = db.Column(db.String(128))
#     posts = db.relationship('Post', backref='author', lazy=True)
#
#     @property
#     def password(self):
#         raise AttributeError('password is not a readable attribute')
#
#     @password.setter
#     def password(self, password):
#         self.password_hash = generate_password_hash(password)
#
#     def verify_password(self, password):
#         return check_password_hash(self.password_hash, password)
#
#
# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

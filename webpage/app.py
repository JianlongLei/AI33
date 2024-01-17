import os

from flask import *

from flask import Flask
from flask_pymongo import PyMongo
from werkzeug.local import LocalProxy
from werkzeug.utils import secure_filename
from models import *

def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:
        db = g._database = PyMongo(current_app).db

    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)

app = Flask(__name__)
def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:
        db = g._database = PyMongo(current_app).db

    return db


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('template/register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            session['username'] = user.username
            # Implement additional check here for manager
            return redirect(url_for('main'))
    return render_template('template/login.html')


@app.route('/')
def home():
    # Fetch all posts from the database, ordered by the date in descending order
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('template/home.html', posts=posts)

app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_post = Post(title=title, content=content, user_id=session['user_id'])
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main'))
    return render_template('template/post.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
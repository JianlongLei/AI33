import os

from flask import *
from flask import Flask
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename

from model.Post import Post
from model.User import User

app = Flask(__name__, template_folder="template/")
app.config.update(
    MONGO_URI='mongodb://localhost:27017/flask',
    MONGO_USERNAME='',
    MONGO_PASSWORD='',
    # MONGO_DBNAME='user'
)
app.debug = True
mongo = PyMongo(app)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # new_user = User(username=username, email=email, password=password)
        new_user = User.create_user(username=username, email=email, password=password)
        # mongo.db.session.add(new_user)
        # mongo.db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # user = User.query.filter_by(username=username).first()
        use = User.find_by_username(username)
        # if user and user.verify_password(password):
        #     session['username'] = user.username
        #     # Implement additional check here for manager
        #     return redirect(url_for('main'))
    return render_template('login.html')


@app.route('/')
def home():
    # Fetch all posts from the database, ordered by the date in descending order
    # posts = Post.query.order_by(Post.date_posted.desc()).all()
    top_ten_posts = Post.get_top_ten_posts()
    if top_ten_posts is None:
        top_ten_posts = []
    # posts = None
    return render_template('home.html', posts=top_ten_posts)


app.config['UPLOAD_FOLDER'] = 'uploads/'


@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # top_ten_posts = Post.get_top_ten_posts()
        # new_post = Post(title=title, content=content, user_id=session['user_id'])
        # mongo.db.session.add(new_post)
        # mongo.db.session.commit()
        return redirect(url_for('main'))
    return render_template('home.html')


if __name__ == '__main__':
    # db.create_all()

    app.run(debug=True)

import os

from fastapi import requests
from flask import *
from flask import Flask
from werkzeug.utils import secure_filename

from model.Post import Post
from model.User import User

app = Flask(__name__, template_folder="template/", static_folder="static/")
app.debug = True
myserver = ""

current_user = User
post_list = []
post_content = {}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        url = myserver+"/register/"
        data = {"username": username, "password": password, "email": email}
        response =  requests.post(url,json=data)
        if response.json()['status'] == 'success':
            flash('You have successfully registered! Please login.')
            # current_user = User(response.json()['user_id'], response.json()['username'], response.json()['password'], response.json()['email'])
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        url = myserver+"/login/"
        data = {'username': username, 'password': password}
        response = requests.post(url,json=data)
        if response.json()['status'] == 'success':
            flash('You have successfully logged in!')
            current_user = User(response.json()['user_id'], response.json()['username'], response.json()['password'], response.json()['email'])
            return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout(current_user):
    if request.method == 'POST':
        url = myserver+"/logout/"
        data = {"user_id": current_user.user_id}
        response = requests.get(url,json=data)
        if response.json()['status'] == 'success':
            flash('You have successfully logged out!')
            current_user = None
            return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('main'))
    return render_template('createPost.html')


@app.route('/')
def homepage():
    posts_data = request.args.get('posts', [])
    current_posts = posts_data
    if len(current_posts) == 0:
        # url = myserver + "/homepage/"
        # response = requests.get(url)
        response = {"status": "success", "post_list": 
                    [{"author": "User1", "date": "2022-01-01", "content": "First post", "image_url": "/static/images/post1.png","post_id": "1"},
                    {"author": "User2", "date": "2022-01-02", "content": "Second post", "image_url": "/static/images/post1.png","post_id":"2"},
                    {"author": "User2", "date": "2022-01-02", "content": "third post", "image_url": "/static/images/post1.png","post_id":"3" },
                    {"author": "User2", "date": "2022-01-02", "content": "fourth post", "image_url": "/static/images/post1.png","post_id":"4"},
                    ]}
        # if response.json()['status'] == 'success':
        if response['status'] == 'success':
            # current_posts = response.json()['post_list']
            current_posts = response['post_list']
            return render_template('home.html', posts=current_posts, last_post_id=response['post_list'][-1]['post_id'])
        flash("fail to initialize posts")
    return render_template('home.html', posts=current_posts)


@app.route('/update/', methods=['GET', 'POST'])
def update():
    # url = myserver + "/homepage/"
    last_post_id = request.args.get('last_post_id')
    data = {"last_post_id": last_post_id}
    print(data)
    # response = requests.get(url, json=data)
    response = {"status": "success", "post_list":
        [{"author": "User1", "date": "2022-01-01", "content": "First post", "image_url": "/static/images/post1.png",
          "post_id": "1"},
         {"author": "User2", "date": "2022-01-02", "content": "Second post", "image_url": "/static/images/post1.png",
          "post_id": "2"},
         {"author": "User2", "date": "2022-01-02", "content": "third post", "image_url": "/static/images/post1.png",
          "post_id": "3"},
         ]}
    # if response.json()['status'] == 'success':
    if response['status'] == 'success':
        # current_posts = response.json()['post_list']
        current_posts = response['post_list']
        return render_template('home.html', posts=current_posts, last_post_id=response['post_list'][-1]['post_id'])
    # flash("fail to load posts")
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)


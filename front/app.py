import os

from fastapi import requests
from flask import *
from flask import Flask
from werkzeug.utils import secure_filename

from model.User import User

app = Flask(__name__, template_folder="template/", static_folder="static/")
app.debug = True
# myserver = os.environ["SERVER_URL"]
myserver = 'localhost:8000'

global current_user
current_user = None
current_post_list = []
response_json = {
    'user_id': 1,
    'username': 'example_user',
    'password': 'example_password',
    'email': 'example@email.com'
}
user_dict = {
    'user_id': response_json['user_id'],
    'username': response_json['username'],
    'password': response_json['password'],
    'email': response_json['email']
}

@app.route('/register', methods=['GET', 'POST'])
def register():
    global current_user
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        url = myserver+"/register/"
        data = {"username": username, "password": password, "email": email}
        print(data)
        # response =  requests.post(url,json=data)
        # if response.json()['status'] == 'success':
        response = {"status": "success", "user_id": 1, "username": "example_user", "password": "example_password", "email": ""}
        if response['status'] == 'success':
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global current_user
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        url = myserver+"/login/"
        data = {'username': username, 'password': password}
        response = requests.post(url,json=data)
        # response = {"status": "success", "user_id": 1, "username": "example_user", "password": "example_password", "email": "123@gmail.com"}
        # if response.json()['status'] == 'success':
        if response['status'] == 'success':
            # flash('You have successfully logged in!')
            # current_user = User(response.json()['user_id'], response.json()['username'], response.json()['password'], response.json()['email'])
             current_user = User(response['user_id'], request.form['username'], response['password'], response['email'])
             return redirect(url_for('homepage'))
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    global current_user
    url = myserver+"/logout/"
    data = {"user_id": current_user.user_id}
    response = requests.get(url,json=data)
    # response = {"status": "success"}
    # if response.json()['status'] == 'success':
    if response['status'] == 'success':
        current_user = None
        current_post_list.clear()
    return redirect(url_for('homepage'))


@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        # file = request.files['file']
        # filename = secure_filename(file.filename)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        url = myserver+"/create/post/"
        data = {"user_id": current_user.user_id,"title":title, "content": content}
        response = requests.post(url,json=data)
        # response = {"status": "success"}
        # if response.json()['status'] == 'success':
        if response['status'] == 'success':
            return redirect(url_for('update'))
    return render_template('createPost.html')


@app.route('/')
def homepage():
    global current_user
    global current_post_list
    if current_user == None:
        return redirect(url_for('login'))
    # posts_data = request.args.get('posts', [])
    # current_posts = posts_data
    if len(current_post_list) == 0:
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
            current_post_list = response['post_list']
            return render_template('home.html', posts=current_post_list, last_post_id=response['post_list'][-1]['post_id'],user_name=current_user.username)
    return render_template('home.html', posts=current_post_list,user_name=current_user.username)


@app.route('/update/', methods=['GET', 'POST'])
def update():
    global current_post_list
    # url = myserver + "/homepage/"
    # last_post_id = request.args.get('last_post_id')
    last_post_id = current_post_list[-1]['post_id']
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
    # Iterate through response['post_list']
        for post in response['post_list']:
            # Append the new post to current_post_list
            current_post_list.append(post)
        # Trim current_post_list to keep it at a maximum size of 10
        excess_posts = len(current_post_list) - 10
        if excess_posts > 0:
            current_post_list = current_post_list[excess_posts:]
        return render_template('home.html', posts=current_post_list, last_post_id=response['post_list'][-1]['post_id'])
    return render_template('home.html')



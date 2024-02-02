import hashlib
import os

import requests

from flask import *
from flask import Flask

from model.User import User

app = Flask(__name__, template_folder="template/", static_folder="static/")
app.debug = True
myserver = os.getenv("SERVER_URL")

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


def check_response(response):
    if response.status_code < 200 or response.status_code > 300:
        return False
    if response.json().get('status') == 'success':
        return True
    return False


def hash_password(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()


@app.route('/register', methods=['GET', 'POST'])
def register():
    global current_user
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = hash_password(request.form['password'])
        url = myserver + "/register/"
        data = {"username": username, "password": password, "email": email}
        print(data)
        response = requests.post(url, json=data)
        print(response)
        print(response.json())
        if check_response(response):
            current_user = User(response['id'], request.form['username'], response['password'], response['email'])
            return redirect(url_for('homepage'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global current_user
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])
        url = myserver + "/login/"
        data = {'username': username, 'password': password}
        print(data)
        response = requests.post(url, json=data)
        if check_response(response):
            result = response.json()
            print(result)
            if 'user' in result.keys():
                user = result['user']
                current_user = User(user['id'], user['username'], user['password'], user['email'])
                return redirect(url_for('homepage'))
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    global current_user
    url = myserver + "/logout/"
    data = {"user_id": current_user.user_id}
    response = requests.post(url, json=data)
    if check_response(response):
        current_user = None
        current_post_list.clear()
    return redirect(url_for('homepage'))


@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        url = myserver + "/create/post/"
        data = {"user_id": current_user.user_id, "title": title, "content": content}
        response = requests.post(url, json=data)
        if check_response(response):
            return redirect(url_for('homepage'))
    return render_template('createPost.html')


@app.route('/')
def homepage():
    global current_user
    global current_post_list
    if current_user == None:
        return redirect(url_for('login'))
    url = myserver + "/homepage/"
    response = requests.get(url)
    print(response)
    print(response.json())
    if check_response(response):
        current_post_list = response.json()['posts']
        for post in current_post_list:
            if 'img_url' in post.keys():
                post['img_url'] = myserver + post['img_url']
        print(current_post_list)
        return render_template('home.html', posts=current_post_list)
    return render_template('home.html', posts=current_post_list, user_name=current_user.username)


@app.route('/update/', methods=['GET', 'POST'])
def update():
    global current_post_list
    url = myserver + "/homepage/"
    last_post_id = request.args.get()
    # last_post_id = current_post_list[-1]['post_id']
    data = {"last_post_id": last_post_id}
    # print(data)
    response = requests.get(url, json=data)
    # response = {"status": "success", "post_list":
    #     [{"author": "User1", "date": "2022-01-01", "content": "First post", "image_url": "/static/images/post1.png",
    #       "post_id": "1"},
    #      {"author": "User2", "date": "2022-01-02", "content": "Second post", "image_url": "/static/images/post1.png",
    #       "post_id": "2"},
    #      {"author": "User2", "date": "2022-01-02", "content": "third post", "image_url": "/static/images/post1.png",
    #       "post_id": "3"},
    #      ]}
    if check_response(response):
        # if response['status'] == 'success':
        # Iterate through response['post_list']
        for post in response.json()['posts']:
            # Append the new post to current_post_list
            current_post_list.append(post)
        # Trim current_post_list to keep it at a maximum size of 10
        excess_posts = len(current_post_list) - 10
        if excess_posts > 0:
            current_post_list = current_post_list[excess_posts:]
        return render_template('home.html', posts=current_post_list, last_post_id=response['post_list'][-1]['post_id'],
                               user_name=current_user.username)
    return render_template('home.html', posts=current_post_list, user_name=current_user.username)


if __name__ == '__main__':
    # print("ready")
    app.run(host='0.0.0.0')

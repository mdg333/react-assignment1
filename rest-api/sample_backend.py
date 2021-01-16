import random, string
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
users = {
    'users_list':
        [
            {
                'id': 'xyz789',
                'name': 'Charlie',
                'job': 'Janitor',
            },
            {
                'id': 'abc123',
                'name': 'Mac',
                'job': 'Bouncer',
            },
            {
                'id': 'ppp222',
                'name': 'Mac',
                'job': 'Professor',
            },
            {
                'id': 'yat999',
                'name': 'Dee',
                'job': 'Aspring actress',
            },
            {
                'id': 'zap555',
                'name': 'Dennis',
                'job': 'Bartender',
            }
        ]
}


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/users/<id>', methods=['GET', 'DELETE'])
def get_user(id):
    if request.method == 'GET':
        if id:
            for user in users['users_list']:
                if user['id'] == id:
                    return user
            return ({})
        return users
    elif request.method == 'DELETE':
        userToDel = request.get_json()
        try:
            users['users_list'].remove(userToDel)
            resp = jsonify(success=True)
            resp.status_code = 200
            return resp
        except ValueError:
            resp = jsonify(success=False)
            resp.status_code = 404
            return resp


@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        search_username = request.args.get('name')
        search_job = request.args.get('job')
        subdict = {'users_list': []}
        for user in users['users_list']:
            if search_username in {None, user['name']} and search_job in {None, user['job']}:
                subdict['users_list'].append(user)
        return subdict
    elif request.method == 'POST':
        userToAdd = request.get_json()
        if userToAdd.get('id') is None:
            new_id = ''.join(random.choice(string.ascii_lowercase) for _ in range(3)) +\
                 ''.join(random.choice(string.digits) for _ in range(3))
            userToAdd.update({'id': new_id})
        users['users_list'].append(userToAdd)
        resp = jsonify(userToAdd)
        resp.status_code = 201
        return resp

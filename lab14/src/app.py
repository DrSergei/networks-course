from flask import Flask, request, jsonify, abort, send_file

import os
from uuid import uuid4

app = Flask(__name__)

db = {}
users = {}

class Product:
    def __init__(self, name, description):
        self.name = name 
        self.description = description

def get_token():
    return uuid4().hex

def check_token(id, token):
    _, tmp = db[id]
    if tmp == 'public':
        return True
    if tmp == token:
        return True
    return False

def get_new_id():
    return uuid4().hex

def db_insert_product(id, product, token):
    db[id] = (product, token)

def db_pop_product(id):
    return db.pop(id)[0]

def db_get_product(id):
    return db[id][0]

def to_scheme(id, product):
    res =  {
        "id": id,
        "name": product.name,
        "decscription": product.description,
    }
    return res

@app.route('/user/sign-up', methods=['POST'])
def sign_up():
    try:
        data = request.form
        email = data['email']
        password = data['password']
        token = get_token()
        users[(email, password)] = token
        return jsonify({})
    except Exception as e:
        print(e)
        abort(400)

@app.route('/user/sign-in', methods=['POST'])
def sign_in():
    try:
        data = request.form
        email = data['email']
        password = data['password']
        token = users[(email, password)]
        res = {'token': token}
        return jsonify(res)
    except Exception as e:
        print(e)
        abort(400)

@app.route('/product', methods=['POST'])
def post_product():
    try:
        data = request.form
        args = request.args
        token = args.get('token', 'public')
        id = get_new_id()
        product = Product(data['name'], data['description'])
        db_insert_product(id, product, token)
        return jsonify(to_scheme(id, product))
    except Exception as e:
        print(e)
        abort(400)

@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    try:
        args = request.args
        token = args.get('token', 'public')
        if not check_token(id, token):
            abort(401)
        product = db_get_product(id)
        return jsonify(to_scheme(id, product))
    except Exception as e:
        print(e)
        abort(404)

@app.route('/product/<id>', methods=['PUT'])
def put_product(id):
    try:
        args = request.args
        token = args.get('token', 'public')
        if not check_token(id, token):
            abort(401)
        product = db_pop_product(id)
        data = request.form
        name = data.get('name')
        if name is not None:
            product.name = name
        description = data.get('description')
        if description is not None:
            product.description = name
        db_insert_product(id, product)
        return jsonify(to_scheme(id, product))
    except Exception as e:
        print(e)
        abort(404)

@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    try:
        args = request.args
        token = args.get('token', 'public')
        if not check_token(id, token):
            abort(401)
        product = db_pop_product(id)
        return jsonify(to_scheme(id, product))
    except Exception as e:
        print(e)
        abort(404)

@app.route('/products', methods=['GET'])
def get_products():
    buffer = []
    args = request.args
    token = args.get('token', 'public')
    for id, (product, tmp) in db.items():
        if tmp != 'public' and tmp != token:
            continue
        buffer.append(to_scheme(id, product))
    return jsonify(buffer)

if __name__ == '__main__':
    app.run(debug=True)

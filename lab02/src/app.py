from flask import Flask, request, jsonify, abort, send_file

import os
from uuid import uuid4

app = Flask(__name__)

db = {}

class Product:
    def __init__(self, name, description, icon = None):
        self.name = name 
        self.description = description
        self.icon = icon

def get_new_id():
    return uuid4().hex

def db_insert_product(id, product):
    db[id] = product

def db_pop_product(id):
    return db.pop(id)

def db_get_product(id):
    return db[id]

def get_path(id):
    return os.path.join(os.getcwd(), 'icons', str(id))

def to_scheme(id, product):
    res =  {
        "id": id,
        "name": product.name,
        "decscription": product.description,
    }
    if product.icon is not None:
        res['icon'] = product.icon
    return res

@app.route('/product', methods=['POST'])
def post_product():
    try:
        data = request.form
        id = get_new_id()
        product = Product(data['name'], data['description'])
        db_insert_product(id, product)
        return jsonify(to_scheme(id, product))
    except Exception as e:
        print(e)
        abort(400)

@app.route('/product/<id>/image', methods=['POST'])
def post_icon(id):
    try:
        data = request.files
        icon = data['icon']
        product = db_get_product(id)
        _, ext = os.path.splitext(icon.filename)
        path = get_path(id) + ext
        product.icon = path
        icon.save(path)
        return jsonify(to_scheme(id, product))
    except Exception as e:
        print(e)
        abort(404)

@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    try:
        product = db_get_product(id)
        return jsonify(to_scheme(id, product))
    except Exception as e:
        print(e)
        abort(404)

@app.route('/product/<id>/image', methods=['GET'])
def get_icon(id):
    try:
        product = db_get_product(id)
        return send_file(product.icon)
    except Exception as e:
        print(e)
        abort(404)

@app.route('/product/<id>', methods=['PUT'])
def put_product(id):
    try:
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
        product = db_pop_product(id)
        return jsonify(to_scheme(id, product))
    except Exception as e:
        print(e)
        abort(404)

@app.route('/products', methods=['GET'])
def get_products():
    buffer = []
    for id, product in db.items():
        buffer.append(to_scheme(id, product))
    return jsonify(buffer)

if __name__ == '__main__':
    icons = os.path.join(os.getcwd(), 'icons')
    if not os.path.exists(icons):
        os.mkdir(icons)
    app.run(debug=True)

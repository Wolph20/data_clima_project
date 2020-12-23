from flask import Flask, request, jsonify, Response, render_template
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId
import requests

app = Flask(__name__)
# app.config['MONGO_URI'] = 'mongodb://localhost/pythonmongodb'
client = MongoClient('mongodb://mongodb:27017')
# client = MongoClient('mongodb://localhost:27017')
db= client.product_db

@app.route('/')
def Index():
    return jsonify({'msg': 'Bienvenido a MiDatabase'})

@app.route('/add_product', methods = ['POST'])
def add_product():

    product_name = request.json['product_name']
    planting_date = request.json['planting_date']
    temp_min = request.json['temp_min']
    temp_max = request.json['temp_max']
    altitud_min = request.json['altitud_min']
    altitud_max = request.json['altitud_max']
    precip_min = request.json['precip_min']
    precip_max = request.json['precip_max']
    humidity_min = request.json['humidity_min']
    humidity_max = request.json['humidity_max']
    
    
    if product_name:
        id = db.product.insert_one(
            {'product_name' : product_name, 'planting_date' : planting_date,
             'temp_min' : temp_min, 'temp_max' : temp_max, 'altitud_min' : altitud_min, 
             'altitud_max' : altitud_max, 'precip_min' : precip_min, 'precip_max' : precip_max, 
             'humidity_min' : humidity_min, 'humidity_max' : humidity_max}
        )
        response = {
            'id' : str(id),
            'product_name' : product_name, 
            'planting_date' : planting_date,
            'temp_min' : temp_min, 
            'temp_max' : temp_max, 
            'altitud_min' : altitud_min, 
            'altitud_max' : altitud_max,
            'precip_min' : precip_min, 
            'precip_max' : precip_max, 
            'humidity_min' : humidity_min,
            'humidity_max' : humidity_max
        }
    else:
        {'message':'received'}
    return {'message':'received'}

@app.route('/find_product', methods=['GET'])
def Get_product():
    product = db.product.find()
    response = json_util.dumps(product)
    
    return Response(response, mimetype = 'application/json')

@app.route('/product/<product_name>', methods=['GET'])
def Get_productByName(product_name):
    product = db.product.find_one({'product_name': product_name})
    response = json_util.dumps(product)
    return Response(response, mimetype = 'application/json')

@app.route('/del_product/<id>', methods=['GET'])
def del_product(id):
    db.product.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'Product deleted'})

@app.route('/update_product/<id>', methods=['PUT'])
def update_product(id):
    db.product.update_one({'_id': ObjectId(id)}, {'$set': {
        'product_name': request.json['product_name'],
        'planting_date': request.json['planting_date'],
        'temp_min': request.json['temp_min'],
        'temp_max': request.json['temp_max']
        
    }})
    
    return jsonify({'msg': 'Updated succesfully'})


from flask import Flask, request, json, jsonify, Response, render_template, session
from bson import json_util
import requests
import pandas as pd
from function import *
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def Index():
    return jsonify({'msg': 'Bienvenido a Microservicio'})

@app.route('/consume', methods=['POST'])
def consume():

    url = "http://148.247.201.227:5200/Clustering"

    lat1 = request.json['lat1']
    lat2 = request.json['lat2']
    lat3 = request.json['lat3']
    long1 = request.json['long1']
    long2 = request.json['long2']
    long3 = request.json['long3']
    fech_ini = request.json['fech_ini']
    fech_fin = request.json['fech_fin']
    crop = request.json['prod']
    
    session['lat1'] = lat1
    session['lat2'] = lat2
    session['lat3'] = lat3
    session['long1'] = long1
    session['long2'] = long2
    session['long3'] = long3
    session['fech_ini'] = fech_ini
    session['fech_fin'] = fech_fin
    session['prod'] = crop

    if crop:

        # Re = ConsumGeoposData(url, lat1, lat2, lat3, long1, long2, long3, fech_ini, fech_fin)
        b= "Cafe"
        url = "http://localhost:8000/product/{}".format(b) #crop

        response = requests.get(url)
        Re = json.loads(response.content)
        prod_data = {
            'product_name' : Re['product_name'],
            'planting_date' : Re['planting_date'],
            'temp_min' : float(Re['temp_min']),
            'temp_max' : float(Re['temp_max']),
            'precip_min' : float(Re['precip_min']),
            'precip_max' : float(Re['precip_max']),
            'humidity_min' : float(Re['humidity_min']),
            'humidity_max' : float(Re['humidity_max'])
        }
        
        with open('json_wolph.json') as file:
            pre_data = json.load(file)
        data = pre_data['results']
        
        geo_data = Extract_data(data)
        
        (dat, temp, hum) = Data_process(geo_data)
        
        dict_data = knowledge(dat,prod_data)
        response = {'results' : dict_data}
    
        return response

@app.route('/regression', methods=['GET'])
def regression():

    url = "http://148.247.201.227:5200/Clustering"

    lat1 = session['lat1']
    lat2 = session['lat2'] 
    lat3 = session['lat3']
    long1 = session['long1']
    long2 = session['long2']
    long3 = session['long3']
    fech_ini = session['fech_ini']
    fech_fin = session['fech_fin']
    crop = session['prod']
    
    if crop:

        # Re = ConsumGeoposData(url, lat1, lat2, lat3, long1, long2, long3, fech_ini, fech_fin)
        
        with open('json_wolph.json') as file:
            pre_data = json.load(file)
        data = pre_data['results']
        
        geo_data = Extract_data(data)
        
        (dat, temp, hum) = Data_process(geo_data)
        
        dict_data = temp
        response = {'results' : dict_data}
    
        return response

if __name__ == "__main__":
    app.run(port = 6654, debug=True)
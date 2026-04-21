from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.objectid import ObjectId                                                                  #gia na epistrepsei pragmata poy ns katalavainei to db
import numpy as np

app = Flask(__name__)                                                                               #efarmogi flask 
CORS(app)                                                                                           #adeia epikoinwnias me db

app.config["MONGO_URI"] = "mongodb://localhost:27017/WIS_Project"                                   #syndesi localhost me db

mongo = PyMongo(app)

@app.route('/like', methods =['POST'])                                                              #to rout einai POST gt allazei to db
def add_like():
    data = request.get_json()                                                                       #dictionery apo dedomena tou front 
    product_id = data.get('id')                                                                     #apo to dictionery pairnw to id

    if not product_id:
        return jsonify({'error' : 'Missing id'}), 400                                               #apantiseis se morfi jason an den edvse id
    
    try:
        apotelesma =  mongo.db.products.update_one(                                                 #entoli gia to db
            {'_id': ObjectId(product_id)},                                                          #search me to id pou phra
            {'$inc': {'likes' : 1}}                                                                 #ayjhsh twn like
        )

        if apotelesma.matched_count == 0:                                                           #an den brhka proion
            return jsonify({'error' : 'Product not found'}), 404
        
        return jsonify({'message' : 'Like added succesfully!'}), 200
    except:
        return jsonify({'error': str(Exception)}), 400                                              #ola ta 3 psifia einai outputs
    


@app.route('/popular', methods = ['GET'])
def popular_fives():
    
    top_products = mongo.db.products.find().sort('likes', -1).limit(5)                              # sort me basi ta like kai pairbw top 5

    lista_proiontwn = []

    for product in top_products:
        lista_proiontwn.append({
            'name' : product.get('name'),
            'image' : product.get('image'),
            'description' : product.get('description'),
            'likes': product.get('likes'),
            'price' : product.get('price')
        })
    return lista_proiontwn
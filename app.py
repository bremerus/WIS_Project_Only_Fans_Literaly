from flask import Flask, request, jsonify, render_template 
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.objectid import ObjectId                                                                  #gia na epistrepsei pragmata poy ns katalavainei to db
import numpy as np

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='/')                                                                       #efarmogi flask 
CORS(app)                                                                                           #adeia epikoinwnias me db

app.config["MONGO_URI"] = "mongodb://localhost:27017/WIS_Project"                                   #syndesi localhost me db
mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/items')
def items_page():
    return render_template('items.html')




@app.route('/search')
def search():
    query = request.args.get('query', '')
    # Ψάχνει στη βάση για το όνομα (query) χωρίς να κοιτάει κεφαλαία/πεζά
    products = mongo.db.products.find({"name": {"$regex": query, "$options": "i"}})
    
    results = []
    for p in products:
        results.append({
            "id": str(p['_id']),
            "name": p['name'],
            "price": p['price'],
            "image": p['image'],
            "description": p.get('description', ''), 
            "likes": p.get('likes', 0)
        })
    return jsonify(results)

@app.route('/like', methods =['POST'])                                                              #to rout einai POST gt allazei to db
def add_like():
    data = request.get_json()                                                                       #dictionery apo dedomena tou front 
    product_id = data.get('id')                                                                     #apo to dictionery pairnw to id
    print(f"DEBUG: Έλαβα like για το ID: {product_id}")

    if not product_id:
        return jsonify({'error' : 'Missing id'}), 400                                               #apantiseis se morfi jason an den edvse id
    
    try:

        try:
            from bson.objectid import ObjectId
            query = {'_id': ObjectId(product_id)}
        except:
            query = {'_id': product_id}

        apotelesma =  mongo.db.products.update_one(                                                 #entoli gia to db
            {'_id': ObjectId(product_id)},                                                          #search me to id pou phra
            {'$inc': {'likes' : 1}}                                                                 #ayjhsh twn like
        )

        if apotelesma.matched_count == 0:                                                           #an den brhka proion
            return jsonify({'error' : 'Product not found'}), 404
        
        return jsonify({'message' : 'Like added succesfully!'}), 200
    except Exception as e:
        print(f"DEBUG ERROR: {e}") # Εκτύπωση του σφάλματος στο τερματικό
        return jsonify({'error': str(e)}), 400

                                                    
    


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




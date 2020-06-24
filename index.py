import pymongo
import os
import sys
from flask import Flask, render_template, request, jsonify
from bson.json_util import dumps

MONGO_HOST = os.environ['MONGO_HOST']
MONGO_USER = os.environ['MONGO_USER']
MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
MONGO_PORT = os.environ['MONGO_PORT']
MONGO_DB_NAME = os.environ['MONGO_DB']

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/add")
def add():
	try:
		item = request.get_json()
		print(item)
		client = pymongo.MongoClient('mongodb://%s:%s@%s:%s' %(MONGO_USER, MONGO_PASSWORD,MONGO_HOST, MONGO_PORT))		
		db = client[MONGO_DB_NAME]
		collection = db["items"]		
		x = collection.insert_one(item)					
		return jsonify({"error": 0, "result": "OK"})
	except:
		print("Unexpected error:", sys.exc_info()[0])
		return jsonify({"error": 1, "result": "Unexpected error"}), 500

@app.route("/addall")
def addAll():
	try:
		items = request.get_json()		
		client = pymongo.MongoClient('mongodb://%s:%s@%s:%s' %(MONGO_USER, MONGO_PASSWORD,MONGO_HOST, MONGO_PORT))		
		db = client[MONGO_DB_NAME]
		collection = db["items"]		
		x = collection.insert_many(items)					
		return jsonify({"error": 0, "result": "OK"})
	except:
		print("Unexpected error:", sys.exc_info()[0])
		return jsonify({"error": 1, "result": "Unexpected error"}), 500

@app.route("/items")
def items():
	try:		
		client = pymongo.MongoClient('mongodb://%s:%s@%s:%s' %(MONGO_USER, MONGO_PASSWORD,MONGO_HOST, MONGO_PORT))		
		db = client[MONGO_DB_NAME]
		collection = db["items"]				
		itemsJson = dumps(collection.find())		
		return itemsJson		
	except:
		print("Unexpected error:", sys.exc_info()[0])
		return jsonify({"error": 1, "result": "Unexpected error"}), 500

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0")

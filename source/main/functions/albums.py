from flask import request, jsonify
from datetime import datetime
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['cosplay']
def getAllAlbum():
    try:
        data = request.form
        albums = list(db['albums'].find({'idModel':data['idModel']}))
        if albums:
           
            return jsonify({"data":albums})
        else:
            return jsonify({"status":200,"message":"No album"})
    except Exception as e:
        return jsonify({"status":404,"message":str(e)})
    
def createAlbum():
    try:
        data = request.form.to_dict()
        albums = db['albums']
        new_id = albums.count_documents({}) + 1
        data['_id'] = new_id
        albums.insert_one(data)
        return jsonify({"data":data})
    except Exception as e:
        return jsonify({"status":404,"message":str(e)})
from flask import request, jsonify,send_from_directory
import os
import uuid
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['cosplay']
UPLOAD_FOLDER = os.path.abspath('media')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
BASE_URL = 'http://127.0.0.1:5000'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def addImage():
    try:
        data = request.form.to_dict()
        album = db['albums'].find_one({'_id':int(data['idAlbum'])})
        idol = db['idols'].find_one({'_id':int(data['idModel'])})
        files = request.files.getlist('images') 
        if not files:
            return jsonify({"status": 400, "message": "No files provided"})
        if album and idol:
            for file in files:
                if file and allowed_file(file.filename):

                    file_extension = file.filename.rsplit('.', 1)[1].lower()
                    new_filename = f"{uuid.uuid4().hex}.{file_extension}"

                    idol_folder = os.path.join(UPLOAD_FOLDER, idol['name'])
                    album_folder = os.path.join(idol_folder, album['name'])

                    os.makedirs(album_folder, exist_ok=True)

                    file_path = os.path.join(album_folder, new_filename)
                    file.save(file_path)
                    image_url = f"{BASE_URL}/media/{idol['name']}/{ album['name']}/{new_filename}"
                else:
                    image_url = None
                id = db['images'].count_documents({}) + 1
                data['_id'] = id
                data['link'] = image_url
                db['images'].insert_one(data)
            
            return jsonify({"status":200,"message":"Add image successfull"})
        else:
            return jsonify({"status":400,"message":"One of idInput is not correct"})    
    except Exception as e:
        return jsonify({"status":404,"message":str(e)})
    
def viewImage(fileName,idolName,albumName):
    try:
        folder = os.path.join(UPLOAD_FOLDER, idolName, albumName)
        return send_from_directory(folder, fileName)
    except Exception as e:
        return jsonify({"status":404,"message":str(e)})
    
def getImageByAlbum():
    try:
        data = request.form
        images = list(db['images'].find({'idAlbum':data['idAlbum']}))
        if images:
            return jsonify({"status":200,"data":images})
        else:
            return jsonify({"status":200,"message":"idAlbum is not correct"})
    except Exception as e:
        return jsonify({"status":404,"message":str(e)})

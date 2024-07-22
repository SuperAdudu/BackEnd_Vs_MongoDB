from flask import jsonify,request, send_from_directory
from mongoengine import connect
import os
import re
import uuid
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['cosplay']

UPLOAD_FOLDER = os.path.abspath('media')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
BASE_URL = 'http://127.0.0.1:5000'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_valid_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(regex, email):
        return True
    else:
        return False

def registerUser():
    try:
        data = request.form.to_dict()
        file = request.files['avatar'] if 'avatar' in request.files else None
        if not is_valid_email(data['email']):
            return jsonify({"error": "Invalid email format!"})
        if file and allowed_file(file.filename):

            file_extension = file.filename.rsplit('.', 1)[1].lower()
            new_filename = f"{uuid.uuid4().hex}.{file_extension}"

            avatar_folder = os.path.join(UPLOAD_FOLDER, 'avatar')
            user_avatar_folder = os.path.join(avatar_folder, 'user')

            os.makedirs(user_avatar_folder, exist_ok=True)

            file_path = os.path.join(user_avatar_folder, new_filename)
            file.save(file_path)
            image_url = f"{BASE_URL}/media/avatar/user/{new_filename}"
        else:
            image_url = None
        
        data['avatar'] = image_url
        users = db['users']
        new_id = users.count_documents({}) + 1
        data['_id'] = new_id
        users.insert_one(data)
        return jsonify(data),200
    except Exception as e:
        return jsonify({"status":404,"error":str(e)})
    
def viewAvatarUser(fileName):
    try:
        folder = os.path.join(UPLOAD_FOLDER, 'avatar', 'user')
        return send_from_directory(folder, fileName)
    except Exception as e:
        return jsonify({"status":404,"message":str(e)})
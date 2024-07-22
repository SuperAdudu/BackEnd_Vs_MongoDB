from flask import request, jsonify, send_from_directory
import re,os,uuid
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['cosplay']

UPLOAD_FOLDER = os.path.abspath('media')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
BASE_URL = 'http://127.0.0.1:5000'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def addIdol():
    try:
        data = request.form.to_dict()
        file = request.files['avatar'] if 'avatar' in request.files else None
        if file and allowed_file(file.filename):

            file_extension = file.filename.rsplit('.', 1)[1].lower()
            new_filename = f"{uuid.uuid4().hex}.{file_extension}"

            avatar_folder = os.path.join(UPLOAD_FOLDER, 'avatar')
            user_avatar_folder = os.path.join(avatar_folder, 'idol')

            os.makedirs(user_avatar_folder, exist_ok=True)

            file_path = os.path.join(user_avatar_folder, new_filename)
            file.save(file_path)
            image_url = f"{BASE_URL}/media/avatar/idol/{new_filename}"
        else:
            image_url = None
        data['avatar'] = image_url
        idols = db['idols']
        new_id = idols.count_documents({}) + 1
        data['_id'] = new_id
        idols.insert_one(data)

        return jsonify({"status":200,"data":data})
    
    except Exception as e:
        return jsonify({"status":404,"error":str(e)})
    
def viewAvatarIdol(fileName):
    try:
        folder = os.path.join(UPLOAD_FOLDER, 'avatar', 'idol')
        return send_from_directory(folder, fileName)
    except Exception as e:
        return jsonify({"status":404,"message":str(e)})
    
def getAllIdols():
    try:
        idols = list(db['idols'].find())
        for idol in idols:
            idol['_id'] = str(idol['_id'])
        return jsonify({'status':200,'data':idols})
    except Exception as e:
        return jsonify({'status':404,'message':str(e)})
    
def changeAvatar():
    try:
        data = request.form
        idol = db['idols'].find_one({"_id":int(data['id'])})
        if not idol:
            return jsonify({"status":400,"message":"Id is not correct"})    
        file = request.files['avatar'] if 'avatar' in request.files else None
        if file and allowed_file(file.filename):

            file_extension = file.filename.rsplit('.', 1)[1].lower()
            new_filename = f"{uuid.uuid4().hex}.{file_extension}"

            avatar_folder = os.path.join(UPLOAD_FOLDER, 'avatar')
            user_avatar_folder = os.path.join(avatar_folder, 'idol')

            os.makedirs(user_avatar_folder, exist_ok=True)

            file_path = os.path.join(user_avatar_folder, new_filename)
            file.save(file_path)
            image_url = f"{BASE_URL}/media/avatar/idol/{new_filename}"
        else:
            image_url = None
        db['idols'].update_one({'_id':int(data['id'])},{'$set':{'avatar':image_url}})
        new_idol = db['idols'].find_one({"_id":int(data['id'])})
        return jsonify({"status":200,"data":new_idol})     
    except Exception as e:
        return jsonify({"status":404,"error":str(e)})
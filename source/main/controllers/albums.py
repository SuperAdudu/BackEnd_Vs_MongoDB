from source.main.functions.albums import *

def register_routes_albums(app):

    app.add_url_rule('/api/albums/get_all_idol_album',methods=["GET"],view_func=getAllAlbum)
    
    app.add_url_rule('/api/albums/create_album',methods=["POST"],view_func=createAlbum)
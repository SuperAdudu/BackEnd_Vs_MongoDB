from source.main.functions.images import *

def register_routes_images(app):

    app.add_url_rule('/api/images/add_image',methods=["POST"],view_func=addImage)

    app.add_url_rule('/media/<idolName>/<albumName>/<fileName>',view_func=viewImage)

    app.add_url_rule('/api/images/get_image_by_album',methods=["GET"],view_func=getImageByAlbum)
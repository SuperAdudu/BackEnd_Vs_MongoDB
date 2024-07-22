from source.main.functions.idols import *

def register_routes_idols(app):

    app.add_url_rule('/api/idols/get_all_idol',methods=["GET"],view_func=getAllIdols)

    app.add_url_rule('/api/idols/add_idol',methods=["POST"],view_func=addIdol)

    app.add_url_rule('/api/idols/change_avatar',methods=["POST"],view_func=changeAvatar)

    app.add_url_rule('/media/avatar/idol/<fileName>',view_func=viewAvatarIdol)
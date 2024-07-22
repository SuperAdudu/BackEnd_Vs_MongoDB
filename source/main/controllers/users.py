from source.main.functions.users import *

def register_routes_users(app):

    app.add_url_rule('/api/user/register',methods=["POST"],view_func=registerUser)

    app.add_url_rule('/media/avatar/user/<fileName>',view_func=viewAvatarUser)
from source.main.controllers.users import *
from source.main.controllers.idols import *
from source.main.controllers.albums import *
from source.main.controllers.images import *

def register_routes(app):
    register_routes_idols(app)
    register_routes_albums(app)
    register_routes_images(app)
    register_routes_users(app)
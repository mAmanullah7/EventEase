from flask import Flask,render_template
from applications.database import db
from applications.config import Config
from flask_login import LoginManager
from datetime import datetime 
from admin.admin_bp import admin_bp
from flask_restful import Api
from applications.api import *
from flask_cors import CORS

def create_app():
    '''
    Create an Flask app.
    Ensures that correct database and login managers are assigned to Flask app

    Returns:
        - Flask app
        - Login Manager 
    '''
    app = Flask(__name__) #__name__ give Flask an idea of what belongs to your application.
    app.config.from_object(Config) #Configuration setting for Flask Applications imported from Config.py 
    login_manager = LoginManager()
    db.init_app(app) 
    login_manager.init_app(app)
    api=Api(app)
    app.app_context().push()
    return app,login_manager,api

app,login_manager,api = create_app()
CORS(app)
login_manager.login_view='user_login'
login_manager.blueprint_login_views = {
    'admin': '/admin/login',
}
app.register_blueprint(admin_bp,url_prefix = "/admin")
api.add_resource(UserProfile, "/api/user/profile/<string:userID>")
api.add_resource(UserBooking, "/api/user/booking/<string:userID>")
api.add_resource(Venues, "/api/venues/admin/<string:userID>")
api.add_resource(Shows, "/api/shows/admin/<string:userID>")


from  applications.login import *
from applications.user_controller import *


if __name__ == '__main__':
    app.run()
from flask import Blueprint

from applications.database import db

admin_bp = Blueprint("admin",__name__,template_folder = 'admin_templates')


from admin.admin_applications.admin_login import *
from admin.admin_applications.admin_controllers import *




"""
Code permettant de définir l'acès aux routes concernant l'administration du site.
"""

from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

# Import des routes pour le blueprint admin
from app.admin import routes  
from app.admin import anonymous_comment_routes
from app.admin import anonymous_reply_routes
from app.admin import anonymous_subject_routes


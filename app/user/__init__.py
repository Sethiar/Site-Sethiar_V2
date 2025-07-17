"""
Code permettant de définir l'accès aux routes concernant les fonctions utilisateurs du site.
"""

from flask import Blueprint

user_bp = Blueprint('user', __name__)


# Import des routes pour le blueprint user
from app.user import routes  

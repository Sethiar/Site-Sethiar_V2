"""
Code permettant de définir l'accès aux routes concernant les fonctionalités de base du site.
"""

from flask import Blueprint

functional_bp = Blueprint('functional', __name__)

from app.functional import routes  # Import des routes pour le blueprint functional 

"""
Code permettant de définir l'acès aux routes concernant les fonctions d'authentificaion du site.
"""

from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from app.auth import routes  # Import des routes pour le blueprint auth




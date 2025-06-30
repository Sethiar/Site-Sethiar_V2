"""
Code permettant de définir l'accès aux routes concernant le frontend du site.
"""
from flask import Blueprint

frontend_bp = Blueprint('frontend', __name__)

from app.frontend import routes  # Import des routes pour le blueprint frontend
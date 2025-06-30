"""
Code permettant de définir l'acès aux routes concernant le chat du site.
"""

from flask import Blueprint

chat_bp = Blueprint('chat', __name__)
# Import des routes pour le blueprint chat

from app.chat import routes  


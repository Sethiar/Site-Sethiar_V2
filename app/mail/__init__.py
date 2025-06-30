"""
Code permettant de définir l'accès aux routes concernant le mailing du site.
"""

from flask import Blueprint

mail_bp = Blueprint('mail', __name__)

from app.mail import routes  # Import des routes pour le blueprint mail


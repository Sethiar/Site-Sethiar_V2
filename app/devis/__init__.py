"""
Code permettant de définir l'acès aux routes concernant les demandes de devis du site.
"""

from flask import Blueprint

devis_bp = Blueprint('devis', __name__)

from app.devis import routes  # Import des routes pour le blueprint devis
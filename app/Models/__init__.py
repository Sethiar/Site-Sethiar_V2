"""
Déclaration de la base de données pour le site SethiarWorks.
La base de données est configurée pour utiliser PostgreSQL.

L'instance 'db' est créée pour interagir avec la base de données
définie par les modèles SQLAlchemy.
"""

import logging

from flask_sqlalchemy import SQLAlchemy

# Instanciation de la base de données SQLAlchemy.
db = SQLAlchemy()

# Fonction pour fermer la session de la base de données.
def shutdown_session(exception=None):
    """
    Fonction pour fermer la session de la base de données.
    Elle est appelée lors de l'arrêt de l'application ou en cas d'exception.
    """
    db.session.remove()
    logging.info("Session de la base de données fermée.")


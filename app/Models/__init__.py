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


"""
Fichier permettnat d'insatller les tables de données de la base de postgreSQL db_sethiarworks.
"""

from app.Models import db

from app import create_app

app = create_app()


# L'installation des tables de données dans un contexte d'application.
with app.app_context():
    
    # Création de toutes les tables de données à partir de leur classe.
    db.create_all()

# Message de réussite.    
print("Félicitations, toutes les tables ont été installées.")

"""
Fichier qui va permettre de compiler le CSS.
"""

from app import create_app

app = create_app()

with app.app_context():
    # Récupération du bundle défini dans l'application.
    css_bundle = app.assets['scss_all']
    
    # Compilation les SCSS en CSS.
    css_bundle.build()
    
    print("Les fichiers SCSS ont été compilés avec succès.")
    
    
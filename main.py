""" 
fichier de lancement de l'application Site Entreprise SethiarWorks.
"""

import locale
import os

from flask import render_template, send_from_directory

from app import create_app


# Configuration de la localisation en français
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')  

app = create_app()

#-------------------------------------------------------------------
# Définition des pages prarticulières de l'application SethiarWorks.
#-------------------------------------------------------------------


# Route menant au favicon dans static.
@app.route('/logo_favicon.ico')
def favicon():
    """
    Sert le fichier favicon.png à partir du répertoire 'static'.
    """
    return send_from_directory(os.path.join(app.route_path, 'static'),
                               'logo_favicon.ico', mimetype='image/vnd.microsoft.icon')
    

# Route renvoyant l'erreur 404.
@app.errorhandler(404)
def page_not_found(error):
    """
    Renvoie une page d'erreur 404 en cas de page non trouvée.
    
    Args:
        error : l'erreur qui a declenché la page non trouvée.
        
    Returns:
        la page d'erreur 404. 
    """ 
    return render_template("error/404.html"), 404


# route renvoyant l'erreur 401.
def no_authenticated(error):
    """
    Renvoie une page d'erreur 401 en cas de non-authentification de l'utiliateur.
    
    Args:
        error : L'erreur déclenchée par la non-authentification.
    
    Returns:
        la page d'erreur 401.
    """
    return render_template("error/401.html"), 401


# Route affchant la page d'accuueil du site SethiarWorks.
@app.route('/')
def landing_page():
    """
    Page d'accueil du site entreprise de SethiarWorks.
    
    Returns:
        renvoie le fichier html de a page d'accueil du site.
    """
    return render_template('frontend/accueil.html')
    
    
# Lancement de l'application en développement.
if __name__ == '__main__':
    app.run(debug=True)
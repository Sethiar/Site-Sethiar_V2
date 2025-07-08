"""
code qui permet de charger les extensions de l'application.
"""

import os
import requests

# Chargement des variables d'environneemnt depuis le fichier .env
from dotenv import load_dotenv

load_dotenv()

# Fonction pour vérifier les extensions des imports.
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", 'pdf', 'docx', 'doc', 'txt'}


#-----------------------------------------------#
# Instanciation des extensions de l'application #
#-----------------------------------------------#

# Extensions nécessaires pour l'application.
from flask_assets import Environment
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_moment import Moment


# Initialisation des extensions.
mailing = Mail()
csrf = CSRFProtect()
login_manager = LoginManager()
assets = Environment()
moment = Moment()


# Fonctions générant l'autorisation des fichiers acceptés pour le site.
def allowed_file(filename):
    """
    Vérifie si le fichier a une extension autorisée.

    :param filename: Nom du fichier à vérifier.
    :return: True si l'extension est autorisée, False sinon.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#-----------------------------------------------#
# Code de création de l'API de visio conférence #
#-----------------------------------------------#

# Fonction générant le lien de l'API de visio conférence entre l'adminsitrateur et le client.
def create_whereby_meeting_admin():
    """
    Crée une réunion pour un administrateur et renvoie l'URL de la salle.

    Utilise l'API de Whereby pour créer une salle de réunion en spécifiant une date de fin et des champs à récupérer.

    Returns:
        str: URL de la salle d'hôte pour l'administrateur, ou None en cas d'erreur.
    """
    # Chargement des données secrètes depuis les variables d'environnement.
    API_KEY = os.getenv('WHEREBY_API_KEY')
    API_URL = os.getenv('API_URL')
    
    if not API_KEY or not API_URL:
       print("Erreur : Les variables d'environnement WHEREBY_API_KEY ou API_URL sont manquantes.")
       return None
    
    # Données pour la création de la salle de réunion.
    data = {
        "endDate": "2099-02-18T14:23:00.000Z",
        "fields": ["hostRoomUrl"]
    }
    
    # En-têtes HTTP avec l'authentification Bearer.
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Tests de la requête POST pour créer la réunion.
    try:
        # Envoi de la requête POST à l'API de whereby pour créer la réunion.
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()  # Vérifie si la requête a réussi
        
        # Afficher les détails de la réponse pour le débogage.
        print(f"Réponse de l'API : {response.status_code} - {response.text}")
        
        # Analyse de la réponse JSON pour obtenir l'URL de la salle d'hôte.
        if response.status_code not in [200, 201]:
            print(f"Erreur lors de la création de la réunion : {response.status_code} - {response.text}")
            
            return None 
        
        data = response.json()
        print("Room créée avec succès :", data.get("roomUrl"))
        
        # Récupération de l'URL de la salle d'hôte. 
        print("Données de la réponse :", data.get("hostRoomUrl"))
        
        # Renvoi de l'URL de la salle d'hôte.
        return data.get("hostRoomUrl")
    
    except requests.HTTPError as http_err:
        # Affichage de l'erreur HTTP spécifique et la réponse complète pour le debug.
        print(f"Erreur HTTP lors de la création de la réunion : {http_err}")
        
        # Affichage de la réponse complète pour le debug.
        print(f"Réponse complète : {response.text}")
        
        return None
    
    except requests.RequestException as e:
        
        # Affichage de toute autre erreur de requête.
        print(f"Erreur lors de la création de la réunion : {e}")
        
        return None

    

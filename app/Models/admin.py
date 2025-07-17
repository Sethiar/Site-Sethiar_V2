"""
Représente la classe Admin.
"""

#----------------------------------------------------------------
# Création d'une classe gérant les administrateurs.
#----------------------------------------------------------------


import logging


from flask_login import UserMixin

from . import db
from .base_model import BaseModel

# Modèle de la classe Admin.
class Admin(UserMixin, BaseModel):
    """
    Classe Admin qui représente un administrateur dans la base de données.
    
    Hérite de UserMixin pour intégrer les fonctionnalités de Flask-Login.
    
    Attributs:
        id (int): Identifiant unique de l'administrateur.
        username (str): Nom d'utilisateur de l'administrateur.
        role (str): Rôle de l'administrateur.
        password_hash (LB): Mot de passe de l'administrateur hashé.
        salt (LB): Sel utilisé pour le hachage du mot de passe.        
    """
    
    __tablename__ = 'admin'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False, default='SuperAdmin')
    password_hash = db.Column(db.LargeBinary(255), nullable=False)
    salt = db.Column(db.LargeBinary(255), nullable=False)
    
    # Relation avec la table ChatRequest
    chat_request = db.relationship('ChatRequest', back_populates='admin', cascade='all, delete-orphan')
    

    
    #=========================================================#
    # Fonction qui représente l'objet en chaîne de caractères #
    #=========================================================#
    
    def __repr__(self):
        """
        Représentation de l'objet Admin.
        Retourne une chaîne de caractères représentant l'administrateur.
        
        Returns:
            str: Représentation de l'administrateur.
        """
        return f"<Admin (id='{self.id}', pseudo='{self.pseudo}', role='{self.role}')>"
    
    
    #====================================================================#
    # Fonctions utilisées par Flask-Login pour gérer l'authentification  #  
    #====================================================================#
        
    # Fonction qui permet de vérifier si l'administrateur est actif ou non.
    def is_active(self):
        """
        Vérifie si l'administrateur est actif.
        
        Returns:
            bool: Toujours True, car les administrateurs sont toujours actifs.
        """
        logging.debug(f"Checking if admin {self.pseudo} is active.")
        # Dans ce cas, on considère que tous les administrateurs sont actifs.
        return True
    
    
    # Fonction qui permet de vérifier si l'administrateur est anonyme ou non.
    def is_anonymous(self):
        """
        Vérifie si l'administrateur est anonyme.
        
        Returns:
            bool: Toujours False, car les administrateurs ne sont pas anonymes.
        """
        logging.debug(f"Checking if admin {self.pseudo} is anonymous.")
        return False
    
    
    # Fonction qui permet de vérifier si l'administrateur est authentifié ou non.
    def get_id(self):
        """
        Retourne l'identifiant de l'administrateur.
        Returns:
            int: Identifiant de l'administrateur.
        """
        logging.debug(f"Getting ID for admin {self.pseudo}.")
        # Utilisation de super() pour appeler la méthode get_id de UserMixin
        return str(self.id)
    
    
    # Fonction qui permet de vérifier si l'administrateur a un rôle spécifique.
    def has_role(self, role):
        """
        Vérifie si l'administrateur a un rôle spécifique.
        
        Args:
            role (str): Le rôle à vérifier.
        
        Returns:
            bool: True si l'administrateur a le rôle spécifié, False sinon.
        """
        logging.debug(f"Checking if admin {self.pseudo} has role {role}.")
        return self.role == role
    
    
    # Fonction qui permet de vérifier si l'administrateur est un super administrateur.
    def is_admin(self):
        """
        Vérifie si l'administrateur est un super administrateur.
        
        Returns:
            bool: True si l'administrateur est un super administrateur, False sinon.
        """
        logging.debug(f"Checking if admin {self.pseudo} is a super admin.")
        return self.role == 'SuperAdmin'
    #----------------------------------------------------------------
    
    # Fin des fonctions utilisées par Flask-Login pour gérer l'authentification pour les administrateurs du site.
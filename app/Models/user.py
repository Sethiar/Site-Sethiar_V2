"""
Modèle de la classe utilisateur.
"""

#----------------------------------------------------------------------------------------------
# Création d'une classe gérant les utilisateurs.
#----------------------------------------------------------------------------------------------
 

import bcrypt
import logging

from flask_login import UserMixin
from .import db


from datetime import datetime, timedelta

# Modèle de la classe Utilisateur.
class User(db.Model, UserMixin):
    """
    Modèle de données représentant un utilisateur de l'application.

    Attributes:
        id (int) : Identifiant unique de l'utilisateur.
        lastname (str): Nom du client.
        firstname (str): Prénom du client.
        enterprise_name (str): Nom de l'entreprise client.
        role (str) : Rôle de l'utilisateur.
        phone (str): Téléphone du client.
        email (str) : Adresse e-mail de l'utilisateur.
        password_hash (LB) : Mot de passe hashé de l'utilisateur.
        salt (bytes) : Salage du mot de passe.
        profil_photo (bytes) : Photo de profil de l'utilisateur en format binaire.
        
    """

    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(30), nullable=False)
    firstname = db.Column(db.String(30), nullable=False)
    enterprise_name = db.Column(db.String(30), nullable=False)
    role = db.Column(db.String(30), default='Utilisateur')
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.LargeBinary(255), nullable=False)
    salt = db.Column(db.LargeBinary(255), nullable=False)
    profil_photo = db.Column(db.LargeBinary, nullable=False)
    chemin_photo = db.Column(db.String(255), nullable=True)

    # Relation avec les commentaires des clients.
    customer_comments = db.relationship('CustomerComment', back_populates='user', cascade='all, delete-orphan')

    # Relation avec les réponses aux commentaires.
    comment_replies = db.relationship('CommentReply', back_populates='user', cascade='all, delete-orphan')
    #----------------------------------------------------------------------------------------------
    
    
    #----------------------------------------------------------------------------------------------
    # Fonction qui représente l'objet en chaîne de caractères.
    #----------------------------------------------------------------------------------------------
    def __repr__(self):
        """
        Représentation de l'objet Utilisateur.
        Retourne une chaîne de caractères représentant l'utilisateur.

        Returns :
            str: Chaîne représentant l'objet Utilisateur.
        """
        return (f"<User(id='{self.id}', lastname='{self.lastname}', firstname='{self.firstname}', \
            enterprise_name='{self.enterprise_name}',  role='{self.role}', phone='{self.phone}', \
            email='{self.email}', chemin_photo='{self.chemin_photo}', >")
    #---------------------------------------------------------------


    #----------------------------------------#
    # Fonction qui redéfinit un mot de passe #
    #----------------------------------------#
    
    def set_password(self, new_password):
        """
        Redéfinit le mot de passe de l'utilisateur.

        Args:
            new_password (str) : Le nouveau mot de passe de l'utilisateur.
        """
        self.password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        db.session.add(self)
        db.session.commit()
    #---------------------------------------------------------------    


    #----------------------------------------------------------------------------------------------
    # Fonctions utilisées par Flask-Login pour gérer l'authentification.    
    #----------------------------------------------------------------------------------------------
    
    # Fonction qui vérife l'authentification de l'utilisateur.
    @property
    def is_authenticated(self):
        """
        Indique si l'utilisateur est authentifié.
        L'utilisateur est considéré authentifié s'il a un pseudo non vide.

        Returns:
            bool: True si l'utilisateur a un pseudo, False sinon.
        """
        # Vérifie que le pseudo existe et n'est pas vide
        return bool(self.email)
    
    
    # Fonction qui permet de vérifier si l'administrateur est actif ou non.
    def is_active(self):
        """
        Vérifie si l'utilisateur est actif.
        
        Returns:
            bool: Toujours True, car les utilsiateurs sont toujours actifs.
        """
        logging.debug(f"Checking if user {self.enterprise_name} is active.")
        # Dans ce cas, on considère que tous les utilisateurs sont actifs.
        return True
    
    
    # Fonction qui vérifie que l'utilisateur est anonyme.
    def is_anonymous(self):
        """
        Indique si l'utilisateur est anonyme.

        Returns :
            bool : False car l'utilisateur n'est jamais anonyme.
        """
        return False
    
    
    # Fonction qui permet de récupérer l'id de l'utilisateur authentifié.
    def get_id(self):
        """
        Récupère l'identifiant de l'utilisateur.

        Returns :
            str : L'identifiant de l'utilisateur.
        """
        return str(self.id)


    # Fonction qui vérifie le rôle de l'utilisateur.
    def has_role(self, role):
        """
        Récupère le rôle de l'utilisateur.

        :param role: le rôle de l'utilisateur.
        :return:
        """
        return self.role == role
#----------------------------------------------------------------------------------------------

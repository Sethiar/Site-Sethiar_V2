"""
Classe permettant de créer l'objet "sujet" de l'espace de commentaires.
"""

#========================================#
#   Modèle de table de données "Sujet"  #
#========================================#


import logging

from .base_model import BaseModel
from enum import Enum

# Fonction qui va permettre de gérer les status des sujets créés par les utilisateurs anonymes.
class SubjectStatus(Enum):
    """
    Enumération des status possibles pour un sujet d'anonyme.
    
    Attributes:
        VALIDE (str): Sujet validé.
        EN_ATTENTE (str): Sujet en attente de modération.
        REFUSE (str): Sujet refusé par l'administrateur.
    """
    VALIDE = "Validé"
    EN_ATTENTE = "En attente"
    REFUSE = "Refusé"
    

from . import db
from datetime import datetime


# Modèle de la classe représentant les sujets anonymes de l'espace de comemtaires.
class Subject(BaseModel):
    """
    Modèle de données représentant les sujets de l'espace de commentaires.
    
    Attributes:
        id (int): Identifiant unique du sujet pour l'espace de commentaires.
        name (str): Nom du sujet de l'espace de commentaires.
        author (str): Nom de l'auteur du sujet. Anonyme par défaut.
        created_at (Datetime): Date de la création du sujet.
    """
    
    __tablename__ = "subject"
    __table_args__ = {"extend_existing": True}
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    
    # Auteur : si connecté, stockage de l'user_id, sinon author_enterprise_name et is_anonyme à True.
    author_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    author_enterprise_name = db.Column(db.String(50), nullable=True)
    is_anonymous = db.Column(db.Boolean, default=False, nullable=False)
    
    # Gestion du statut.
    status=db.Column(db.Enum(SubjectStatus), nullable=False, default=SubjectStatus.EN_ATTENTE)
    
    # Date de création 
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    # Relation avec la table comment.
    comments = db.relationship(
        'Comment', 
        back_populates='subject', 
        cascade='all, delete-orphan'
        )
    
    
    # Methode statique qui va gérer l'authentification ou non de l'utilisateur.
    @staticmethod
    def create(name, user=None, author_enterprise_name=None):
        """
        Factory method pour créer un sujet avec gestion de statut admapté selon l'auteur.
        
        Le statut est automatiquement réglé :
            - VALIDE si l'utilisateur est connecté
            - EN_ATTENTE sinon (anonyme)
    
        Args:
            name (str): Nom du sujet.
            user (User, optional): Instance utilisateur connecté, ou None si anonyme.
            enterprise_name (str, optional): Nom de l'entreprise pour un sujet anonyme. Par défaut None.

        Returns:
            Subject: Instance de Subject créée (non commitée).
        """
        
        is_anon = user is None
        status = SubjectStatus.VALIDE if not is_anon else SubjectStatus.EN_ATTENTE
        
        # Si l'utilisateur est connecté on renvoie le nom de l'entreprise.
        if user:
            author_enterprise_name = user.enterprise_name if user.enterprise_name else f"{user.firstname} {user.lastname}"
            author_user_id = user.id
        else:
            author_enterprise_name = author_enterprise_name if author_enterprise_name else "Anonyme"
            author_user_id = None
        
        return Subject(
            name=name,
            author_user_id=author_user_id,
            author_enterprise_name=author_enterprise_name,
            is_anonymous=is_anon,
            status=status,
        )
        
    # Fontion récupérant l'auteur du sujet.
    @property
    def author_display(self):
        
        """
        Renvoie le nom de l’auteur du sujet : soit le nom d'entreprise saisi soit l'anonymat de l'auteur.
        """
        if self.is_anonymous or not self.author_enterprise_name:
            return "Anonyme"
        else:
            return f"{self.author_enterprise_name}"
        
    
    #==============================================================#
    #  Représentation en chaîne de caractères de  l'objet Subject  #
    #==============================================================#
    
    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet Subject.
        
        Returns:
            str: Chaîne représentant l'objet Subject.
        """
        return f"<Subject(name='{self.name}', author='{self.author_enterprise_name}', created_at='{self.created_at}')>"
    
    
    #===================================================================#
    # Fonctions relatives à la validation, le rejet d'un sujet anonyme  #
    #===================================================================#

    # Fonction qui permet de convertir l'objet SubjectAnonymous en dictionnaire.
    def to_dict(self):
        """
        Convertit l'object Subject en dictionnaire.
        
        Returns:
            dict: Dictionnaire représentant l'object Subject.
        """
        data = {
            "id": self.id,
            "name": self.name,
            "author": self.author_enterprise_name,
            "status": self.status.value,
            "created_at": self.created_at.isoformat()
            }
        return data
    
    # Fonction qui permet de valider le sujet d'un anonyme.
    def validate(self):
        """
        Accepte le sujet anonyme en changeant son statut à "Validé".
        
        """
        # Mise à jour du statut du sujet anonyme.
        self.status = SubjectStatus.VALIDE
        db.session.commit()
        
        logging.info(f"Sujet anonyme {self.name} validé avec succès.")
        
        
    # Fonction qui permet de rejeter un sujet et de le supprimer de la base de données.
    def reject(self):
        """
        Rejette le sujet en changeant son statut à "Rejeté" et le supprime.
        
        """
        # Mise à jour du statut du sujet anonyme.
        self.status = SubjectStatus.REFUSE
        # Suppression du sujet.
        db.session.delete(self)
        # Enregistrement dans la base de données.
        db.session.commit()
        
        logging.info(f"Sujet anonyme {self.name} rejeté et supprimé avec succès.")
        
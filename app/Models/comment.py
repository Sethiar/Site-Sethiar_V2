"""
Modèle représentant les commentaires d'un utilisateur anonyme ou non.
"""

#==================================#
#   Modèle de la classe "Comment"  #
#==================================#

import logging

from .base_model import BaseModel
from enum import Enum


# Fonction qui va permettre de gérer les statuts des commentaires anonymes.
class CommentStatus(Enum):
    """
    Enumération des statuts possibles pour un commentaire anonyme.
    
    Attributs:
        VALIDE (str): Commentaire validé.
        EN_ATTENTE (str): Commentaire en attente de modération.
        REFUSE (str): Commentaire refusé par l'administrateur.
    """
    VALIDE = "Validé"
    EN_ATTENTE = "En attente"
    REFUSE = "Refusé"


from . import db
from datetime import datetime


# Modèle de la classe AnonymousComment.
class Comment(BaseModel):
    """
    Représente un commentaire laissé par un utilisateur anonyme ou non sur l'espace de commentaire du site.
    
    Attributes:
        id (int): Identification unique du commentaire.
        comment_content (str): Contenu du commentaire.
        comment_date (datetime): Date et heure du commentaire.
        status (str): Statut du commentaire (par exemple, 'Validé', 'En attente', 'Refusé').
        subject_id (int): Identifiant du sujet associé au commentaire.
        subject (Comments): Relation avec la table de commentaires.
        anonymous_id (str): Identifiant de l'utilisateur anonyme, s'il n'est pas connecté.
        replies_anonymous (list): Réponses associées à ce commentaire.
    """
    
    __tablename__ = "comment"
    __table_args__ = (
        db.Index('idx_anonymous_comment_anonymous_id', 'anonymous_id'),
        {"extend_existing": True}
    )
    
    id = db.Column(db.Integer, primary_key=True)
    comment_content = db.Column(db.Text(), nullable=False)
    comment_date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    status=db.Column(db.Enum(CommentStatus), nullable=False, default=CommentStatus.EN_ATTENTE)
    
    # Relation avec la classe Subject.
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    subject = db.relationship('Subject', back_populates='comments')
    
    # Auteur connecté (nullable)
    author_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    author_enterprise_name = db.Column(db.String(50), nullable=False)
    author_user = db.relationship('User', back_populates='comments')
    
    # Auteur anonyme (nullable)
    anonymous_id = db.Column(db.String(36), nullable=True)
    
     # Booléen pour savoir si c’est un commentaire anonyme (optionnel)
    is_anonymous = db.Column(db.Boolean, nullable=False, default=False)
    
    # Relation avec la classe ReplyComment avec suppression en cascade -- Réponse : utilisateur à utilisateur.
    replies = db.relationship('ReplyComment', back_populates='comment', cascade='all, delete-orphan')
    
    # Relation avec la classe ReplyAnonymousUserComment avec suppression en cascade -- Réponse anonyme à utilisateur.
    replies_anonymous_user = db.relationship('ReplyAnonymousUserComment', back_populates='comment', cascade='all, delete-orphan')
    
    # Relation avec la classe ReplyUserAnonymousComment avec suppression en cascade -- Réponse utilisateur à anonyme.
    replies_user_anonymous = db.relationship('ReplyUserAnonymousComment', back_populates='comment', cascade='all, delete-orphan')
    
    # Relation avec la classe ReplyAnonymousComment avec suppression en cascade -- Réponse anonyme à anonyme.
    replies_anonymous_anonymous = db.relationship('ReplyAnonymousComment', back_populates='comment', cascade='all, delete-orphan')

    
    # Methode statique qui va gérer l'authentification ou non de l'utilisateur.
    @staticmethod
    def create(comment_content, subject, user=None, author_enterprise_name=None, anonymous_id=None):
        """
        Factory method pour créer un commentaire avec statut adapté selon l'auteur.
        
        Cette méthode crée un nouvel objet `Comment` avec un statut automatiquement défini :
            - `VALIDE` si l'auteur est un utilisateur connecté.
            - `EN_ATTENTE` si l'auteur est anonyme.
    
        Args:
            comment_content (str): contenu du commentaire.
            subject (Subject): instance du sujet associé.
            user (User or None): utilisateur connecté, sinon None.
            author_enterprise_name (str or None): nom entreprise si anonyme.
            anonymous_id (str or None): identifiant anonyme si anonyme.
    
        Returns:
            Comment: instance créée (non commitée).
        """
        
        is_anon = user is None
        status = CommentStatus.VALIDE if not is_anon else CommentStatus.EN_ATTENTE
        
        if user:
            author_enterprise_name = user.enterprise_name if user.enterprise_name else f"{user.enterprise_name}"
            author_user_id = user.id
        else:
            author_enterprise_name = author_enterprise_name if author_enterprise_name else "Anonyme"
            author_user_id = None
    
        return Comment(
            comment_content=comment_content,
            subject=subject,
            author_user_id=author_user_id,
            author_enterprise_name=author_enterprise_name,
            anonymous_id=anonymous_id if is_anon else None,
            is_anonymous=is_anon,
            status=status
        )
        
        
    #===================================================#
    #  Représentation en str d'une instance de Comment  #
    #===================================================#
    
    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet Comment.
        
        Returns:
            str: Chaîne représentant l'objet Comment avec son Id, son contenu sa date, son statut ainsi que le sujet auquel il est associé.
        """
        return f"<Comment (id: {self.id}, content: {self.comment_content[:20]}..., \
                date: {self.comment_date}, status: {self.status.value}, subject_id: {self.subject_id})>"
    
    
    #=========================================================================#
    # Fonctions relatives à la validation, le rejet d'un commentaire anonyme  #
    #=========================================================================#

    # Fonction qui permet de convertir l'objet Comment en dictionnaire.
    def to_dict(self):
        """
        Convertit l'objet Comment en dictionnaire.

        Returns:
            dict: Dictionnaire représentant l'objet Comment.
        """
        data = {
            "id": self.id,
            "comment_content": self.comment_content,
            "comment_date": self.comment_date.isoformat() if self.comment_date else None,
            "status": self.status.value,
            "subject_id": self.subject_id,
            "author_user_id": self.author_user_id,
            "author_enterprise_name": self.author_enterprise_name,
            "anonymous_id": self.anonymous_id,
            "is_anonymous": self.is_anonymous,
            }
        
        # Ajout le nom de l'auteur du sujet.
        if self.author_user:
            data["author_name"] = f"{self.author_enterprise_name}"
       
        else:
            data["author_name"] = "Anonyme"

        return data

    # Fonction qui permet de valider un commentaire anonyme.
    def validate(self):
        """
        Accepte le commentaire anonyme en changeant son statut à 'Validé'.
    
        """
        # Mise à jour du statut du commentaire anonyme.
        self.status = CommentStatus.VALIDE
        db.session.commit()
            
        logging.info(f"Commentaire anonyme {self.id} validé avec succès.")
    

    # Fonction qui permet de rejeter un commentaire anonyme et de le supprimer de la base de données Comment.
    def reject(self):
        """
        Rejette le commentaire anonyme en changeant son statut à 'Refusé' et le supprime de la base de données.
    
        """
        # Mise à jour du statut du commentaire anonyme.    
        self.status = CommentStatus.REFUSE
        db.session.delete(self)
        db.session.commit()
    
        logging.info(f"Commentaire anonyme {self.id} rejeté.")
    
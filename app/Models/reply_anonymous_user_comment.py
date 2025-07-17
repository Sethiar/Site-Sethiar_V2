"""
Classe représentant une réponse d'un utilisateur anonyme à un commentaire d'utilisateur authentifié
"""


#===============================================#
# Modèle de la classe ReplyAnonymousUserComment #
#===============================================#
import logging

from .base_model import BaseModel
from enum import Enum


# Fonction qui va permettre de gérer les statuts des réponses anonymes aux commentaires d'authentifiés.
class ReplyAnonymousUserCommentStatus(Enum):
    """
    Enumération des statuts possibles pour une réponse anonyme à un commentaire d'utilisateur authentifié.
    
    Attributs:
        VALIDEE (str): Réponse validée.
        EN_ATTENTE (str): Réponse en attente de validation.
        REFUSEE (str): Réponse refusée par l'administrateur.
    """
    VALIDEE = "Validée"
    EN_ATTENTE = "En attente"
    REFUSEE = "Refusée"
    
    
from . import db
from datetime import datetime


# Modèle de la classe ReplyAnonymousUserComment.
class ReplyAnonymousUserComment(BaseModel):
    """
    Représente une réponse d'un utilisateur anonyme à un commentaire d'utilisateur authentifié.
    
    Attributes:
        id (int): Identifiant unique de la réponse.
        anonymous_id (str): Identifiant de l'utilisateur anonyme.
        reply_content (str): Contenu de la réponse.
        reply_date (datetime): Date et heure de la réponse.
        status (str): Statut de la réponse (par exemple, 'Validée', 'En attente', 'Refusée').
        customer_comment_id (int): Identifiant du commentaire d'utilisateur authentifié auquel la réponse est associée.
        customer_comment (CustomerComment): Relation avec le commentaire d'utilisateur authentifié.
    """
    
    __tablename__ = "reply_anonymous_user_comment"
    __table_args__ = (
        db.Index('idx_reply_anonymous_user_comment_comment_id', 'comment_id'),
        {"extend_existing": True}
    )

    id = db.Column(db.Integer, primary_key=True)
    anonymous_id = db.Column(db.String(36), nullable=False)
    reply_content = db.Column(db.Text(), nullable=False)
    reply_date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    
    # Modération possible
    status = db.Column(db.Enum(ReplyAnonymousUserCommentStatus), nullable=False, default=ReplyAnonymousUserCommentStatus.EN_ATTENTE)
    
    # Relation avec la classe Comment.
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
    
    comment = db.relationship('Comment', back_populates='replies_anonymous_user')
    
    
    #=============================================================================#
    # Représentation en chaîne de caractères de l'objet ReplyAnonymousUserComment #
    #=============================================================================#

    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet ReplyAnonymousUserComment.
        """
        return f"<ReplyAnonymousUserComment (id: {self.id}, content: {self.reply_content[:20]}..., \
            status: {self.status.value})>"
            
            
    #==========================================================================#
    # Création d'un dictionnaire pour les données de ReplyAnonymousUserComment #
    #==========================================================================#

    def to_dict(self):
        """
        Convertit l'objet ReplyAnonymousUserComment en dictionnaire.
        
        Returns:
            dict: Dictionnaire représentant l'objet avec ses attributs.
        """
        data = {
            "id": self.id,
            "anonymous_id": self.anonymous_id,
            "reply_content": self.reply_content,
            "reply_date": self.reply_date.isoformat() if self.reply_date else None,
            "status": self.status.value,
            "comment_id": self.comment_id
        }
        return data       
     
    #======================================================================================================#
    # Fonctions relatives à la validation, le rejet d'une réponse anonyme à un commentaire d'authentifiés  #
    #======================================================================================================#        
            
    # Fonction qui permet de valider une réponse anonyme à un commentaire d'utilisateur authentifié.
    def validate(self):
        """
        Valide la réponse anonyme à un commentaire d'utilisateur authentifié en changeant son statut à 'Validée'.
        
        Returns:
            None
        """
        # Mise à jour du statut de la réponse anonyme.
        self.status = ReplyAnonymousUserCommentStatus.VALIDEE
        db.session.commit()
        
        logging.info(f"Réponse anonyme à un commentaire d'utilisateur authentifié {self.id} validée avec succès.")
    
    
    # Fonction qui permet de rejeter une réponse anonyme à un commentaire d'utilisateur authentifié. 
    def reject(self):
        """
        Rejette la réponse anonyme à un commentaire d'utilisateur authentifié en changeant son statut à 'Refusée'.
        
        Returns:
            None
        """
        # Mise à jour du statut de la réponse anonyme.
        self.status = ReplyAnonymousUserCommentStatus.REFUSEE
        db.session.commit()
        
        logging.info(f"Réponse anonyme à un commentaire d'utilisateur authentifié {self.id} rejetée avec succès.")  
        
        
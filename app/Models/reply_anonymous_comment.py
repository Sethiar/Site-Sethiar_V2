"""
Modèle représentant les réponses aux commentaires d'un utilisateur anonyme. 
"""


#===========================================#
# Modèle de la classe ReplyAnonymousComment #
#===========================================#

import logging
from .base_model import BaseModel
from enum import Enum


# fonction qui va permettre de gérer les statuts des réponses anonymes aux anonymes.
class ReplyAnonymousCommentStatus(Enum):
    """
    Enumération des statuts possibles pour une réponse anonyme à un commentaire anonyme.
    
    Attributs:
        VALIDE (str): Réponse validée.
        EN_ATTENTE (str): Réponse en attente de validation.
        REFUSE (str): Réponse refusée par l'administrateur.
    """
    VALIDEE = "Validée"
    EN_ATTENTE = "En attente"
    REFUSEE = "Refusée"


from . import db
from datetime import datetime


# Modèle de la classe ReplyAnonymousComment.
class ReplyAnonymousComment(BaseModel):
    """
    Représente une réponse à un commentaire laissé par un utilisateur anonyme.

    Attributes:
        id (int): Identifiant unique de la réponse.
        anonymous_id (str): Identifiant de l'utilisateur anonyme, s'il n'est pas connecté.
        reply_content (str): Contenu de la réponse.
        reply_date (datetime): Date et heure de la réponse.
        status (str): Statut de la réponse (par exemple, 'Validée', 'En attente', 'Refusée').
        anonymous_comment_id (int): Identifiant du commentaire anonyme auquel la réponse est associée.
        anonymous_comment (AnonymousComment): Relation avec le commentaire anonyme.
    """

    __tablename__ = "reply_anonymous_comment"
    __table_args__ = (
        db.Index('idx_reply_anonymous_comment_comment_id', 'comment_id'),
        {"extend_existing": True}
    )

    id = db.Column(db.Integer, primary_key=True)
    anonymous_id = db.Column(db.String(36), nullable=False)
    reply_content = db.Column(db.Text(), nullable=False)
    reply_date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    status = db.Column(db.Enum(ReplyAnonymousCommentStatus), nullable=False, default=ReplyAnonymousCommentStatus.EN_ATTENTE)
    
    # Relation avec la classe Comment.
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
    comment = db.relationship('Comment', back_populates='replies_anonymous_anonymous')


    #=================================================================#
    #  Représentation en str d'une instance de ReplyAnonymousComment  #
    #=================================================================#
    
    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet ReplyAnonymousComment.
        
        Returns:
            str: Représentation de l'objet avec son ID, son contenu et son statut.
        """
        return f"<ReplyAnonymousComment (id: {self.id}, content: {self.reply_content[:20]}..., \
                status: {self.status})>"
                
    
    #======================================================================================================#
    # Fonctions relatives à la validation et au rejet des réponses anonymes  à des commentaires d'anonymes #
    #======================================================================================================#
    
    # Fonction qui permet de convertir l'objet ReplyAnonymousComment en dictionnaire.
    def to_dict(self):
        """
        Convertit l'objet ReplyAnonymousComment en dictionnaire.

        Returns:
            dict: Dictionnaire représentant l'objet ReplyAnonymousComment.
        """
        data = {
            "id": self.id,
            "anonymous_id": self.anonymous_id,
            "reply_content": self.reply_content,
            "reply_date": self.reply_date.isoformat(),
            "status": self.status.value,
            "anonymous_comment_id": self.anonymous_comment_id
            }
        return data
    
    # Fonction qui permet de valider une réponse anonyme à un commentaire anonyme.
    def validate(self):
        """
        Valide la réponse anonyme à un commentaire anonyme en changeant son statut à 'Validée'.

        Returns:
            None
        """
        # Mise à jour du statut de la réponse anonyme.
        self.status = ReplyAnonymousCommentStatus.VALIDEE
        db.session.commit()
        
        logging.info(f"Réponse anonyme à un commentaire anonyme {self.id} validée avec succès.")
        
        
    # Fonction qui permet de rejeter une réponse anonyme à un commentaire anonyme.
    def reject(self):
        """
        Rejette la réponse anonyme à un commentaire anonyme en changeant son statut à 'Refusée'.

        Returns:
            None
        """
        # Mise à jour du statut de la réponse anonyme.
        self.status = ReplyAnonymousCommentStatus.REFUSEE
        db.session.commit()
        
        logging.info(f"Réponse anonyme à un commentaire anonyme {self.id} rejetée avec succès.")    
        
        
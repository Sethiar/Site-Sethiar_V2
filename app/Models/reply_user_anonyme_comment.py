"""
Classe représentant une réponse d'un utilisateur connecté à un commentaire d'anonyme.
"""

#===============================================#
# Modèle de la classe ReplyUserAnonymousComment #
#===============================================#

from .base_model import BaseModel
    
from . import db
from datetime import datetime


# Modèle de la classe ReplyUserAnonymousComment.
class ReplyUserAnonymousComment(BaseModel):
    """
    Représente une réponse d'un utilisateur authentifié à un commentaire d'utilisateur anonyme.
    
    Attributes:
        id (int): Identifiant unique de la réponse.
        user_id (str): Identifiant de l'utilisateur authentifié.
        reply_content (str): Contenu de la réponse.
        reply_date (datetime): Date et heure de la réponse.
        comment_id (int): Identifiant du commentaire d'utilisateur anonyme auquel la réponse est associée.
        comment (Comment): Relation avec le commentaire d'utilisateur anonyme.
    """
    
    __tablename__ = "reply_user_anonymous_comment"
    __table_args__ = (
        db.Index('idx_reply_user_anonymous_comment_comment_id', 'comment_id'),
        {"extend_existing": True}
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reply_content = db.Column(db.Text(), nullable=False)
    reply_date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    
    # Relation avec la classe Comment.
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
    comment = db.relationship('Comment', back_populates='replies_user_anonymous')
    
    # Relation avec la classe de l'utilisateur.
    user = db.relationship('User', back_populates='replies_user_anonymous')


    
    #=============================================================================#
    # Représentation en chaîne de caractères de l'objet ReplyUserAnonymousComment #
    #=============================================================================#

    def __repr__(self):
        return f"<ReplyUserAnonymousComment(id={self.id}, user_id={self.user_id}, comment_id={self.comment_id})>"
    
    
    #==========================================================================#
    # Création d'un dictionnaire pour les données de ReplyUserAnonymousComment #
    #==========================================================================#
    
    def to_dict(self):
        """
        Convertit l'objet ReplyUserAnonymousComment en dictionnaire.
        
        Returns:
            dict: Dictionnaire représentant l'objet avec ses attributs.
        """
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "reply_content": self.reply_content,
            "reply_date": self.reply_date.isoformat() if self.reply_date else None,
            "comment_id": self.comment_id
        }
        return data
    
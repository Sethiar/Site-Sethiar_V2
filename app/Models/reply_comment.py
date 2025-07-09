"""
Représente la classe des réponses aux commentaires des sujets du forum.
"""

#----------------------------------------------------------------
# Création d'une classe gérant les réponses aux commentaires.
#----------------------------------------------------------------

from . import db
from .base_model import BaseModel


from datetime import datetime


# Table des réponses aux commentaires des clients.
class CommentReply(BaseModel):
    """
    Représente une réponse à un commentaire sur le site.

    Attributes:
        id (int) : Identifiant unique de la réponse.
        reply_content (str) : Contenu de la réponse.
        reply_date (datetime) : Date et heure de la réponse (par défaut, date actuelle UTC).
        comment_id (int) : Identifiant du commentaire associé à la réponse.
        user_id (int) : Identifiant de l'utilisateur ayant posté la réponse.
        anonymous_id (str) : Identifiant de l'utilisateur anonyme.
    """

    __tablename__ = "comment_reply"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    reply_content = db.Column(db.Text(), nullable=False)
    reply_date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    # Relation avec la classe CustomerComment.
    comment_id = db.Column(db.Integer, db.ForeignKey('customer_comment.id'), nullable=False)
    comment = db.relationship('CustomerComment', back_populates='replies')

    # Relation avec la classe User.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', back_populates='comment_replies')
    
    # Relation avec la classe Anonyme.
    anonymous_id = db.Column(db.String(36), nullable=True)

    
    # Fonction qui permet de représenter l'objet en chaîne de caractères.
    def __repr__(self):
        """
        Affichage lisible de l'objet pour le debug ou les logs.
        """
        return f"<CommentReply(id={self.id}, comment_id={self.comment_id}, user_id={self.user_id}, date={self.reply_date})>"


    # Fonction qui renvoie les données au sein d'un dictionnaire.
    def to_dict(self, include_user=False):
        """
        Convertit l'objet en dictionnaire (utile pour API/JSON).

        Args:
            include_user (bool): Inclure ou non les infos sur l'auteur.

        Returns:
            dict: Représentation clé/valeur de l'objet.
        """
        data = {
            "id": self.id,
            "reply_content": self.reply_content,
            "reply_date": self.reply_date.isoformat(),
            "comment_id": self.comment_id,
            "user_id": self.user_id
        }

        if include_user and self.user:
            data["user"] = {
                "id": self.user.id,
                "username": getattr(self.user, "username", "Inconnu")
            }

        return data
    
    
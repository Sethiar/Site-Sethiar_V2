"""
Représente la classe des commentaires postés par les clients de l'entrprise ou des anonymes.
"""

#----------------------------------------------------------------
# Création d'une classe gérant les commentaires des clients.
#----------------------------------------------------------------

from . import db
from datetime import datetime
from .base_model import BaseModel


# Modèle de la classe CommentCustomer.
class CustomerComment(BaseModel):
    """
    Représente un commentaire laissé sur l'espace de commentaire du site.
    
    Attributes:
        id (int): identification unique du commentaire.
        name_enterprise (str): Nom de l'entreprise du client.
        comment_content (str): Contenu du commentaire.
        comment_date (datetime): Date et heure du commentaire.
        subject_id (int): Identifiant du sujet associé au commentaire
        subject (Comments): Relation avec la tabe de commentaires.
        user_id (int): identifiant de l'utilisateur client auteur du commentaire.
        user (User): Relation avec l'utilisateur.
        replies (list): Réponses associées à ce commentaire.
    """
    
    __tablename__ = "customer_comment"
    __table_args__ = {"extend_existing": True}
    
    id = db.Column(db.Integer, primary_key=True)
    name_enterprise = (db.Column(db.String(30), nullable=True))
    comment_content = db.Column(db.Text(), nullable=False)
    comment_date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    
    # Relation avec la classe SubjectComment.
    subject_id = db.Column(db.Integer, db.ForeignKey('subject_comment.id'), nullable=False)
    subject = db.relationship('SubjectComment', back_populates='comments')
    
    # Relation avec la classe User.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', back_populates='customer_comments')
    
    # Relation avec le classe Replysubject avec suppression en cascade.
    replies = db.relationship('CommentReply', back_populates='comment', cascade='all, delete-orphan')
    
    
    # Fonction qui représente l'objet en chaîne de caractères.
    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet CustomerComment.
        
        Returns:
            str: Chaîne représentant l'objet CustomerComment.
        """
        auteur = self.user.lastname if self.user else "AnonymousUser"
        return f"<CustomerComment(id={self.id}, auteur='{auteur}', content='{self.comment_content[:20]}...', \
        date={self.comment_date})>"         
                 
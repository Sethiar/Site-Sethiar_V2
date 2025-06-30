"""
Classe permettant de créer l'objet "sujet" de l'espace de commentaires.
"""

from . import db

# Modèle de la classe représentant les sujets de l'espace de comemtaires.
class SubjectComment(db.Model):
    """
    Modèle de données représentant les sujets de l'espace de commentaires.
    
    Attributes:
        id (int): Identifiant unique du sujet pour l'espace de commentaires.
        nom (str): Nom du sujet de l'espace de commentaires.
    """
    
    __tablename__ = "subject_comment"
    __table_args__ = {"extend_existing": True}
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    
    # Relation avec la table customer_comment.
    comments = db.relationship('CustomerComment', back_populates='subject', cascade='all, delete-orphan')
    
    
    # Représentation en chaîne de caractères de  l'objet SubjectComment.
    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet SubjectComment.
        
        Returns:
            str: Chaîne représentant l'objet SubjectComment.
        """
        return f"<SubjectComment(nom='{self.nom}')"
    
    
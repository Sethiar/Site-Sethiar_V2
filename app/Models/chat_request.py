"""
Classe représentant les requêtes de chat vidéo.
"""

#====================================#
#  Modèle de la classe  ChatRequest  #
#====================================#

from .base_model import BaseModel
from enum import Enum

# Fonction qui va permettre de gérer les statuts des requêtes de chat vidéo.
class ChatRequestStatus(Enum):
    """
    Enumération des statuts possibles pour une requête de chat.
    
    Attributs:
        EN_ATTENTE (str): Requête en attente de traitement.
        ACCEPTEE (str): Requête acceptée par l'administrateur.
        REFUSEE (str): Requête refusée par l'administrateur.
    """
    EN_ATTENTE = "En attente"
    ACCEPTEE = "Acceptée"
    REFUSEE = "Refusée"


from sqlalchemy import Enum as PgEnum


# Modèle de la classe ChatRequest.
"""
Code créant l'objet "ChatRequest" qui représente une requête de chat dans la base de données.
""" 

from . import db
import logging


from datetime import datetime

# Utilisation de JSON pour postgreSQL
from sqlalchemy.dialects.postgresql import JSON


class ChatRequest(BaseModel):
    """
    Classe ChatRequest qui représente une requête de chat dans la base de données.
    
    Attributs:
        id (int): Identifiant unique de la requête de chat.
        enterprise_name (str): Nom de l'entreprise qui a fait la requête.
        admin_id (int): Identifiant de l'administrateur qui a répondu à la requête.
        email (str): Email du demandeur de devis
        request_content (str): Contenu de la requête de chat.
        date_rdv (datetime): Date initiale proposée pour le rendez-vous.
        heure (time): Heure initiale proposée pour le rendez-vous.
        status (str): Statut de la requête (par exemple, 'en attente', 'acceptée', 'refusée').
        admin_choice (list): Choix de l'administrateur concernant la requête.
        user_choice (datetime): Stockage de la date et de l'heure choisies par l'utilisateur.
        created_at (datetime): Date et heure de création de la requête.
        meta_data (dict): Métadonnées associées à la requête, stockées en JSON.
    """
    
    __tablename__ = 'chat_request'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    enterprise_name = db.Column(db.String(30), nullable=True, default="Particulier")
    email = db.Column(db.String(50), nullable=False)
    request_content = db.Column(db.Text, nullable=False)
    date_rdv = db.Column(db.DateTime(timezone=True), nullable=True)
    heure = db.Column(db.Time(), nullable=True)
    
    status = db.Column(PgEnum(ChatRequestStatus), nullable=False, default=ChatRequestStatus.EN_ATTENTE)
    admin_choice = db.Column(JSON, nullable=True)
    user_choice = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    # Relation avec la table Admin.
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    admin = db.relationship('Admin', back_populates='chat_request')
    
    
    #===================================================#
    #    Représentation sre en chaine de catactères     #
    #===================================================#
    
    def __repr__(self):
        """
        Représentation de l'objet ChatRequest.
        
        Returns:
            str: Représentation de la requête de chat.
        """
        return f"<ChatRequest (id='{self.id}', enterprise_name='{self.enterprise_name}', email='{self.email}', \
                status='{self.status}', created_at='{self.created_at}', request_content='{self.request_content[:20]}...', \
                date_rdv='{self.date_rdv}', heure='{self.heure}', admin_choice='{self.admin_choice}', \
                user_choice='{self.user_choice}')>"
               
                
    #==========================================================================#
    # Fonctions relatives à la validation / Rejet d'une demande de chat vidéo  #  
    #==========================================================================#

    # Fonction qui convertit l'objet ChatRequest en dictionnaire.
    # Cela est utile pour la sérialisation JSON ou pour d'autres opérations.
    def to_dict(self, include_admin=False):
        data = {
            'id': self.id,
            'nom de l\'entreprise': self.enterprise_name,
            'email': self.email,
            'request_content': self.request_content,
            'date_rdv': self.date_rdv.isoformat() if self.date_rdv else None,
            'heure': str(self.heure) if self.heure else None,
            
            'status': self.status.value if isinstance(self.status, ChatRequestStatus) else self.status,
            'user_choice': self.user_choice.isoformat() if self.user_choice else None,
            'created_at': self.created_at.isoformat()
        }
        if include_admin:
            data['admin_choice'] = self.admin_choice
            data['admin_id'] = self.admin_id
        return data

    
    # Fonction qui permet d'accepter un chat vidéo et ainsi de modifier le statut de la demande.
    def accept_chat_request(self):
        """
        Accepte la requête de chat en modifiant son statut à 'acceptée'.
        """
        self.status = ChatRequestStatus.ACCEPTEE
        
        # Sauvegarde des changements dans la base de données. 
        self.save_data()
        logging.info(f"ChatRequest {self.id} a été acceptée.")
    
    
    # Fonction qui permet de refuser un chat vidéo et ainsi de modifier le statut de la demande.
    def refuse_chat_request(self):
        """
        Refuse la requête de chat en modifiant son statut à 'refusée'.
        """
        self.status = ChatRequestStatus.REFUSEE
        
        # Sauvegarde dans la base de données.
        self.save_data()
        logging.info(f"ChatRequest {self.id} a été refusée.")
    
    
    # Fonction qui permet de valider un chat vidéo et ainsi de modifier le statut de la demande.
    def validate_chat_request(self, new_status=ChatRequestStatus.EN_ATTENTE):
        """
        Valide la requête de chat en modifiant son statut.
        Args:
            new_status (str): Nouveau statut de la requête. Par défaut, 'en attente'.
        """
        
        if not isinstance(new_status, ChatRequestStatus):
            raise ValueError(f"Le statut doit être une instance de ChatRequestStatus, pas {type(new_status)}.")
        
        self.status = new_status
        self.save_data()
    
        # Commit des changements dans la base de données.
        logging.info(f"ChatRequest {self.id} traité avec le statut {self.status}.")
        
        
    
                
                        
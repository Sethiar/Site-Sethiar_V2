"""
Représente la classe des demandes de devis.
"""

#----------------------------------------------------------------
# Création d'une classe gérant les administrateurs.
#----------------------------------------------------------------


import logging

from . import db
from .base_model import BaseModel
from enum import Enum

# Utilisation de JSON pour postgreSQL
from sqlalchemy.dialects.postgresql import JSON


# Classe permettant de gérer le statut de la demande de devis.
class DevisRequestStatus(Enum):
    """
    Enumération des statuts possibles pour une requête de chat.
    
    Attributs:
        EN_ATTENTE (str): Requête en attente de traitement.
        ACCEPTEE (str): Requête acceptée par l'administrateur.
        REFUSEE (str): Requête refusée par l'administrateur.
    """
    EN_ATTENTE = 'en attente'
    ACCEPTEE = 'acceptée'
    REFUSEE = 'refusée'


from sqlalchemy import Enum as PgEnum


from datetime import datetime

# Modèle de la classe DevisRequest.
class DevisRequest(BaseModel):
    """
    Modèle de données représentant une demande de devis.
    
    Attributes:
        id (int): Identifiant unique de la demande de devis.
        lastname (str): Nom du client.
        firstname (str): Prénom du client.
        phone (str): Téléphone du client.
        enterprise_name (str): Nom de l'entreprise. default=particulier
        email (str): Email du client.
        project_type (str): Type de projet demandé.
        devis_content (str): Contenu de la demande de devis.
        date_devis (datetime): Date de la demande de devis.
        status (StatutEnum): Statut de la demande (en attente, validée, refusée).       
        meta_data (dict): Métadonnées associées à la requête, stockées en JSON.
    """
    
    __tablename__ = "devis_request"
    __table_args__ = {"extend_existing": True}
    
    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(30), nullable=False)
    firstname = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    enterprise_name = db.Column(db.String(30), nullable=False, default="Particulier")
    email = db.Column(db.String(50), nullable=False)
    project_type = db.Column(JSON, nullable=False)
    devis_content = db.Column(db.Text, nullable=False)
    date_devis = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    status = db.Column(PgEnum(DevisRequestStatus), nullable=False, default=DevisRequestStatus.EN_ATTENTE)
    meta_data = db.Column(JSON, nullable=True)
    
    
    #==================================================================#
    # Fonction représentant les données dans une chaîne de caractères  #
    #==================================================================#
    
    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'objet DevisRequest
        
        Returns:
           str: Cahîne de caractère représentant l'objet DevisRequest.
        """
        return (f"<DevisRequest(id='{self.id}', nom='{self.lastname}', prénom='{self.firstname}', \
            téléphone='{self.phone}', name_enterprise='{self.name_enterprise}', email='{self.email}', \
            project_type='{self.project_type}', devis_content='{self.devis_content}'>")
        
    #-------------------------------------------------------------------------------------------
    
    # Fonction qui convertit l'objet DevisRequest en dictionnaire.
    # Cela est utile pour la sérialisation JSON ou pour d'autres opérations.
    def to_dict(self, include_admin=False):
        data = {
            'id': self.id,
            'name_enterprise': self.name_enterprise,
            'phone': self.phone,
            'email': self.email,
            'project_type': self.project_type,
            'devis_content': self.devis_content,
            'date_devis': self.date_devis.isoformat() if self.date_devis else None,
            'status': self.status.value if isinstance(self.status, DevisRequestStatus) else self.status,
            'meta_data': self.meta_data
        }
        if include_admin:
            data['admin_id'] = self.admin_id
        
        return data


    # Fonction qui permet de valider une demande de devis et ainsi de modifier le statut de la demande.
    def validate_devis_request(self, new_status=DevisRequestStatus.EN_ATTENTE):
        """
        Valide la demade de devis en modifiant son statut.
        Args:
            new_status (str): Nouveau statut de la requête. Par défaut, 'en attente'.
        """
        
        if not isinstance(new_status, DevisRequestStatus):
            raise ValueError(f"Le statut doit être une instance de DevisRequestStatus, pas {type(new_status)}.")
        
        # Nouveau stautus doit être une instance de DevisRequestStatus.
        self.status = new_status
        self.save_data()
    
        # Commit des changements dans la base de données.
        logging.info(f"DevisRequest {self.id} status updated to {self.status}.")
        logging.debug(f"DevisRequest {self.id} updated in the database.")
        logging.debug(f"DevisRequest {self.id} committed to the database.")
        
        return self
        
    # Fonction qui permet de valider une demande de devis.
    def accept_devis_request(self):
        """
        Accepte la demande de devis en modifiant son statut à 'acceptée'.
        """
        return self.validate_devis_request(new_status=DevisRequestStatus.ACCEPTEE)
    
    # Fonction qui permet de refuser une demande de devis.
    def refuse_devis_request(self):
        """
        Refuse la deamnde de devis en modifiant son statut à 'refusée'.
        """
        return self.validate_devis_request(new_status=DevisRequestStatus.REFUSEE) 
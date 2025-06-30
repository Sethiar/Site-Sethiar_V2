"""
Ce code permet de gérer les entrées dans les tables de données.
"""

import logging
from . import db

class BaseModel(db.Model):
    __abstract__ = True  # Cette classe ne crée pas de table directement
    
    def save_data(self):
        """
        Enregistre les données dans la base de données.
        """
        try:
            db.session.add(self)
            db.session.commit()
            logging.debug(f"{self.__class__.__name__} enregistré avec succès.")
        except Exception as e:
            db.session.rollback()
            logging.error(f"Erreur lors de l'enregistrement dans {self.__class__.__name__}: {e}")
            raise e
        return self

    def delete_data(self):
        """
        Supprime les données de la base de données.
        """
        try:
            db.session.delete(self)
            db.session.commit()
            logging.debug(f"{self.__class__.__name__} supprimé avec succès.")
        except Exception as e:
            db.session.rollback()
            logging.error(f"Erreur lors de la suppression dans {self.__class__.__name__}: {e}")
            raise e
        return self

    def update_data(self):
        """
        Met à jour les données existantes dans la base de données.
        """
        try:
            db.session.commit()
            logging.debug(f"{self.__class__.__name__} mis à jour avec succès.")
        except Exception as e:
            db.session.rollback()
            logging.error(f"Erreur lors de la mise à jour dans {self.__class__.__name__}: {e}")
            raise e
        return self
    
    def as_dict(self, exclude=None):
        """
        Convertit l'instance en dictionnaire.

        Args:
            exclude (list, optional): Liste des attributs à exclure. Par défaut : None.

        Returns:
            dict: Représentation de l'objet sous forme de dictionnaire.
        """
        if exclude is None:
            exclude = []

        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name not in exclude
        }

    @classmethod
    def find_by_id(cls, id_):
        """
        Recherche une instance par son ID.

        Args:
            id_ (int): Identifiant de l'objet.

        Returns:
            instance: Objet trouvé ou None.
        """
        return cls.query.get(id_)

    @classmethod
    def all(cls):
        """
        Retourne toutes les instances de la table.

        Returns:
            list: Liste des objets.
        """
        return cls.query.all()

    @classmethod
    def filter_by(cls, **kwargs):
        """
        Recherche les objets correspondant aux filtres donnés.

        Args:
            **kwargs: Filtres à appliquer (ex: username="arnaud").

        Returns:
            list: Objets correspondants.
        """
        return cls.query.filter_by(**kwargs).all()
    
    
"""
admin = Admin(username="arnaud", role="SuperAdmin")
admin.save_data()

# Mettre à jour
admin.role = "Admin"
admin.update_data()

# Supprimer
admin.delete_data()

# Trouver un objet
Admin.find_by_id(1)
Admin.filter_by(username="arnaud")

# Sérialiser en JSON
admin.as_dict(exclude=["password_hash", "salt"])

"""
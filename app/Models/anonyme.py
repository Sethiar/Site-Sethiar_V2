"""
Classe représentant un utilisateur anonyme du site.
"""
from uuid import uuid4
from flask_login import AnonymousUserMixin


# Modèle de la classe anonyme.
class AnonymousUser(AnonymousUserMixin):
    """
    Classe Anonyme qui représente un utilisateur anonyme dans l'application.
    
    Hérite de AnonymousUserMixin pour intégrer les fonctionnalités de Flask-Login.
    """
    def __init__(self, anonymous_id=None):
        """
        Initialise l'utilisateur anonyme.
        
        Args:
            anonymous_id (str, optional): Identifiant de l'utilisateur anonyme. 
                                           Par défaut, il est None.
        """
        self.anonymous_id = anonymous_id or str(uuid4())

    
    # Fonction qui renvoit une chaine de caractères.
    def __repr__(self):
        """
        Représentation de l'objet Anonyme.
        
        Returns:
            str: Représentation de l'utilisateur anonyme.
        """
        return f"<AnonymousUser (ID: {self.id})>"
    
    # fonction attribuant une photo par defaut à l'utilisateur anonyme.
    def profil_photo_anonymous(self):
        """
        Attribution de la photo de profil par défaut à l'utilisateur anonyme.
        """
        return 'static/images/images_profil/default_profile_photo.png'
    #----------------------------------------------------------------
    
    
    #=========================================#
    # Fonctions relatives à la classe Anonyme #
    #=========================================#
    
    # Fonction qui permet de vérifier que l'anonyme n'a pas de rôle.
    def has_role(self, role):
        """
        Vérifie si l'utilisateur anonyme a un rôle spécifique.
        
        Args:
            role (str): Le rôle à vérifier.
        
        Returns:
            bool: Toujours False, car les utilisateurs anonymes n'ont pas de rôles.
        """
        # Les utilisateurs anonymes n'ont pas de rôles.
        return False
    
    
    # Fonction / Propriété qui renvoie l'identifiant de l'utilisateur anonyme.
    @property
    def id(self):
        """
        Retourne l'identifiant de l'utilisateur anonyme.
        
        Returns:
            str: Identifiant de l'utilisateur anonyme, qui est toujours 'Anonyme'.
        """
        # L'identifiant de l'utilisateur anonyme est une chaîne fixe.
        return 'Anonyme'
    
    # Fin des fonctions utilisées par Flask-Login pour gérer les utilisateurs anonymes.
    
    
"""
Classe représentant un utilisateur anonyme du site.
"""

from flask_login import AnonymousUserMixin


# Modèle de la classe anonyme.
class AnonymousUser(AnonymousUserMixin):
    """
    Classe Anonyme qui représente un utilisateur anonyme dans l'application.
    
    Hérite de AnonymousUserMixin pour intégrer les fonctionnalités de Flask-Login.
    """
    
    # Fonction qui renvoit une chaine de caractères.
    def __repr__(self):
        """
        Représentation de l'objet Anonyme.
        
        Returns:
            str: Représentation de l'utilisateur anonyme.
        """
        return f"<AnonymousUser (utilisateur anonyme)>"
    #----------------------------------------------------------------
    
    #--------------------------------------------------------------
    # Fonctions relatives à la classe Anonyme.
    #--------------------------------------------------------------
    
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
    
    
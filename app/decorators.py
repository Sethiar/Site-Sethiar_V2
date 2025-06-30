"""
Code configurant les décorateus de l'applicaiton.
"""

from functools import wraps
from flask import session, redirect, url_for, flash


# Focntion restreignant l'accès aux seuls adminsitrateurs.
def admin_required(f):
    """
    Ce décorateur vérifie si l'utilisateur est authentifié et possède le rôle de SuperAdmin.
    
    Si l'utilisateur n'a pas ce rôle, il est redirigé vers la page de donnexion spécifique
    aux administrateurs avec un message d'avertissement.
    
    Args: 
        f (function): La fonction à décorer.
        
    Returns:
        function: La fonction décorée qui inclut la vérification des privilèges administrateur.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """
        Fonction interne exécutée à la place de la fonction décorée.
        
        Cette fonction vérifie le rôle de administrateur à partir des données de connexion 
        et redirige si l'utilisateur n'est pas un administrateur.
        
        Args: 
            *args: Aguments positionnels pour la fonction décorée.
            **kwargs: Arguments nommés pour la fonction décorée.
            
        Returns:
            Response: Soit la réponse de la fonction décorée, soit la redirection.    
        """
        
        # Vérification de la qualité de l'administrateur de l'utilisateur.
        if 'role' not in session or session['role'] != "SuperAdmin":
            flash("Vosu n'avez les droits nécessaires pour vous connecter ici.","danger")
            return redirect(url_for('auth.login_admin'))
        
        # Si l'utilisateur est un administrateur, exécute la fonction décorée.
        return (f(*args, **kwargs))
    
    return decorated_function
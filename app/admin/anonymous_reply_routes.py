"""
Routes pour la gestion des réponses anonymes aux commentaires d'authentifiés ou non dans la section administrateur
"""

import logging
from flask import redirect, render_template, flash, url_for

from app.admin import admin_bp

from app.Models.reply_anonymous_comment import ReplyAnonymousComment, ReplyAnonymousCommentStatus

from app.Models.reply_anonymous_user_comment import ReplyAnonymousUserComment, ReplyAnonymousUserCommentStatus

from app.decorators import admin_required

# Routes permettant d'afficher les réponses anonymes non-validées.
@admin_bp.route('/liste-reponses-anonymes', methods=['GET'])
@admin_required
def anonymous_replies_list():
    """
    Affiche toutes les réponses anonymes à valider (anonymes + authentifiés).
    
    Cette route permet à l'administrateur de visuliser toutes les réposnes des utilisateurs non connectés.
    
    Elle affiche aussi les formulaires afin de valider ou rejeter ces réponses.
    
    Returns:
        Response: La page HTML du bakend affichant les tableaux des réponses non validées.
    """

    # Cas n°1 -- Réponses à commentaires d’anonymes
    
    # Récupération de toutes les réponses anonymes aux commentaires anonymes avec statut en attente.
    anonymous_replies = ReplyAnonymousComment.query.filter_by(status=ReplyAnonymousCommentStatus.EN_ATTENTE).all()
    
    # Création d'un dictionnaire regroupant les réponses.
    grouped_anonymous_replies = {
        "en_attente": anonymous_replies
        }
     
    # Cas n°2 -- Réponses à commentaires d’authentifiés
    
    # Récupération de toutes les réponses anonymes aux commentaires d'indentifiés avec le statut en attente.
    anonymous_user_replies = ReplyAnonymousUserComment.query.all()
    
    # Création d'un dictionnaire regroupant les réponses.
    grouped_anonymous_user_replies = {
        "en_attente": anonymous_user_replies
        }

    return render_template(
        'admin/anonymous_replies_list.html',
        grouped_anonymous_replies=grouped_anonymous_replies,
        grouped_anonymous_user_replies=grouped_anonymous_user_replies
    )


# Méthode pour valider les réponses à un commentaire anonyme.
@admin_bp.route('/anonyme/validation-reponse-anonyme/<int:id>', methods=['GET', 'POST'])
def validate_anonymous_reply(id):
    """
    Fonction pour gérer les réponses anonymes aux commentaires anonymes.
    
    Cette route permet à un administrateur de valider les réponses anonymes aux commentaires anonymes.
    Après avoir mis à jour le statut de la réponse, celle-ci est enregistrée dans la base de données.
    
    Returns:
        Response : Retour sur la page affichant les tableaux des réponses anonymes non validées.
    """
    
    # Récupération du commentaire anonyme à partir de son ID.
    anonymous_reply = ReplyAnonymousComment.query.get_or_404(id)

    try:
        # Appel de la méthode pour valider le commentaire anonyme.
        anonymous_reply.validate()
        logging.info(f"Réponse anonyme {anonymous_reply.id} validée et enregistrée dans ReplyAnonymousComment.")
        
        flash("Réponse anonyme validée avec succès.", "success")
        return redirect(url_for('admin.anonymous_replies_list'))
    
    except Exception as e:
        logging.error(f"Erreur lors de la validation de la réponse anonyme: {e}")
        flash("Erreur lors de la validation de la réponse anonyme.", "danger")
        return redirect(url_for('admin.anonymous_replies_list'))      
    

# Méthode pour rejeter les réponses à un commentaire anonyme.
@admin_bp.route('/anonyme/rejet-reponse-anonyme/<int:id>', methods=['GET', 'POST'])
def reject_anonymous_reply(id):
    """
    Fonction pour gérer les réponses anonymes aux commentaires anonymes.
    
    Cette route permet à un administrateur de rejeter les réponses anonymes.
    Après avoir mis à jour le statut de la réponse, il est enregistré dans la base de données.
    
    Returns:
        Response retour sur la page affichant les tableaux des réponses anonymes non validées.
    """
    
    # Récupération de la réponse anonyme à partir de son ID.
    anonymous_reply = ReplyAnonymousComment.query.get_or_404(id)
    
    try:
        # Appel de la méthode pour rejeter la réponse anonyme.
        anonymous_reply.reject()
        logging.info(f"Réponse anonyme {anonymous_reply.id} rejetée avec succès.")
        
        flash("Réponse anonyme rejetée avec succès.", "success")
        return redirect(url_for('admin.anonymous_replies_list'))
    
    except Exception as e:
        logging.error(f"Erreur lors du rejet de la réponse anonyme: {e}")
        flash("Erreur lors du rejet de la reponse anonyme.", "danger")
        return redirect(url_for('admin.anonymous_reply_list'))
    
    
    
# Méthode pour valider une réponse anonymes d'un commentaire d'authentifié.
@admin_bp.route('/anonyme/validation-reponse-anonyme-utilisateur/<int:id>', methods=['GET', 'POST'])
def validate_anonymous_user_reply(id):
    """
    Fonction pour valider la réponse anonyme à un utilisateur authentifié.
    
    Cette route permet à un administrateur de valider les réponses anonymes.
    Après avoir mis à jour le statut du commentaire, il est enregistré dans la base de données.
    
    Returns:
        Response retour sur la page affichant les tableaux des réponses non validées.
    """
    
    # Récupération de la réponse anonyme à partir de son ID.
    anonymous_user_reply = ReplyAnonymousUserComment.query.get_or_404(id)

    try:
        # Appel de la méthode pour valider la réponse anonyme.
        anonymous_user_reply.validate()
        logging.info(f"Réponse anonyme {anonymous_user_reply.id} validée et enregistrée dans ReplyAnonymousUserComment.")
        
        flash("Réponse anonyme validée avec succès.", "success")
        return redirect(url_for('admin.anonymous_replies_list'))
    
    except Exception as e:
        logging.error(f"Erreur lors de la validation de la réponse anonyme: {e}")
        flash("Erreur lors de la validation de la réponse anonyme.", "danger")
        return redirect(url_for('admin.anonymous_replies_list'))      
    

# Méthode pour rejeter une réponse anonymes d'un commentaire d'authentifié.
@admin_bp.route('/anonyme/rejet-reponse-anonyme-utilisateur/<int:id>', methods=['GET', 'POST'])
def reject_anonymous_user_reply(id):
    """
    Fonction pour rejeter la réponse anonyme à un utilisateur authentifié.
    
    Cette route permet à un administrateur de rejeter les réponses anonymes.
    Après avoir mis à jour le statut du commentaire, il est enregistré dans la base de données.
    
    Returns:
        Response retour sur la page affichant les tableaux les réponses anonymes non validées.
    """
    
    # Récupération de la réponse anonyme à partir de son ID.
    anonymous_user_reply = ReplyAnonymousUserComment.query.get_or_404(id)
    
    try:
        # Appel de la méthode pour rejeter le commentaire anonyme.
        anonymous_user_reply.reject()
        logging.info(f"Réponse anonyme {anonymous_user_reply.id} rejetée avec succès.")
        
        flash("Réponse anonyme validée avec succès.", "success")
        return redirect(url_for('admin.anonymous_replies_list'))
    
    except Exception as e:
        logging.error(f"Erreur lors de la validation de la réponse anonyme: {e}")
        flash("Erreur lors de la validation de la réponse anonyme.", "danger")
        return redirect(url_for('admin.anonymous_replies_list'))  
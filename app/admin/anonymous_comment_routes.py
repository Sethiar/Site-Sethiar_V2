"""
Routes pour la gestion des commentaires anonymes dans l'interface d'administration.
"""

import logging

from flask import redirect, url_for, flash, render_template

from app.admin import admin_bp

from app.Models.comment import Comment, CommentStatus

from app.decorators import admin_required


# Routes permettant d'afficher les commentaires anonymes non validés.
@admin_bp.route('/liste-commentaires-anonymes', methods=['GET'])
@admin_required
def anonymous_comments_list():
    """
    Affiche la liste des commentaires anonymes validés et non validés.

    Cette route permet à l'administrateur de visualiser tous les commentaires anonymes,
    qu'ils soient validés ou en attente de validation. Elle affiche également les formulaires
    nécessaires pour valider ou rejeter les commentaires.

    Returns:
        Response: La page HTML du backend affichant les tableaux des commentaires anonymes validés et non validés.
    """
    
    # Récupération de tous les commentaires anonymes en attente de validation.
    anonymous_comments = Comment.query.filter_by(status=CommentStatus.EN_ATTENTE).all()
    
    # Création du dictionnaire regroupant les commentaires par statut
    grouped_anonymous_comments = {
        "en attente": anonymous_comments
    }
    
    return render_template(
        'admin/anonymous_comments_list.html',
        anonymous_comments=anonymous_comments,
        grouped_anonymous_comments=grouped_anonymous_comments        
    )


# Méthode pour valider un commentaire anonyme.
@admin_bp.route('/anonyme/validation-commentaire-anonyme/<int:id>', methods=['GET', 'POST'])
def validate_anonymous_comment(id):
    """
    Fonction pour valider les routes de gestion des commentaires anonymes.
    
    Cette route permet à un administrateur de valider les commentaires anonymes.
    Après avoir mis à jour le statut du commentaire, il est enregistré dans la base de données.
    
    Returns:
        Response retour sur la page affichant les tableaux des commentaires anonymes validés et non validés.
    """
    
    # Récupération du commentaire anonyme à partir de son ID.
    anonymous_comment = Comment.query.get_or_404(id)

    try:
        # Appel de la méthode pour valider le commentaire anonyme.
        anonymous_comment.validate()
        logging.info(f"Commentaire anonyme {anonymous_comment.id} validé et enregistré dans ValidatedAnonymousComment.")
        
        flash("Commentaire anonyme validé avec succès.", "success")
        return redirect(url_for('admin.anonymous_comments_list'))
    
    except Exception as e:
        logging.error(f"Erreur lors de la validation du commentaire anonyme: {e}")
        flash("Erreur lors de la validation du commentaire anonyme.", "danger")
        return redirect(url_for('admin.anonymous_comments_list'))      
    

# Méthode pour rejeter un commentaire anonyme.
@admin_bp.route('/anonyme/rejet-commentaire-anonyme/<int:id>', methods=['GET', 'POST'])
def reject_anonymous_comment(id):
    """
    Fonction pour rejeter les commentaires anonymes.
    
    Cette route permet à un administrateur de rejeter les commentaires anonymes.
    Après avoir mis à jour le statut du commentaire, il est enregistré dans la base de données.
    
    Returns:
        Response retour sur la page affichant les tableaux des commentaires anonymes validés et non validés.
    """
    
    # Récupération du commentaire anonyme à partir de son ID.
    anonymous_comment = Comment.query.get_or_404(id)
    
    try:
        # Appel de la méthode pour rejeter le commentaire anonyme.
        anonymous_comment.reject()
        logging.info(f"Commentaire anonyme {anonymous_comment.id} rejeté avec succès.")
        
        flash("Commentaire anonyme rejeté avec succès.", "success")
        return redirect(url_for('admin.anonymous_comments_list'))
    
    except Exception as e:
        logging.error(f"Erreur lors du rejet du commentaire anonyme: {e}")
        flash("Erreur lors du rejet du commentaire anonyme.", "danger")
        return redirect(url_for('admin.anonymous_comments_list'))
    
    
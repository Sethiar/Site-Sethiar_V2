"""
Routes pour la gestion des sujets anonymes dans l'interface administrateur.
"""

#==========================#
#   Routes Sujets anonymes #
#==========================#


import logging
from flask import redirect, url_for, flash, render_template

from app.admin import admin_bp

from app.Models.subject import Subject, SubjectStatus

from app.decorators import admin_required


# Méthode permettant de valider les sujets créés par les anonymes.
@admin_bp.route('/liste-sujets-anonymes', methods=['GET', 'POST'])
@admin_required 
def subject_anonymous_list():
    """
    Affiche la liste des sujets anonymes validés et non validés.
    
    Cette route permet à l''administrateur de visualiser tous les sujest créés par les utilisateurs anonymes.
    Qu'ils soient validés ou en cours de validation. Elle affiche égaement les fonctions nécessaires 
    afin de valider ou rejeter et supprimer les sujets.
    
    Returns:
        Response: LA page HTML du backend affichant les tabelaux des sujets anonymes.    
    """
    # Récupération de tous les sujets anonymes en attente de validation.
    subject_anonymous = Subject.query.filter_by(status=SubjectStatus.EN_ATTENTE).all()
    
    # Crédu dictionnaire regroupant les commentaires par statut.
    grouped_subject_anonymous = {
        "en attente": subject_anonymous
    }
    
    return render_template('admin/subjects_anonymous_list.html',
                           subject_anonymous=subject_anonymous,
                           grouped_subject_anonymous=grouped_subject_anonymous
                           )
    
    
# Méthode pour valider un sujet anonyme.
@admin_bp.route('/anonyme/validation-sujet-anonyme/<int:id>', methods=['GET', 'POST'])
def validate_subject_anonymous(id):
    """
    Fonction pour valider les routes de gestion des sujets anonymes.
    
    Cette routes permet à l'administrateur de valider les sujets anonymes.
    Après avoir mis à jour le statut du commentaire, il est enregistré dans la base de données.
    
    Returns:
        Response reotur sur la page du backend affichant le tableau des sujets anonymes.
    """
    
    # Récupération du sujet anonyme à partir de son id.
    subject_anonymous = Subject.query.get_or_404(id)
    
    try:
        # Appel de la fonction pour valider le sujet.
        subject_anonymous.validate()
        logging.info(f"Sujet anonyme {subject_anonymous.id} validé et enregitré")
        
        flash("Suejt anonyme validé avec succès.", "success")
        return redirect(url_for('admin.subject_anonymous_list'))
    
    except Exception as e:
        logging.error(f"Erreur lors de la validation du sujet anonyme: {e}")
        flash("Erreur lors de la validation du sujet.", "danger")
        return redirect(url_for('admin.subject_anonymous_list'))
    

# Methode pour rejeter un sujet anonyme.
@admin_bp.route('/anonyme/rejet-sujet_anonyme/<int:id>', methods=['GET', 'POST'])
def reject_subject_anonymous(id):
    """
    Fonction pour rejeter un sujet anonyme.
    
    Cette route permet à un administrateur de rejeter les sujets anonymes.
    Après avoir mis à jour le statut du commentaire, il est supprimé de la base de données.
    
    Returns:
        Response retour sue la page affichant le tableau des sujets anonymes.
    """
    # Récupération des sujets anonymes à partir de leur id.
    subject_anonymous = Subject.query.get_or_404(id)
    
    try:
        # Appel de la méthode pour rejeter le sujet anonoyme.
        subject_anonymous.reject_subject_anonymous()
        logging.info(f"Sujet anonyme {subject_anonymous.id} rejeté et supprimé avec succès.", "success")
        
        flash("Sujet anonyme rejeté et supprimé avec succès.")
        return redirect(url_for('admin.subject_anonymous_list'))
    
    except Exception as e:
        logging.error("Erreur lors du rejet et de la suppression du sujet:{e}")
        flash("Erreur lors du rejet et de la suppression du sujet.", "danger")
        return redirect(url_for('admin.subject_anonymous_list'))
    
    
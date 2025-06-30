"""
Code permettant de gérer les demandes de devis
"""

from app.devis import devis_bp

from flask import flash, redirect, url_for
from app import db

from app.mail.routes import mail_reply_devis_reject, mail_reply_devis_validate

from app.Models.devis_request import DevisRequest


# Méthode supprimant la demande de chat vidéo du tableau administrateur.
@devis_bp.route('/suppression-demande-devis/<int:id>', methods=['POST'])
def suppress_devis(id):
    """
    Supprime une demande de devis du tableau des demandes administratives.

    Cette route permet à l'administrateur de supprimer une demande de devis spécifique en fonction de son ID.
    Après la suppression, un message de confirmation est affiché et l'administrateur est redirigé vers la
    page de la liste des devis du site.

    Args:
        id (int): L'identifiant unique de la demande de devis à supprimer.

    Returns:
        Response: Redirection vers la page de la liste des devis après la suppression du devis.
    """
    try:
        # Récupération du devis à supprimer.
        devis = DevisRequest.query.get(id)

        # Vérification de l'existence du devis.
        if not devis:
            flash("La demande de devis n'a pas été trouvée.", "danger")
            return redirect(url_for('admin.list_devis'))

        # Suppression du devis.
        db.session.delete(devis)

        # Enregistrement au sein de la base de données.
        db.session.commit()

        # Message de confirmation après la suppression.
        flash(f"La requête de l'utilisateur : {devis.nom} {devis.prenom} a été supprimée.", "success")

    except Exception as e:
        # Gestion des erreurs et annulation des changements si nécessaire.
        db.session.rollback()  # Annulation des modifications en cas d'erreur.
        flash(f"Une erreur s'est produite lors de la suppression : {str(e)}", "danger")

    finally:
        # Fermeture de la session de base de données.
        db.session.close()

    return redirect(url_for('admin.list_devis'))


# Méthode générique pour traiter une demande de devis.
def process_devis(id, action):
    """
    Traite une demande de devis en fonction de l'action spécifiée (valider ou refuser)
    et en informe l'utilisateur par e-mail.

    Args:
        id (int): L'identifiant unique de la demande de devis.
        action (str): L'action à effectuer, soit "valider" ou "refuser".

    Returns:
        Response: Redirection vers la page de la liste des devis après traitement.
    """
    # Récupération de la demande de devis.
    devis = DevisRequest.query.get_or_404(id)

    try:
        # Mise à jour du statut selon l'action.
        if action == "valider":
            devis.accept_devis_request()
            mail_reply_devis_validate(devis)
            flash("La demande de devis a été traitée et validée.", "success")
        elif action == "refuser":
            devis.refuse_devis_request()
            mail_reply_devis_reject(devis)
            flash("La demande de devis a été traitée et refusée.", "success")
        else:
            flash("Action inconnue pour traiter la demande.", "danger")
            return redirect(url_for("admin.list_devis"))

        # Sauvegarde des modifications dans la base de données.
        db.session.commit()

    except Exception as e:
        # Gestion des erreurs lors du traitement.
        flash(f"Une erreur s'est produite : {str(e)}", "danger")
        # Annule les changements si une erreur survient.
        db.session.rollback()

    finally:
        # Fermeture de la session de base de données.
        db.session.close()

    return redirect(url_for("admin.list_devis"))


# Route pour valider une demande de devis.
@devis_bp.route('/validation-demande-devis/<int:id>', methods=['POST'])
def valide_devis(id):
    """

    :param id:
    :return:
    """
    return process_devis(id, "valider")


# Route pour refuser une demande de devis.
@devis_bp.route('/refus-demande-devis/<int:id>', methods=['POST'])
def refuse_devis(id):
    """

    :param id:
    :return:
    """
    return process_devis(id, "refuser")
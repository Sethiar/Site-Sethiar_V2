"""
Code permettant de gérer les routes concernant le chat vidéo du blog.
"""

from datetime import datetime

from app.chat import chat_bp

from flask import render_template, flash, redirect, url_for, request

from app import db

from app.forms.chat_request import ChatRequestForm, UserLink

from app.Models.chat_request import ChatRequest
from app.Models.admin import Admin

from app.mail.routes import send_mail_validate_request, send_mail_refusal_request, \
    send_confirmation_request_reception, send_request_admin

from app.extensions import create_whereby_meeting_admin


# Route permettant d'afficher la vidéo du chat vidéo.
@chat_bp.route('/video_chat/<int:request_id>')
def video_chat(request_id):
    """
    Route permettant d'ouvrir la page de chat vidéo pour une demande spécifique.

    Cette route affiche la page de chat vidéo uniquement si la demande est validée et que la date/heure du rendez-vous
    est proche de l'heure actuelle. Sinon, elle renvoie une erreur et redirige vers la page d'accueil.

    :param request_id: L'identifiant de la demande de chat vidéo.
    :return: La page HTML contenant l'interface de chat vidéo, si les conditions sont remplies.
    """

    # Récupération de la demande de chat vidéo par son identifiant.
    request = ChatRequest.query.get_or_404(request_id)

    # Vérification de la validation de la demande et si la date/heure du rendez-vous est proche de l'heure actuelle.
    now = datetime.now()
    rdv_datetime = datetime.combine(request.date_rdv, request.heure)

    # Vérification pour autoriser l'accès seulement un jour ou une heure avant le rendez-vous.
    if request.status != 'validée' or rdv_datetime > now:
        flash("Le chat vidéo n'est pas encore disponible ou la demande n'est pas validée.", "error")
        return redirect(url_for('landing_page'))

    return render_template('chat_session_user.html', request=request)


# Route permettant de remplir le formulaire afin de demander un chat vidéo.
@chat_bp.route('/demande-chat-video', methods=['GET', 'POST'])
def chat_request():
    """"
    Affiche le formulaire permettant à l'utilisateur de demander un chat vidéo.

    Cette route est accessible à tous les utilisateurs. Elle instancie le formulaire de demande de chat
    vidéo et le rend disponible à l'utilisateur pour qu'il puisse le remplir.

    :return: Le formulaire de demande de chat vidéo, affiché via le template 'chat/form_request_chat.html'.
    """
    # Instanciation du formulaire.
    formrequest = ChatRequestForm()

    return render_template('chat/form_request_chat.html', formrequest=formrequest)


# Route permettant d'afficher le formulaire de demande de chat
# vidéo et d'enregistrer les informations dans la base de données.
@chat_bp.route('/envoi-demande-chat', methods=['GET', 'POST'])
def send_request():
    """
    Gère la demande de chat vidéo en affichant le formulaire et en enregistrant
    les informations dans la base de données, avec envoi d'emails à l'utilisateur et à l'administrateur.
    """

    formrequest = ChatRequestForm()

    if formrequest.validate_on_submit():
       
        # Récupération des données du formulaire.
        enterprise_name = formrequest.enterprise_name.data
        email = formrequest.email.data
        request_content = formrequest.request_content.data
        date_rdv = formrequest.date_rdv.data
        heure = formrequest.heure.data
        datetime_rdv = datetime.combine(date_rdv, heure)

        # Vérification de la disponibilité de la plage horaire
        conflicting_request = ChatRequest.query.filter_by(date_rdv=date_rdv, heure=heure).first()

        if conflicting_request:
            flash(f"La plage horaire pour le {date_rdv} à {heure} est déjà réservée. Veuillez choisir une autre plage.",
                  "danger")
            return redirect(request.url)
        
        # Récupération de l'administrateur.
        admin = Admin.query.first()
        if not admin:
            flash("Aucun administrateur disponible pour traiter la demande.", "error")
            return redirect(url_for('landing_page'))

        # Création d'une nouvelle demande de chat.
        new_request = ChatRequest(
            enterprise_name=enterprise_name,
            email=email,
            request_content=request_content,
            date_rdv=date_rdv,
            heure=heure,
            admin_id=admin.id
        )
            
        # Tests.    
        try:
            db.session.add(new_request)
            db.session.commit()

            # Envoi du mail à l'utilisateur.
            send_confirmation_request_reception(new_request.email)

            # Envoi du mail à l'administrateur avec le fichier en pièce jointe (si fichier joint).
            send_request_admin(admin, request_content=request_content)

            flash("Demande effectuée avec succès.", "success")

        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de l'enregistrement de la demande: {str(e)}", "danger")
        
        finally:
            db.session.close()
             
        return redirect(url_for('landing_page'))
    
    # En cas d'erreur de validation.
    return render_template('chat/form_request_chat.html', formrequest=formrequest)


# Méthode supprimant la demande de chat vidéo du tableau administrateur.
@chat_bp.route('/suppression-demande-chat/<int:id>', methods=['POST'])
def suppress_request(id):
    """
    Supprime une demande de chat vidéo du tableau des demandes administratives.

    Cette route permet à l'administrateur de supprimer une demande de chat vidéo spécifique en fonction de son ID.
    Après la suppression, un message de confirmation est affiché et l'administrateur est redirigé vers la page du calendrier
    des demandes de chat.

    Args:
        id (int): L'identifiant unique de la demande de chat vidéo à supprimer.

    Returns:
        Response: Redirection vers la page du calendrier d'administration après la suppression de la demande.
    """
    # Récupération de la requête à supprimer.
    request = ChatRequest.query.get(id)

    # Vérification de l'existence de la requête.
    if request:
        # Suppression de la requête.
        db.session.delete(request)
        # Enregistrement au sein de la base de données.
        db.session.commit()
        flash(f"La requête de l'utilisateur : {request.pseudo} a été supprimée.")
        
        # Fermeture de la connexion.
        db.session.close()
        
    return redirect(url_for('admin.calendar'))


# Méthode traitant la demande en attente et la validant.
@chat_bp.route('/validation-demande-chat/<int:id>', methods=['POST'])
def valide_request(id):
    """
    Valide une demande de chat vidéo spécifique et en informe l'utilisateur par e-mail.

    Cette route permet à un administrateur de valider une demande de chat vidéo en attente, identifiée par son ID.
    Après avoir mis à jour le statut de la demande à "validée", un e-mail de confirmation est envoyé à l'utilisateur
    pour l'informer de la validation et lui fournir le lien de la session de chat.

    Args:
        id (int): L'identifiant unique de la demande de chat vidéo à valider.

    Returns:
        Response: Redirection vers la page du calendrier d'administration après la validation de la demande.
    """

    # Vérification de l'existence de la requête.
    if request:
        try:
            # Récupération de la requête à valider.
            request = ChatRequest.query.get_or_404(id)

            # Vérification de l'existence de l'utilisateur.
            if not request:
                flash("Utilisateur non trouvé.", "danger")
                return redirect(url_for("admin.calendar"))

            # Validation de la requête.
            request.accept_chat_request()
            # Envoi du mail de validation.
            send_mail_validate_request(request)

            flash("La demande de chat vidéo a été traitée et validée.", "success")
        except Exception as e:
            # Gestion erreur si erreur.
            flash(f"Une erreur s'est produite lors de la validation: {str(e)}", "danger")
            return redirect(url_for("admin.calendar"))

    return redirect(url_for("admin.calendar"))


# Méthode traitant la demande en attente et la refusant.
@chat_bp.route('/refus-demande-chat/<int:id>', methods=['POST'])
def refuse_request(id):
    """
    Refuse une demande de chat vidéo spécifique et en informe l'utilisateur par e-mail.

    Cette route permet à un administrateur de refuser une demande de chat vidéo en attente, identifiée par son ID.
    Après avoir mis à jour le statut de la demande à "refusée", un e-mail de notification est envoyé à l'utilisateur
    pour l'informer du refus.

    Args:
        id (int): L'identifiant unique de la demande de chat vidéo à refuser.

    Returns:
        Response: Redirection vers la page du calendrier d'administration après le traitement de la demande.
    """
    # Récupération de la requête à refuser.
    request = ChatRequest.query.get_or_404(id)

    # Vérification de l'existence de la requête.
    if request:
        try:
            # Récupération de l'utilisateur avec son pseudo.
            request = ChatRequest.query.get_or_404(id)

            # Vérification de l'existence de l'utilisateur.
            if not request:
                flash("Utilisateur non trouvé.", "danger")
                return redirect(url_for("admin.calendar"))

            # Refus de la requête.
            request.refuse_chat_request()
            # Envoi du mail de refus.
            send_mail_refusal_request(request)

            flash("La demande de chat vidéo a été traitée et refusée.", "success")
        except Exception as e:
            # Gestion erreur si erreur.
            flash(f"Une erreur s'est produite lors de la validation: {str(e)}", "danger")
            return redirect(url_for("admin.calendar"))

    return redirect(url_for("admin.calendar"))


# Route permettant d'envoyer le lien du chat vidéo à l'utilisateur par mail.
@chat_bp.route('/envoi-lien-utilisateur/<int:id>', methods=['POST'])
def send_user_link(id):
    """
    Envoie un e-mail contenant le lien du chat vidéo à un utilisateur spécifique.

    Cette route récupère le lien du chat vidéo depuis le formulaire soumis,
    ainsi que les détails de la requête et de l'utilisateur associés. Un e-mail contenant le lien du chat vidéo
    est ensuite envoyé à l'utilisateur.

    Args:
        id (int): L'identifiant de la requête de chat vidéo associée à l'utilisateur.

    Returns:
        Response: Redirection vers la page du calendrier d'administration après l'envoi de l'e-mail.
    """
    # Instanciation du formulaire.
    form = UserLink()

    if form.validate_on_submit():
        # Récupération du lien du chat vidéo à partir du formulaire.
        chat_link = form.chat_link.data

        # Récupération de la requête de chat vidéo associée à l'ID fourni.
        request_data = ChatRequest.query.get(id)

        if request_data:
            # Récupération de l'email de l'utilisateur demandeur du chat.
            email = ChatRequest.query.get(email=request_data.email).first()

            if email:
                # Appel de la fonction pour envoyer l'e-mail avec le lien du chat vidéo.
                send_mail_validate_request(email, request_data, chat_link)
                flash("Le lien a été envoyé à l'utilisateur avec succès.", "success")
            else:
                flash("Erreur : utilisateur introuvable.", "danger")
        else:
            flash("Erreur : requête de chat vidéo introuvable.", "danger")
    else:
        flash("Erreur dans le formulaire, veuillez vérifier les champs.", "danger")

    return redirect(url_for('admin.calendar'))


# Route permettant de générer le lien du chat pour l'administrateur.
@chat_bp.route('/admin_room_url')
def chat_video_session_admin():
    """
    Génère le lien de session pour l'administrateur et le rend disponible.

    Cette route appelle une fonction pour générer un lien unique pour la session de chat vidéo destinée à
    l'administrateur. Le lien est ensuite rendu disponible via un template HTML. Si la génération du lien échoue,
    une erreur est retournée.

    Returns:
        Response: Le rendu du modèle HTML 'chat/chat_session_admin.html' avec le lien de session si la génération
                  est réussie. Sinon, retourne un message d'erreur avec le code de statut 500.
    """
    # Appel de la fonction qui génère le lien administrateur.
    admin_room_url = create_whereby_meeting_admin()

    if admin_room_url:
        # Log pour vérifier le lien récupéré.
        print("admin Host Room URL:", admin_room_url)

        # Rendu du template avec le lien admin.
        return render_template('chat/chat_session_admin.html', room_url=admin_room_url)
    else:
        # Retourne une erreur si l'URL n'a pas pu être générée.
        return "Erreur lors de la génération de la réunion whereby côté administrateur.", 500
"""
Code permettant de définir les routes concernant les fonctions de l'administrateur du site comme, la consultation des
commentaires clients, leur suppression, la gestion des demandes de chat vidéo et l'accès au backend...
"""
import bcrypt

from PIL import Image
from io import BytesIO
from collections import defaultdict

from datetime import datetime

from flask import render_template, redirect, url_for, request, flash

from app.admin import admin_bp

from app.Models import db

from app.Models.admin import Admin
from app.Models.user import User
from app.Models.chat_request import ChatRequest, ChatRequestStatus

from app.Models.devis_request import DevisRequest

from app.Models.comment_customer import CustomerComment

from app.forms.form_comment import SuppressCommentForm
from app.forms.user_registration import UserRecording

from app.forms.chat_request import ChatRequestForm, UserLink
from app.forms.devis_request import DevisRequestForm


from app.decorators import admin_required

from app.extensions import create_whereby_meeting_admin, allowed_file


# Route permettant de se connecter au backend en tant qu'administrateur.
@admin_bp.route("/")
@admin_required
def backend():
    """
    Affiche la page principale du backend de l'administration.

    Cette route est accessible uniquement aux administrateurs et permet de visualiser la page d'accueil du backend.
    Elle récupère la liste des administrateurs enregistrés et passe ces informations au modèle HTML pour affichage.

    :return: admin/backend.html
    """
    # Récupération du nom et des informations de l'administrateur.
    admin = Admin.query.all()

    return render_template("admin/backend.html", admin=admin, logged_in=True)


# Route permettant de visualiser la liste des utilisateurs et leurs informations.
@admin_bp.route('/liste-utilisateurs')
@admin_required
def users_list():
    """
    Affiche la liste des utilisateurs enregistrés sur le blog avec leurs informations.

    Cette route est accessible uniquement aux administrateurs et permet de voir tous les utilisateurs
    enregistrés avec leurs détails tels que le nom de l'entreprise, l'email du référent, son téléphone.

    Les formulaires suivants sont disponibles sur cette page :
        - formuser : Formulaire d'enregistrement d'un nouvel utilisateur.

    Returns:
        template: La vue 'backend/users_list.html' avec les données utilisateur, et les formulaires pour
        gérer les actions d'enregistrement, de bannissement et de débannissement des utilisateurs.
    """

    # Instanciation des formulaires.
    formuser = UserRecording()
 
    # Récupération de la lettre pour le filtrage.
    lettre = request.args.get('lettre', type=str)

    # Filtrer les utilisateurs par le nom de l'entreprise si une lettre est fournie.
    if lettre:
        users = User.query.filter(User.enterprise_name.ilike(f'{lettre}%')).order_by(User.enterprise_name.asc()).all()
    else:
        users = User.query.order_by(User.enterprise_name.asc()).all()

    # Création d'une liste de dictionnaires mettant à disposition toutes les données utilisateur.
    user_data = [
        {
            'id': user.id, 
            'Nom de l\'entreprise': user.enterprise_name, 
            'Téléphone': user.phone, 
            'Email': user.email
        }
        for user in users
    ]

    return render_template("admin/users_list.html", users=user_data, formuser=formuser)


# Route permettant de supprimer un utilisateur.
@admin_bp.route("/supprimer-utilisateur/<int:id>", methods=["POST"])
@admin_required
def suppress_user(id):
    """
    Supprime définitivement un utilisateur du système en utilisant son ID.

    Cette route permet à l'administrateur de supprimer un utilisateur spécifique en le retirant
    complètement de la base de données. La suppression est effectuée via une requête POST, et après
    la suppression, un message de confirmation est affiché et l'administrateur est redirigé vers
    la page de liste des utilisateurs.

    Args:
        id (int): L'identifiant unique de l'utilisateur à supprimer.

    Context:
        user (User): Instance de l'utilisateur récupéré depuis la base de données à l'aide de l'ID fourni.

    Returns:
        Response: Une redirection vers la page de liste des utilisateurs après la suppression, avec un message
                  de confirmation du succès de l'opération.
    """
    # Récupération des utilisateurs.
    user = User.query.get(id)

    if user:
        # Suppression de l'utilisateur.
        db.session.delete(user)
        # Validation de l'action.
        db.session.commit()
        flash("L'utilisateur a été supprimé avec succès." + " " + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))
        
        # Fermeture de la session.
        db.session.close()
    else:
        # Affichage d'un message d'erreur si l'utilisateur n'est pas trouvé.
        flash("L'utilisateur n'a pas été trouvé.", "error")

    return redirect(url_for("admin.users_list"))


# Route permettant d'afficher la liste des commentaires des utilisateurs, avec option de filtrage.
@admin_bp.route('/liste-commentaires', methods=['GET', 'POST'])
@admin_required
def list_comments_customer():
    """
    Affiche la liste des commentaires des utilisateurs clients avec option de filtrage.

    Cette route permet aux administrateurs de visualiser tous les commentaires que les utilisateurs ont laissés. 
    Les commentaires sont regroupés par utilisateur. Il est possible de filtrer les utilisateurs en fonction de la première lettre de leur pseudo.

    Returns:
        Response: Une page HTML affichant les commentaires des utilisateurs, avec
                  des options de filtrage et de suppression.

    Templates:
        admin/user_comment.html: Le modèle utilisé pour rendre la page des commentaires des utilisateurs.

    Context:
        formuser (UserRecording): Formulaire utilisé pour gérer les utilisateurs.
        suppressform (SuppressCommentForm): Formulaire utilisé pour supprimer des commentaires de sujets.
        user_comment (dict): Dictionnaire où les clés sont le nom de l'entreprise des utilisateurs et les valeurs sont des
                              listes de commentaires associés à ces utilisateurs.
    """
    
    # Instanciation des formulaires.
    formuser = UserRecording()
    suppressform = SuppressCommentForm()

    # Récupération de la lettre de filtrage des utilisateurs à partir des paramètres de requête.
    lettre = request.args.get('lettre', type=str)

    # Filtrage des utilisateurs en fonction de la lettre choisie.
    if lettre:
        users = User.query.filter(User.enterprise_name.ilike(f'{lettre}%')).order_by(User.enterprise_name.asc()).all()
    else:
        users = User.query.order_by(User.enterprise_name.asc()).all()

    # Création du dictionnaire récupérant les commentaires par utilisateur.
    user_comment = {}

    # Pour chaque utilisateur, récupération de tous les commentaires associés.
    for user in users:
        # Récupération de tous les commentaires associés à l'utilisateur.
        comments = CustomerComment.query.filter_by(user_id=user.id).all()
        if comments:
            user_comment[user] = []
            for comment in comments:
                # Ajout du commentaire et du sujet associé dans le dictionnaire.
                user_comment[user].append({
                    'comment': comment
                })

    return render_template("admin/user_comment.html", user_comment=user_comment, formuser=formuser,
                           suppressform=suppressform)


# Route permettant de supprimer un commentaire.
@admin_bp.route("/supprimer-commentaires/<int:id>", methods=['GET', 'POST'])
@admin_required
def suppress_comment(id):
    """
    Supprime un commentaire.

    Cette route permet de supprimer un commentaire spécifique, identifié par son ID. 
    Après la suppression, un message de confirmation est affiché et l'administrateur 
    est redirigé vers la page d'administration.

    Args:
        id (int): L'identifiant unique du commentaire à supprimer.

    Returns:
        Response: Une redirection vers la page d'administration après la suppression.

    """
    # Récupération du commentaire du sujet à supprimer.
    comment = CustomerComment.query.get(id)

    if comment:
        # Suppression du commentaire.
        db.session.delete(comment)
        # Validation de l'action.
        db.session.commit()
        flash("Le commentaire a été supprimé avec succès." + " "
              + datetime.now().strftime(" le %d-%m-%Y à %H:%M:%S"))
        # Fermeture de la session.
        db.session.close()
        
    else:
        # Si le commentaire n'est pas trouvé, un message d'erreur peut être affiché.
        flash("Le commentaire demandé n'existe pas.", 'error')

    return redirect(url_for("admin.list_comments"))


# Route permettant d'accéder aux événements du calendrier du chat vidéo et de générer le lien administrateur.
@admin_bp.route("/calendrier-chat-vidéo")
@admin_required
def calendar():
    """
    Affiche la page du calendrier avec les événements de chat vidéo.

    Cette route est accessible uniquement aux administrateurs. Elle récupère toutes les demandes de chat vidéo,
    filtre celles qui sont validées, et prépare les données nécessaires pour l'affichage du calendrier.

    Pour chaque demande validée, un lien de connexion pour l'administrateur est généré et inclus dans les données
    envoyées à la page HTML du calendrier.

    Context:
        formrequest : Formulaire permettant la soumission d'une demande de chat vidéo.
        formlink : Formulaire permettant de soumettre le lien de chat vidéo à l'utilisateur.
        requests : Liste de toutes les demandes de chat vidéo récupérées depuis la table ChatRequest.
        rdv_data : Liste des rendez-vous filtrés avec les détails nécessaires pour le calendrier.

    :return: La page HTML du calendrier des chats vidéo, incluant les données des demandes et les formulaires
             pour la gestion des requêtes.
    """
    # Instanciation des formulaires.
    formrequest = ChatRequestForm()
    # Récupération de toutes les requêtes.
    requests = ChatRequest.query.all()
    
    # Instanciation du formulaire pour le lien su chat vidéo.
    formlink = UserLink()

    # Préparation des données des rendez-vous pour le calendrier.
    rdv_data = []

    # Filtrage et préparation des données pour chaque demande validée.
    for request in requests:
        if request.status == ChatRequestStatus.ACCEPTEE:
            # Génération du lien administrateur pour la réunion.
            admin_room_url = create_whereby_meeting_admin()

            rdv_data.append({
                'Nom de l\'entreprise': request.enterprise_name,
                'status': request.status,
                'content': request.request_content,
                'date_rdv': datetime.combine(request.date_rdv, request.heure),
                'link': admin_room_url
            })

            return render_template('admin/calendar.html',
                                   formrequest=formrequest,
                                   requests=requests,
                                   formlink=formlink,
                                   rdv_data=rdv_data)

    return render_template('admin/calendar.html', formrequest=formrequest, requests=requests,
                           rdv_data=rdv_data, formlink=formlink, ChatRequestStatus=ChatRequestStatus)


# Route permettant d'afficher les devis reçus par l'entreprise SethiarWorks.
@admin_bp.route("/liste-devis", methods=['GET', 'POST'])
def list_devis():
    """
    Fonction qui permet d'accéder à la liste de tous les devis reçus par le site de SethiarWorks.

    Les informations fournies par le formulaire de devis sont affichées au sein d'un tableau.
    Ces devis sont en attente de traitement. Lors de l'acceptation/refus d'un devis, un mail est envoyé à l'utilisateur
    afin de l'informer de la décision prise.

    Validation. Refus des devis.
    Suppression des devis possible.
    """
    # Instanciation du formulaire.
    formdevis = DevisRequestForm()
    # Récupération des devis
    list_user_devis = DevisRequest.query.all()

    # Regroupement des devis par statut.
    grouped_devis = defaultdict(list)
    for devis in list_user_devis:
        grouped_devis[devis.status.value].append(devis)
    
    return render_template("admin/demand_devis.html", 
                           grouped_devis=grouped_devis, formdevis=formdevis)


# Route permettant de joindre le formulaire pour enregistrer un utilisateur.
@admin_bp.route("/creer-utilisateur", methods=['GET', 'POST'])
def create_user_form():
    """
    Crée un utilisateur avec le rôle administrateur automatiquement.
    Utilise des informations prédéfinies et des variables d'environnement pour créer un administrateur.
    :return: Redirection vers la page du backend - admin/backend.html ou affiche un message d'erreur.
    """
    # Instanciation du formulaire.
    formuser = UserRecording()

    return render_template("admin/form_useradmin.html", formuser=formuser)


# Route permettant de traiter les données du formulaire de l'enregistrement d'un utilisateur.
@admin_bp.route('/enregistrement-utilisateur', methods=['GET', 'POST'])
def user_recording():
    """
    Gère l'enregistrement d'un nouvel utilisateur. Cette fonction traite à la fois les
    requêtes GET et POST. Lors d'une requête GET, elle affiche le formulaire
    d'enregistrement. Lors d'une requête POST, elle traite les données soumises par
    l'utilisateur, valide le formulaire, gère le fichier de photo de profil, redimensionne
    l'image et enregistre les informations de l'utilisateur dans la base de données.

    :return: Redirection vers la page de confirmation de l'email si l'inscription est réussie,
             sinon redirection vers la page d'enregistrement avec un message d'erreur.
    """
    formuser = UserRecording()

    if formuser.validate_on_submit():
        # Assainissement des données.
        lastname = formuser.lastname.data
        firstname = formuser.firstname.data
        enterprise_name = formuser.enterprise_name.data
        role = formuser.role.data
        phone = formuser.phone.data
        email = formuser.email.data
        password = formuser.password.data
        
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

        # Vérification de la soumission du fichier.
        if 'profil_photo' not in request.files or request.files['profil_photo'].filename == '':
            flash("Aucune photo de profil fournie.", "error")
            return redirect(url_for('user.user_registration'))

        profil_photo = request.files['profil_photo']
        if profil_photo and allowed_file(profil_photo.filename):
            photo_data = profil_photo.read()

            # Redimensionnement de l'image avec Pillow.
            try:
                img = Image.open(BytesIO(photo_data))
                img.thumbnail((75, 75))
                img_format = img.format if img.format else 'JPEG'
                output = BytesIO()
                img.save(output, format=img_format)
                photo_data_resized = output.getvalue()
            except Exception as e:
                flash(f"Erreur lors du redimensionnement de l'image : {str(e)}", "error")
                return redirect(url_for("admin.user_recording"))

            if len(photo_data_resized) > 5 * 1024 * 1024:  # 5 Mo
                flash("Le fichier est trop grand (maximum 5 Mo).", "error")
                return redirect(url_for("admin.user_recording"))

            photo_data = profil_photo.read()  # Lire les données binaires de l'image
        else:
            flash("Type de fichier non autorisé.", "error")
            return redirect(url_for("admin.user_recording"))

        new_user = User(
            lastname=lastname,
            firstname=firstname,
            enterprise_name=enterprise_name,
            role=role,
            phone=phone,
            email=email,
            
            password_hash=password_hash,
            salt=salt,
            
            # Stockage des données binaires de l'image.
            profil_photo=photo_data_resized
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Inscription réussie! Vous pouvez maintenant vous connecter.")
            return redirect(url_for("mail.send_confirmation_email_user", email=email))
        
        except Exception as e:
            
            db.session.rollback()
            flash(f"Erreur lors de l'enregistrement de l'utilisateur: {str(e)}", "error")
        
        
    return render_template("admin/backend.html", formuser=formuser)


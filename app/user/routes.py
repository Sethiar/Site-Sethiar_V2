"""
Code permettant de définir les routes concernant les fonctions des utilisateurs du blog comme l'enregistrement
et l'accès aux formulaires.
"""
import uuid

from datetime import datetime

from app.user import user_bp

from app.Models import db

from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_required, current_user


from app.forms.devis_request import DevisRequestForm
from app.forms.form_comment import CommentForm, ChangeCommentForm, SuppressCommentForm, \
    ReplyCommentForm, ChangeCommentReply, SuppressCommentReply

from app.forms.subject_comment import NewSubjectCommentForm

from app.Models.user import User
from app.Models.subject import Subject, SubjectStatus
from app.Models.comment import Comment
from app.Models.reply_comment import ReplyComment

from app.Models.comment import Comment, CommentStatus

from app.Models.reply_anonymous_comment import ReplyAnonymousComment, ReplyAnonymousCommentStatus

from app.Models.reply_user_anonyme_comment import ReplyUserAnonymousComment

from app.Models.reply_anonymous_user_comment import ReplyAnonymousUserComment, ReplyAnonymousUserCommentStatus
from app.Models.devis_request import DevisRequest

from app.mail.routes import mail_reply_comment, \
    send_mail_validate_demand, send_mail_inform_demand



# Méthode permettant de visualiser la photo de l'utilisateur.
@user_bp.route("/profil_photo/<int:user_id>")
def profil_photo(user_id):
    """
    Affiche la photo de profil d'un utilisateur ou une photo par defualt si anonyme.

    :param user_id : L'identifiant de l'utilisateur.

    :return : L'image de la photo de profil en tant que réponse HTTP avec le type MIME approprié.
    """
    user = User.query.get_or_404(user_id)
    if user.profil_photo:
        return user.profil_photo, {'Content-Type': 'image/jpeg'}
    else:
        return "No image found", 404



# Route permettant de renvoyer la photo de profil par défaut pour les utilisateurs anonymes.
@user_bp.route('/static/images/images_profil/default_profile_photo.png')
def profil_photo_anonymous():
    return url_for('static', filename='images/images_profil/default_profile_photo.png')


# route qui va permettre à un sujet connecté ou non de créer un sujet.
@user_bp.route("/comment/ajouter-sujet", methods=['POST'])
def add_subject_comment():
    """
    Permet à un utilisateur (connecté ou non) de créer un sujet.
    
        - Connecté --> Création du sujet dans l'espace de commentaire.
        - Anonyme --> En attende de validation par l'admin.
    """
    # Instanciation du formulaire.
    form = NewSubjectCommentForm()

    if form.validate_on_submit():
        # Utilise la méthode statique propre du modèle Subject
        subject = Subject.create(
            name=form.name.data,
            user=current_user if current_user.is_authenticated else None
        )
        
        # Ajout dans la base de données.
        db.session.add(subject)
        try:
            # Enregistrement dans la base de données.
            db.session.commit()
            if subject.is_anonymous:
                flash("Votre sujet a été soumis et est en attente de validation.", "info")
            else:
                flash("Sujet créé avec succès.", "success")
        except Exception as e:
            db.session.rollback()
            flash("Une erreur est survenue lors de l'ajout du sujet.", "error")
            print("Erreur lors de l'ajout du sujet :", e)

    return redirect(url_for('frontend.comments'))         
    

# Route permettant à un utilisateur connecté ou non de poster un commentaire.
@user_bp.route("/commentaires", methods=['POST'])
def comment_enterprise():
    """
    Permet à un utilisateur, connecté ou non, de laisser un commentaire.

    Returns :
         redirect : Redirige vers la page d'accueil après avoir laissé un commentaire.
    """
    # Récupération du contenu du commentaire.
    comment_content = request.form.get("comment_content")
    subject_id = request.form.get("subject_id")

    # Vérification que le contenu du commentaire existent.
    if not comment_content or not subject_id:
        flash("Le contenu du commentaire ou le sujet est manquant.", "error")
        return redirect(url_for("frontend.comments"))
    
    try:
        subject_id = int(subject_id)
    except ValueError:
        flash("Sujet invalide.", "error")
        return redirect(url_for("frontend.comments"))
    
    # Recherche du sujet dans la table Subject.
    subject = Subject.query.get(subject_id)
    if not subject or subject.status != SubjectStatus.VALIDE:
        flash("Sujet introuvable ou non validé.", "error")
        return redirect(url_for("frontend.comments"))

    # Gestion de l'anonymat
    anonymous_id = None
    if not current_user.is_authenticated:
        if "anonymous_id" not in session:
            session["anonymous_id"] = str(uuid.uuid4())
        anonymous_id = session["anonymous_id"]

    # Création du commentaire
    new_comment = Comment.create(
        comment_content=comment_content,
        subject=subject,
        user=current_user if current_user.is_authenticated else None,
        anonymous_id=anonymous_id
    )
    
    # Ajout dans la base de données.
    db.session.add(new_comment)
    try:
        # Enregistrement de la base de données.
        db.session.commit()
        flash("Commentaire soumis avec succès.", "success" if not new_comment.is_anonymous else "info")
    except Exception as e:
        db.session.rollback()
        print("Erreur lors de l'enregistrement du commentaire :", e)
        flash("Une erreur est survenue. Veuillez réessayer.", "error")
        return redirect(url_for("frontend.comments"))

    return redirect(url_for("frontend.subject_comment", subject_id=subject_id,
                            user_enterprise_name=new_comment.author_enterprise_name))


# Route permettant à un utilisateur connecté de modifier son commentaire.
@user_bp.route('/modification-commentaire-utilisateur/<int:id>', methods=['GET', 'POST'])
@login_required
def change_comment(id):
    """
    Permet à un utilisateur connecté de modifier son commentaire.
    N'autorise que l'auteur du commentaire à le modifier. Mais si l'utilisateur est anonyme,
    il ne peut modifier son commentaire.

    Args:
        id (int): L'id du commentaire à modifier.

    Returns:
        redirect: Redirige vers la page des commentaires.
    """
    comment = Comment.query.filter_by(id=id).first_or_404()

    # Vérification que l'utilisateur actuel est l'auteur du commentaire.
    if comment.user_id != current_user.id and comment.anonymous_id != session.get('anonymous_id'):
        flash('Vous n\'êtes pas autorisé à modifier ce commentaire.')
        return redirect(url_for('frontend.forum_subject'))

    formchange = ChangeCommentForm(obj=comment)

    if formchange.validate_on_submit():
        comment.comment_content = formchange.comment_content.data
        db.session.commit()
        flash('Commentaire modifié avec succès.')
        return redirect(url_for('frontend.comments'))
    else:
        flash('Erreur lors de la validation du commentaire.')

    return render_template('user/edit_comment.html', formchange=formchange, comment=comment)


# Route permettant à un utilisateur connecté de supprimer son commentaire.
@user_bp.route('/suppression-commentaire-utilisateur/<int:id>', methods=['POST'])
@login_required
def delete_comment(id):
    """
    Permet à un utilisateur connecté de supprimer son commentaire.
    N'autorise que l'auteur du commentaire à le supprimer. Mais si l'utilisateur est anonyme,
    il ne peut supprimer son commentaire.

    Args:
        id (int): L'id du commentaire à supprimer.

    Returns:
        redirect: Redirige vers la page des commentaires.
    """
    formsuppress = SuppressCommentForm()
    comment = Comment.query.filter_by(id=id).first_or_404()

    # Vérification que l'utilisateur actuel est l'auteur du commentaire.
    if comment.user_id != current_user.id and comment.anonymous_id != session.get('anonymous_id'):
        flash('Vous n\'êtes pas autorisé à supprimer ce commentaire.')
        return redirect(url_for('frontend.comments', comment=comment))

    db.session.delete(comment)
    db.session.commit()
    flash('Commentaire supprimé avec succès.')
    return redirect(url_for('frontend.comments', comment=comment))


# Route permettant à un utilisateur connecté ou non de répondre à un commentaire authentifié ou non.
@user_bp.route("/comment<int:comment_id>/reply_subject", methods=['GET', 'POST'])
def comment_replies(comment_id):
    """
    Permet à un utilisateur connecté ou non de répondre à un commentaire.
    """
    # Instanciation du formulaire.
    formreply = ReplyCommentForm()
    # Récupération de tous les commentaires.
    comment = Comment.query.get_or_404(comment_id)
    
    # Détermination du type de commentaire.
    comment_type = "anonymous" if comment.author_user_id is None else "customer"
    subject_id = comment.subject_id


    if formreply.validate_on_submit():

        reply_content = formreply.reply_content.data
        anonymous_id = session.get("anonymous_id")
        
        # Cas n°1 : utilisateur connecté.
        if current_user.is_authenticated:
            if comment_type == "customer":
                # Authentifié --> Authentifié.
                new_reply = ReplyComment(
                    reply_content=reply_content,
                    user_id=current_user.id,
                    comment_id=comment.id
                )    
            else:
                # Authentifié --> Anonyme.
                new_reply = ReplyUserAnonymousComment(
                    reply_content=reply_content,
                    user_id=current_user.id,
                    comment_id=comment.id,
                )    
                
        # Cas n°2 : Utilisateur anonyme.
        else:
            if not anonymous_id:
                # Génération d'un id au cas où.
                anonymous_id = str(uuid.uuid4())
                session["anonymous_id"] = anonymous_id
                
            if comment_type == "customer":
                # Anonyme --> Authentifié.
                new_reply = ReplyAnonymousUserComment(
                    reply_content = reply_content,
                    anonymous_id=anonymous_id,
                    comment_id=comment.id,
                    status=ReplyAnonymousUserCommentStatus.EN_ATTENTE
                )
            # Réponse anonyme.
            else:
                # Anonyme --> Anonyme
                new_reply = ReplyAnonymousComment(
                    reply_content=reply_content,
                    anonymous_id=anonymous_id,
                    comment_id=comment.id,
                    status=ReplyAnonymousCommentStatus.EN_ATTENTE                    
                )
                   
        # Ajout dans la base de données.
        db.session.add(new_reply)
        # Enregistrement dans la base de données.
        db.session.commit()
        flash("La réponse au commentaire a bien été enregistrée.", "success")


        # Notification par e-mail si nécessaire
        if (
            current_user.is_authenticated
            and comment_type == "customer"
            and comment.author_user and comment.author_user.email
        ):
            mail_reply_comment(comment.author_user.email, comment.subject)

        flash("La réponse a bien été enregistrée.", "success")
        return redirect(url_for("frontend.subject_comment", subject_id=subject_id))

    return render_template("user/reply_comment.html", formreply=formreply, comment=comment)


# Route permettant à un utilisateur connecté de modifier sa réponse à un commentaire.
@user_bp.route('/modification-reponse-utilisateur/<int:id>', methods=['GET', 'POST'])
@login_required
def change_reply(id):
    """
    Permet à un utilisateur connecté de modifier sa réponse à un commentaire.

    Args:
        id (int): L'id de la réponse à modifier.

    Returns:
        redirect: Redirige vers la page du sujet du forum après modification de la réponse
    """
    reply = ReplyComment.query.filter_by(id=id).first_or_404()

    # Vérification que l'utilisateur actuel est l'auteur du commentaire
    if reply.user_id != current_user.id:
        flash('Vous n\'êtes pas autorisé à modifier cette réponse.')
        return redirect(url_for('frontend.comments', comment_id=reply.comment_id))

    formchangereply = ChangeCommentReply(obj=reply)

    if formchangereply.validate_on_submit():
        reply.reply_content = formchangereply.reply_content.data
        
        # Mise à jour dans la base de données.
        db.session.commit()
        flash('Réponse modifiée avec succès.')
        return redirect(url_for('frontend.comments', comment_id=reply.comment_id))
    else:
        flash('Erreur lors de la validation du commentaire.')

    return render_template('user/edit_reply.html', formchangereply=formchangereply, reply=reply)


# Route permettant à un utilisateur connecté de supprimer sa réponse à un commentaire.
@user_bp.route('/suppression-reponse-utilisateur/<int:id>', methods=['POST'])
@login_required
def delete_reply(id):
    """
    Permet à un utilisateur connecté de supprimer sa réponse à un commentaire.

    Args:
        id (int): L'id de la réponse à supprimer.

    Returns:
        redirect: Redirige vers la page du sujet du forum après suppression de la réponse.
    """
    formsuppressreply = SuppressCommentReply()
    reply = ReplyComment.query.filter_by(id=id).first_or_404()

    # Vérification que l'utilisateur actuel est l'auteur du commentaire
    if reply.user_id != current_user.id:
        flash('Vous n\'êtes pas autorisé à supprimer cette réponse.')
        return redirect(url_for('frontend.frontend', comment_id=reply.comment_id))

    # Obtenir le subject_id avant de supprimer la réponse
    comment_id = reply.comment_id

    db.session.delete(reply)
    db.session.commit()
    flash('Réponse supprimée avec succès.')

    return redirect(url_for('frontend.comments', comment_id=comment_id))



# Route permettant de renvoyer la demande de devis.
@user_bp.route("/demande-de-devis-formulaire", methods=['GET', 'POST'])
def user_devis():
    """
    Affiche le formulaire afin de remplir la demande de devis.

    :return: le formulaire de la demande de devis.
    """

    # Création de l'instance du formulaire
    form_devis = DevisRequestForm()

    return render_template("user/devis_form.html", form_devis=form_devis)


# Route permettant d'enregistrer la demande de devis.
@user_bp.route("/demande-de-devis-envoi-formulaire", methods=['GET', 'POST'])
def user_devis_demand():
    """
    Fonction qui va récupérer les données de la demande de devis et les enregistrer au sein de la base de données.

    :return: Page de remerciement de la demande de devis ou retour à la page du formulaire en cas d'erreur.
    """
    # Création de l'instance du formulaire
    form_devis = DevisRequestForm()

    if form_devis.validate_on_submit():
        
        # Création d'un nouvel objet Devis avec les données du formulaire.
        new_devis = DevisRequest(
            lastname=form_devis.lastname.data,
            firstname=form_devis.firstname.data,
            phone=form_devis.phone.data,
            enterprise_name=form_devis.enterprise_name.data,
            email=form_devis.email.data,
            project_type=form_devis.project_type.data,
            devis_content=form_devis.devis_content.data
        )

        try:
            db.session.add(new_devis)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash("Une erreur est survenue lors de l'enregistrement. Veuillez réessayer.", "error")
            return redirect(url_for('user.user_devis_demand'))
        else:
            send_mail_validate_demand(new_devis)
            send_mail_inform_demand()
            flash("Votre demande de devis a été envoyée avec succès !!", "success")
            return redirect(url_for('user.user_devis_thanks'))
    else:
        # Affichage des erreurs de validation du formulaire.
        for field, errors in form_devis.errors.items():
            for error in errors:
                flash(f"Erreur dans le champ {field}: {error}", "error")

    # Si le formulaire est invalide ou qu'on arrive via GET
    return render_template("user/devis_form.html", form=form_devis)


# Route pour la page de remerciement
@user_bp.route("/demande-de-devis-remerciement")
def user_devis_thanks():
    """
    Page affichée après l'envoi réussi d'une demande de devis.
    """
    
    return render_template("user/devis_form_thanks.html")
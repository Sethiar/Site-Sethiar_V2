"""
Code permettant de définir les routes concernant les fonctions des utilisateurs du blog comme l'enregistrement
et l'accès aux formulaires.
"""

from datetime import datetime

from app.user import user_bp

from app.Models import db

from markupsafe import escape
from flask import render_template, redirect, url_for, request, flash, jsonify 
from flask_login import login_required, current_user


from app.forms.devis_request import DevisRequestForm
from app.forms.form_comment import CommentForm, ChangeCommentForm, SuppressCommentForm, \
    ReplyCommentForm, ChangeCommentReply, SuppressCommentReply

from app.forms.subject_comment import NewSubjectCommentForm

from app.Models.user import User
from app.Models.subject_comment import SubjectComment
from app.Models.comment_customer import CustomerComment
from app.Models.reply_comment import CommentReply

from app.Models.devis_request import DevisRequest

from app.mail.routes import mail_reply_comment, \
    send_mail_validate_demand, send_mail_inform_demand, send_confirmation_email_admin

from app.extensions import allowed_file


# Méthode permettant de visualiser la photo de l'utilisateur.
@user_bp.route("/profil_photo/<int:user_id>")
def profil_photo(user_id):
    """
    Affiche la photo de profil d'un utilisateur.

    :param user_id : L'identifiant de l'utilisateur.

    :return : L'image de la photo de profil en tant que réponse HTTP avec le type MIME approprié.
    """
    user = User.query.get_or_404(user_id)
    if user.profil_photo:
        return user.profil_photo, {'Content-Type': 'image/jpeg'}
    else:
        return "No image found", 404
    
    
# Route permettant d'ajouter un sujet à l'espace de commentaires une fois connecté.
@user_bp.route("/comment/ajouter-sujet", methods=['POST'])
@login_required
def add_subject_comment():
    """
    Permet à un utilisateur de créer un nouveau sujet pour l'espace de commentaires'.

    Returns :
        redirect : Redirige vers la page d'accueil des commentaires après avoir ajouté le sujet.
    """

    # Création de l'instance du formulaire.
    formsubjectcomment = NewSubjectCommentForm()

    # Passage de la valeur booléenne d'authentification au template.
    is_authenticated = current_user.is_authenticated
    author = current_user.enterprise_name

    # Debug: Vérification du type.
    print("Type of is_authenticated:", type(is_authenticated))

    if request.method == "POST":
        # Saisie du nom du sujet.
        nom_subject_comment = escape(request.form.get("nom"))
        subject_comment = SubjectComment(nom=nom_subject_comment, author=current_user.enterprise_name)

        # Enregistrement du sujet dans la base de données.
        db.session.add(subject_comment)
        db.session.commit()

    # Récupération de tous les sujets après l'ajout du nouveau sujet.
    subjects = SubjectComment.query.all()

    return render_template("frontend/subject_comments.html", formsubjectcomment=formsubjectcomment, subjects=subjects,
                           is_authenticated=is_authenticated) + '#sujet'


# Route permettant à un utilisateur connecté de poster un commentaire.
@user_bp.route("/commentaires", methods=['POST'])
@login_required
def comment_enterprise():
    """
    Permet à un utilisateur connecté de laisser un commentaire.

    Returns :
         redirect : Redirige vers la page d'accueil après avoir laissé un commentaire.
    """
    
    # Passage de la valeur booléenne d'authentification au template.
    is_authenticated = current_user.is_authenticated
    
    # Debug: Vérification du type.
    print("Type de is_authentificated:", type(is_authenticated))
    
    # Utilisation de current_user pour obtenir le nom de l'entreprise et l'id utilisateur.
    user_enterprise_name = current_user.enterprise_name
    user_id = current_user.id
    
 
    # Récupération du contenu du commentaire.
    comment_content = request.form.get("comment_content")
    subject_id = request.form.get("subject_id")

    
    # Vérification que le contenu du commentaire existent.
    if not comment_content or not subject_id:
        flash("Le contenu du commentaire ou le sujet est manquant.", "error")
        
        # Redirige vers la page des commentaires.
        return redirect(url_for("frontend.comments"))  
    
    try:
        subject_id = int(subject_id)
    except ValueError:
        flash("Sujet invalide.", "error")
        return redirect(url_for("frontend.comments"))
    
    
    # Création d'un nouvel objet de commentaire avec les données actuelles.
    new_comment = CustomerComment(
        comment_content=comment_content,
        subject_id=subject_id,
        user_id=current_user.id
        )

    # Ajouter le nouveau commentaire à la base de données.
    db.session.add(new_comment)
    db.session.commit()

    # Redirection sur la page des commentaires.
    return redirect(url_for("frontend.comments", is_authenticated=is_authenticated, subject_id=subject_id, 
                            user_enterprise_name=user_enterprise_name))


# Route permettant à un utilisateur connecté de modifier son commentaire.
@user_bp.route('/modification-commentaire-utilisateur/<int:id>', methods=['GET', 'POST'])
@login_required
def change_comment(id):
    """
    Permet à un utilisateur connecté de modifier son commentaire.

    Args:
        id (int): L'id du commentaire à modifier.

    Returns:
        redirect: Redirige vers la page des commentaires.
    """
    comment = CustomerComment.query.filter_by(id=id).first_or_404()

    # Vérification que l'utilisateur actuel est l'auteur du commentaire.
    if comment.user_id != current_user.id:
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

    Args:
        id (int): L'id du commentaire à supprimer.

    Returns:
        redirect: Redirige vers la page des commentaires.
    """
    formsuppress = SuppressCommentForm()
    comment = CustomerComment.query.filter_by(id=id).first_or_404()

    # Vérification que l'utilisateur actuel est l'auteur du commentaire.
    if comment.user_id != current_user.id:
        flash('Vous n\'êtes pas autorisé à supprimer ce commentaire.')
        return redirect(url_for('frontend.comments', comment=comment))

    db.session.delete(comment)
    db.session.commit()
    flash('Commentaire supprimé avec succès.')
    return redirect(url_for('frontend.comments', comment=comment))


# Route permettant à un utilisateur connecté de répondre à un commentaire une fois connecté.
@user_bp.route("/comment<int:comment_id>/reply_subject", methods=['GET', 'POST'])
@login_required
def comment_replies(comment_id):
    """
    Permet à un utilisateur connecté de répondre à un commentaire.

    Args :
        comment_id (int) : L'identifiant du commentaire auquel répondre.

    Returns :
        redirect ou render_template : Redirige vers la page ddes commentaires après avoir ajouté une réponse,
                                      ou affiche le formulaire de réponse si la méthode est GET.
    """
   
    # Création de l'instance du formulaire.
    formreply = ReplyCommentForm()

    # Récupérer le commentaire par son id.
    comment = CustomerComment.query.get(comment_id)

    if not comment:
        flash("Le commentaire n'a pas été trouvé.", "error")
        return redirect(url_for("frontend.comments"))

    if formreply.validate_on_submit():
        # Obtention de l'utilisateur actuel à partir du nom de l'entreprise.
        user = current_user

        if not user.enterprise_name:
            flash("Utilisateur non trouvé.", "error")
            return redirect(url_for("functional.connexion_requise"))

        # Obtenir le contenu du commentaire à partir de la requête POST.
        reply_content = formreply.reply_content.data


        # Créer une nouvelle réponse au commentaire.
        new_reply = CommentReply(reply_content=reply_content, user_id=user.id, comment_id=comment_id)

        # Ajouter le nouveau commentaire à la table de données.
        db.session.add(new_reply)
        db.session.commit()

        flash("La réponse au commentaire a bien été enregistrée.", "success")
        mail_reply_comment(comment.user.email, comment.subject)

        # Redirection vers la page du sujet du forum
        return redirect(url_for("frontend.comments", comment_id=comment_id))

    # Si le formulaire n'est pas validé ou en méthode GET, affichez le formulaire de réponse
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
    reply = CommentReply.query.filter_by(id=id).first_or_404()

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
    reply = CommentReply.query.filter_by(id=id).first_or_404()

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
        # Afficher les erreurs de validation du formulaire
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
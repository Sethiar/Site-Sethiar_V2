"""
Code permettant de définir les routes concernant les fonctions des utilisateurs du site du frontend.
"""
import uuid 

from flask import render_template, abort


from flask_login import current_user

from app.frontend import frontend_bp

from app.forms.subject_comment import NewSubjectCommentForm
from app.forms.form_comment import CommentForm
from app.forms.form_comment import SuppressCommentForm
from app.forms.form_comment import SuppressCommentReply

from app.Models.subject_comment import SubjectComment
from app.Models.comment_customer import CustomerComment


# Route permettant d'accéder à la zone des commentaires du site.
@frontend_bp.route('acces-commentaires')
def comments():
    """
    Route permettant d'accéder à l'espace commentaires du site.

    :return: templates HTML 'frontend/comments.html.
    """
    # Instanciation du formulaire.
    formsubjectcomment = NewSubjectCommentForm()

    # Récupération de tous les sujets de la table de données.
    subjects = SubjectComment.query.all()

    # Passage de la valuer booléenne d'authentification.
    is_authenticated = current_user.is_authenticated

    # Debug : Vérification du type.
    print("Type of is_authenticated : ", type(is_authenticated))

    return render_template('frontend/comments.html', formsubjectcomment=formsubjectcomment, subjects=subjects,
                           is_authenticated=is_authenticated)


# Route afin de visualiser un sujet de l'espace de commentaires particulier.
@frontend_bp.route("/acces-sujet-comment/<int:subject_id>", methods=['GET', 'POST'])
def subject_comment(subject_id):
    """
    Route permettant d'accéder à un sujet de commentaire spécifique de l'espace commentaires.

    Args:
        subject_id (int) : L'identifiant du sujet à afficher.

    Returns :
        Template HTML 'frontend/subject_comments.html' avec les détails du sujet et ses commentaires associés.

    Raises :
        404 error : Si aucun sujet correspondant à l'ID spécifié n'est trouvé dans la base de données.
    """
    # Si l'utilisateur est anonyme, crée un UUID unique pour cette session
    if not current_user.is_authenticated:
        # Génère un UUID unique pour un utilisateur anonyme
        user_id = str(uuid.uuid4())  
    else:
        # Si l'utilisateur est authentifié, utilise son ID
        user_id = current_user.id 
        
    # Création de l'instance des formulaires.
    formcomment = CommentForm()
    formsuppress = SuppressCommentForm()
    formsuppressreply = SuppressCommentReply()

    # Récupération du sujet spécifié par l'ID depuis la base de données.
    subject = SubjectComment.query.get_or_404(subject_id)

    # Passage de la valeur booléenne d'authentification au template.
    is_authenticated = current_user.is_authenticated

    # Debug : Vérification du type.
    print("Type of is authenticated : ", type(is_authenticated))

    # Vérification de l'existence du sujet.
    if not subject:
        # Si le sujet n'existe pas dans la base de données, erreur 404 renvoyée.
        abort(404)

    # Récupération des commentaires associés à ce sujet.
    comment_subject = CustomerComment.query.filter_by(subject_id=subject_id).all()


    return render_template("frontend/subject_comments.html", subject=subject, subject_id=subject_id,
                           user_id=user_id, formsuppress=formsuppress, 
                           formsuppressreply=formsuppressreply, comment_subject=comment_subject, 
                           formcomment=formcomment, is_authenticated=is_authenticated)

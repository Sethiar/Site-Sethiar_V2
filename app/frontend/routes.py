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

from app.Models.subject import Subject, SubjectStatus

from app.Models.comment import Comment, CommentStatus

from app.Models.reply_comment import ReplyComment

from app.Models.reply_anonymous_comment import ReplyAnonymousComment, ReplyAnonymousCommentStatus

from app.Models.reply_anonymous_user_comment import ReplyAnonymousUserComment, ReplyAnonymousUserCommentStatus

from app.Models.reply_user_anonyme_comment import ReplyUserAnonymousComment


# Route permettant d'accéder à la zone des commentaires du site.
@frontend_bp.route('acces-commentaires')
def comments():
    """
    Route permettant d'accéder à l'espace commentaires du site.

    :return: templates HTML 'frontend/comments.html.
    """
    # Instanciation du formulaire.
    formsubjectcomment = NewSubjectCommentForm()
    
    # Récupération de tous les sujets validés.
    subjects = Subject.query.filter_by(status=SubjectStatus.VALIDE)

    # Passage de la valuer booléenne d'authentification.
    is_authenticated = current_user.is_authenticated

    # Debug : Vérification du type.
    print("Type of is_authenticated : ", type(is_authenticated))

    return render_template('frontend/comments.html', formsubjectcomment=formsubjectcomment,
                           subjects=subjects, is_authenticated=is_authenticated)


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
    subject = Subject.query.get_or_404(subject_id)
    
    # Création de l'instance des formulaires.
    formcomment = CommentForm()
    formsuppress = SuppressCommentForm()
    formsuppressreply = SuppressCommentReply()
    formsubject = NewSubjectCommentForm()
    
    # Récupération des commentaires associés à ce sujet.
    comment = Comment.query.filter_by(
        subject_id=subject_id, 
        status=CommentStatus.VALIDE
        ).all()
    
    # Récupération des réponses authentifiés à un commentaire authentifié.
    replies = {
        comment.id: ReplyComment.query.filter_by(
            comment_id=comment.id
        ).all()
        for comment in comment
    }
    
    # Récupération des réponses anonymes associées à un commentaire anonyme.
    anonymous_replies = {
        comment.id: ReplyAnonymousComment.query.filter_by(
            comment_id=comment.id,
            status=ReplyAnonymousCommentStatus.VALIDEE
        ).all()
        for comment in comment
    }
    
    # Récupération des réponses anonymes associées à des commentaires d'authentifiés.
    anonymous_user_replies = {
        comment.id: ReplyAnonymousUserComment.query.filter_by(
            comment_id=comment.id,
            status=ReplyAnonymousUserCommentStatus.VALIDEE
        ).all()
        for comment in comment
    }
    
    # Récupération des réponses d'authentifiés à des commentaires d'anonymes.
    user_anonymous_replies = {
        comment.id: ReplyUserAnonymousComment.query.filter_by(
            comment_id=comment.id,
        ).all()
        for comment in comment
    }
    
    return render_template("frontend/subject_comments.html", 
                           subject=subject, subject_id=subject_id, user_id=current_user.id if current_user.is_authenticated else str(uuid.uuid4()),
                           formsuppress=formsuppress, formsuppressreply=formsuppressreply, 
                           formsubject=formsubject, comment=comment,
                           replies=replies,
                           anonymous_replies=anonymous_replies, anonymous_user_replies=anonymous_user_replies,
                           user_anonymous_replies=user_anonymous_replies,
                           formcomment=formcomment, is_authenticated=current_user.is_authenticated
                           )

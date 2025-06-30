"""
Code renvoyant le code du formulaire de la saisie d'un commentaire.
"""

#------------------------------------------#
# Formulaire pour poster un commentaire    #
#------------------------------------------#
# Formulaire pour modifier un commentaire  #
#------------------------------------------#
# Formulaire pour supprimer un commentaire #
#------------------------------------------#


from flask_wtf import FlaskForm

from wtforms import  StringField, TextAreaField, SubmitField, HiddenField

from wtforms.validators import DataRequired


# Formulaire permettant à un utilisateur de poster un commentaire sur le site de l'entreprise SethiarWorks.
class CommentForm(FlaskForm):
    """
    Formulaire pour ajouter un commentaire sur le site de l'entreprise SethiarWorks.
    
    Attributes: 
        comment_content (TextAreaField): Contenu du commentaire.
        enterprise_name (StringField): Champ pour le nom de l'entreprise.
        csrf_token (HiddenField): Jeton CSRF pour la sécurité du formulaire.
    """
    
    # Contenu du commentaire.
    comment_content = TextAreaField(
        "Contenu du commentaire",
        validators=[DataRequired()],
        render_kw={"placeholder": "Saisie de votre commentaire"}        
    )
    
    # Nom de l'entreprise.
    enterprise_name = StringField(
        "Nom de l'entreprise",
        validators=[DataRequired()],
        render_kw={"placeholder": "Nom de votre entreprise"}
    )
    
    # Action de soumettre le formulaire.
    submit = SubmitField("Soumettre le commentaire")
    
    # Token de sécurité.
    csrf_token = HiddenField()
    
    
# Formulaire permettant à l'utilisateur de modifier son commentaire.
class ChangeCommentForm(FlaskForm):
    """
    Formulaire permettant de modifier le commentaire de et par l'utilisateur.
    
    Attributes:
        comment_content (TextAreaField): contenu du commentaire.
        submit (SubmitField): Bouton de soumission du formulaire.
        csrf_token (HiddenField) : Jeton CSRF pour la sécurité du formulaire.
    """
    
    # Contenu du commentaire.
    comment_content = TextAreaField(
        "Contenu du commentaire",
        validators=[DataRequired()],
        render_kw={"placeholder": "Saisie du commentaire"}
    )
    
    # Action de soumettre le formulaire
    submit= SubmitField("Soumettre le commentaire")
    
    # Token de sécurité.
    csrf_token = HiddenField()
    
    
# Formulaire permettant de supprimer le commentaire d'un utilisateur.
class SuppressCommentForm(FlaskForm):
    """
    Formulaire permettant de supprimer le commentaire de et par l'utilisateur.
    
    Attributes:
        submit = SubmitField("Supprimer le commentaire)
        csrf_token (HiddenField): Jeton csrf pour la sécurité du commentaire.
    """
    
    # Action de soumettre le formulaire.
    submit = SubmitField("Supprimer le commentaire")
    
    # Token de sécurité.
    csrf_token = HiddenField()
    

#--------------------------------------------------------#
# Formulaire pour poster une réponse à un commentaire    #
#--------------------------------------------------------#
# Formulaire pour modifier une réponse à un commentaire  #
#--------------------------------------------------------#
# Formulaire pour supprimer une réponse à un commentaire #
#--------------------------------------------------------#


# Formulaire peremttant de répondre à un commentaire.
class ReplyCommentForm(FlaskForm):
    """
    Formulaire permettant de répondre à un commentaire sur le site entreprise de SethiarWorks.
    
    Attributes:
        reply_content (TextAreaField): Champ de texte pour la réponse au commentaire.
        comment_id (HiddenField): Champ caché pour l'ID du commentaire.
        submit (SubmitField): Bouton de soumission du commentaire.
        csrf_token (HiddenField): Jeton pour la sécurité du formulaire.
    """
    
    # Contenu de la réponse.
    reply_content = TextAreaField(
        "Réponse au commentaire",
        validators=[DataRequired()],
        render_kw={"placeholder": "Votre réponse"}
    )
    
    # Champ pour stocker l'ID du commentaire parent.
    comment_id = HiddenField("ID du commentaire")
    
    # Action de soumettre le commentaire.
    submit = SubmitField("Soumettre la réponse")
    
    # Token de sécurité.
    csrf_token = HiddenField()
    
    
# Formulaire permettant à un utilisateur de modifier sa réponse à un commentaire.
class ChangeCommentReply(FlaskForm):
    """
    Formulaire permettant de modifier sa réponse à un commentaire.

    Attributes:
        reply_content: Contenu du commentaire de l'utilisateur.
        submit (SubmitField): Bouton de soumission du commentaire.
        csrf_token (HiddenField): Jeton CSRF pour la sécurité du formulaire.
    """
    
    # Contenu de la réponse.
    reply_content = TextAreaField(
        "Contenu de la réponse",
        validators=[DataRequired()],
        render_kw={"placeholder": "Votre réponse"}
    )
    
    # Action de soumettre le commentaire.
    submit = SubmitField("Soumettre la réponse")
    
    # Token de sécurité.
    csrf_token = HiddenField()    
    
    
# Formulaire permettant à un utilisateur de supprimer sa réponse à un commentaire.
class SuppressCommentReply(FlaskForm):
    """
    Formulaire permettant à un utilisateur de supprimer sa réponse à un commentaire.

    Attributes :
        reply_id (HiddenField) : Champ caché pour l'ID de la réponse à supprimer.
        submit (SubmitField): Bouton de soumission du formulaire.
        csrf_token (HiddenField): Jeton CSRF pour la sécurité du formulaire.
    """

    # Réponse à supprimer en fonction de son id.
    reply_id = HiddenField(
        "reply_id",
        validators=[DataRequired()]
    )

    # Action de soumettre le commentaire.
    submit = SubmitField('Supprimer')    
    
    # Token de sécurité.
    csrf_token = HiddenField()    
    
    
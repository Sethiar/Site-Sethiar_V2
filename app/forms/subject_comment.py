"""
Code fournissant les formulaires concernant les sujets de l"'espace de commentaires du site de l'entreprise SethiarWorks.
"""

#==========================================================================================#
# Enregistrement d'un nouveau sujet de commentaire / Suppression d'un sujet de commentaire #
#==========================================================================================#

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, HiddenField
from wtforms.validators import DataRequired


# Formulaire permettant la création d'un nouveau sujet sur l'espace de commentaires.
class NewSubjectCommentForm(FlaskForm):
    """
    Formulaire pour ajouter un nouveau sujet sur l'espace de commentaires.

    Attributes:
        nom (StringField) : Champ pour le nom du sujet pour l'espace de commentaires.

    Example :
        form = NewSubjectCommentForm()
    """
    # Nom du sujet.
    name = StringField(
        "Ajouter un nouveau sujet",
        validators=[DataRequired()],
        render_kw={'placeholder': "Nouveau sujet"}
    )

    # Action de soumettre le formulaire.
    submit = SubmitField("Ajouter le sujet")
    
    # Token de sécurité.
    csrf_token = HiddenField()


# Formulaire permettant de supprimer un sujet de l'espace de commentaires.
class SuppressSubject(FlaskForm):
    """
    Formulaire pour supprimer un sujet de la section espace de commentaires.

    Attributes :
        subject_id (HiddenField) : Champ caché pour l'ID du sujet à supprimer.
        submit (SubmitField): Bouton de soumission du formulaire.
    """
    # Champ caché pour l'id du sujet.
    subject_id = HiddenField(
        'Subject_id',
        validators=[DataRequired()]
    )

    # Action de soumettre le formulaire.
    submit = SubmitField('Supprimer')

    # Token de sécurité.
    csrf_token = HiddenField()
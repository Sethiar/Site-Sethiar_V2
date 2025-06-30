"""
Code renvoyant le code du formulaire de changement de mot de passe utilisateur.
"""

#--------------------------------------------------------------------#
# Formulaire permettant de réinitialiser le mot de passe utilisateur #
#--------------------------------------------------------------------# 

from flask_wtf import FlaskForm

from flask_wtf.file import DataRequired

from wtforms import EmailField, PasswordField, SubmitField, HiddenField

from wtforms.validators import EqualTo


# Formulaire pour mot de passe oublié.
class ForgetPassword(FlaskForm):
    """
    Ce formulaire permet de réinitialiser le mot de passe utilisateur.

    Attributes:
        email(EmailField): Email de l'utilisateur voulant réinitialiser son mot de passe.
        new_password (PasswordField): Nouveau mot de passe.
            csrf_token (HiddenField): Jeton CSRF pour la sécurité du formulaire.
    """

    email = EmailField(
        "Email",
        validators=[DataRequired()],
        render_kw={"placeholder": "Renseignez ici votre email."}
    )

    # Action de soumettre le formulaire.
    submit = SubmitField("Réinitialiser le mot de passe.")

    # Token de sécuité.
    csrf_token = HiddenField()


# Formulaire pour enregistrer le nouveau mot de passe.
class RenamePassword(FlaskForm):
    """
    Ce formulaire permet d'enregistrer un nouveau mot de passe.
    
    Attributes:
        new_password (PasswordField): Nouveau mot de passe.
        confirm_password (PasswordField): Confirmation du nouveau mot de passe.
        csrf_token (HiddenFields): Jeton csrf pour la sécurité du formulaire.
    """
    
    # Champ pour le nouveau password.
    new_password = PasswordField(
        "Nouveau mot de passe utilisateur",
        validators=[DataRequired()],
        render_kw={"placeholder": "Nouveau mot de passe"}
    )
    
    # Champ pour confirmer le nouveau mot de passe.
    confirm_password = PasswordField(
        "Confirmer le nouveau mot de passe",
        validators=[DataRequired(), EqualTo('new_password', message="Les mots de passe doivent correspndre.")],
        render_kw={"placeholder": "Confirmation du nouveau mot de passe"}
    )
    
    # Action de soumettre le formulaire.
    submit = SubmitField("Réinitialiser le mot de passe.")

    # Token de sécuité.
    csrf_token = HiddenField()
    
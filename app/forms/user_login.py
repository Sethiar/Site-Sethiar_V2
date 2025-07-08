"""
Code permettant de se connecter en tant qu'utilisateur.
"""

#--------------------------------#
# Connexion Utilisateur / Client #
#--------------------------------#

from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, HiddenField

from wtforms.validators import DataRequired


class UserConnection(FlaskForm):
    """
    Formulaire de connexion pour les clients de l'entreprise afin de laisser un commentaire.
    
    Attributes:
        name_enterprise (StringField): Champ pour le pseudo du client utilisateur.
        password (PasswordField): Champ pour le password de l'utilisateur.
        submit (SubmitField): Bouton de soumission du commentaire.
        csrf_token (HiddenField): Jeton CSRF pour la sécurité des formulaires.
    """
    
    # Champ pour le nom d'entreprise.
    enterprise_name = StringField(
        "Nom de l'entreprise",
        validators=[DataRequired()],
        render_kw={"placeholder": "Nom entreprise"}
    )
    
    # Champ pour le password.
    password = PasswordField(
        "Mot de passe",
        validators=[DataRequired()],
        render_kw={'placeholder': "Mot de passe"}
    )
    
    # Action de soumettre le formulaire.
    submit = SubmitField("Se connecter")
    
    # Jeton CSRF pour la sécurité du formulaire.
    csrf_token = HiddenField()
    
    
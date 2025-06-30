"""
Code permettant de se connecter en tant qu'administrateur.
"""

#-------------------------------------------#
# Formulaire de connexion administrateur    #
#-------------------------------------------# 
 

from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField, HiddenField
    
from wtforms.validators import DataRequired


class AdminConnection(FlaskForm):
    """
    Formulaire de connexion pour l'administrateur.
    
    Attributes: 
        pseudo (StringField): Champ pour le pseudo de l'administrateur.
        role (StringField): Champ pour le rôle.
        password (PasswordField): Champ pour la password dd el'administrateur.
        submit (SubmitField): Champ pour la soumission du formulaire.
        csrf_token (HidenField): Champ du jeton csrf pour la sécurité des formulaires.
    """
    
    # Champ pour le pseudo.
    pseudo = StringField(
        "Pseudo adminsitrateur",
        validators=[DataRequired()],
        render_kw={"placeholder":"Votre pseudo"}
    )
    
    # Champ pour le rôle.
    role = StringField(
        "Rôle",
        validators=[DataRequired()],
        render_kw={"placeholder": "Votre rôle"}
    )
    
    # Champ pour le mot de passe.
    password = PasswordField(
        "Mot de passe",
        validators=[DataRequired()],
        render_kw={"placeholder": "Votre mot de passe"}
    )
    
    # Action de soumettre le formulaire.
    submit = SubmitField("Se connecter à l'espace administrateur")
    
    # Token de sécurité.
    csrf_token = HiddenField()
    
    
"""
Code permettant à l'administrateur d'inscrire un client au sein de la base de données.
"""


#-------------------------------------------------#
# Enregistrement d'un nouvel Utilisateur / Client #
#-------------------------------------------------#


from flask_wtf import FlaskForm

from wtforms import StringField, EmailField, PasswordField, FileField, \
    SubmitField, HiddenField, TelField
from flask_wtf.file import FileAllowed, FileRequired

from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.Models.user import User


# Classe permettant d'enregistrer les utilisateurs dans la table de données User.
class UserRecording(FlaskForm):
    """
    Formulaire d'inscription pour les utilisateur du site.

    Attributes:
        lastname (StringField): Nom du client.
        firstname (StringField): Prénom du client.
        phone (TelField): Téléphone du client.
        enterprise_name (StringField): Nom de l'entreprise.
        role (Stringfield): Role de l'utilisateur.
        email (EmailField): Email du référent projet.
        password (PasswordField): Champ pour le mot de passe de l'utilisateur.
        password2 (PasswordField): Champ pour la vérification du mot de passe utilisateur.
        profil_photo (FileField): Champ pour le logo de l'entreprise.
        submit (SubmitField): Bouton de soumission du formulaire.
        csrf_token (HiddenField): Jeton CSRF.

    """
    # Champ afin d'enregistrer le nom du référent client.
    lastname = StringField(
        "Nom du client référent",
        validators=[DataRequired()],
        render_kw={"placeholder": "Nom du client"}
    )
    
    # Champ afin d'enregistrer le nom du référent client.
    firstname = StringField(
        "Prénom du client référent",
        validators=[DataRequired()],
        render_kw={"placeholder": "Prénom du client"}
    )
    
    # Champ pour le nom de l'entreprise.
    enterprise_name = StringField(
        "Nom de l'entreprise",
        validators=[DataRequired(), Length(min=2, max=30)],
        render_kw={"placeholder": "Nom entreprise"}
    )
    
    # Champ pour le rôle de l'utilisateur.
    role = StringField(
        "rôle utilisateur",
        validators=[DataRequired()],
        render_kw={"placeholder": "Rôle"}
    )
    
    # Téléphone du référent.
    phone = TelField(
        "Téléphone du client",
        validators=[DataRequired()],
        render_kw={"placeholder": "Téléphone du client"}
    )
    
    # Champ pour l'email du référent projet.
    email = EmailField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email du référent projet."}
    )
    
    # Champ pour le mot de passe.
    password = PasswordField(
        "Mot de passe",
        validators=[DataRequired()],
        render_kw={"placeholder": "Mot de passe utilisateur"}
    )
    
    # Champ pour la vérification du mot de passe.
    password2 = PasswordField(
        "Confirmez le mot de passe",
        validators=[DataRequired(), EqualTo("password", message="Les deux mots de passe doivent correspondre.")],
        render_kw={"placeholder": "Confirmer mot de passe."}
    )
    
    # Champ pour le logo de l'entreprise.
    profil_photo = FileField(
        "Logo de l'entreprise.",
        validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], "Images seulement !!")]
    )
    
    # Bouton de soumission du formulaire.
    submit = SubmitField(
        "Souscrire aux conditions générales du site."
    )
    
    # Token de sécurité.
    csrf_token = HiddenField()
    
    
    # Fonction vérifiant la bonne création du formulaire.
    # Fonction qui vérifie que le nom de l'entreprise n'existe pas déjà dans la base de données.
    def validate_enterprise_name(self, enterprise_name):
        """
        Valide le nom de l'entreprise choisi s'il n'existe pas déjà dans la bae de données.
        
        Args:
            enterprise_name (StringField): Nom de l'entreprise à vérifier.
            
        Raise:
            ValidationError: Si le nom de l'entreprise client.
        """
        
        user = User.query.filter_by(enterprise_name=enterprise_name.data).first()
        if user is not None:
            raise ValidationError("Cette entreprise est déjà enregistrée.")
        
    # Fonction qui vérifie que l'email enregistré n'est pas déjà utilisé.
    def validate_email(self, email):
        """
        Valide l'email choisi.
        
        Args:
            email (EmailField): Email enregistré.
        
        Raise:
            ValidationError: Si l'email est déjà utilisé.
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Cet email est déjà utilisé, Veuillez vérifier vos données.")
        
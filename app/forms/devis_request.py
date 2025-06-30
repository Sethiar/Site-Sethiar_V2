"""
Code renvoyant le code du formulaire de la demande de devis.
"""

#-------------------------------------------------------#
# Formulaire de demande de devis + Vérification Devis.  #
#-------------------------------------------------------# 



from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, TelField, EmailField, \
    SubmitField, HiddenField, SelectMultipleField, widgets

from wtforms.validators import DataRequired, Email, Length, ValidationError, Regexp


# Formulaire de demande de devis.
class DevisRequestForm(FlaskForm):
    """
    Formulaire permettant de demander un devis.

    Attributes:
        request_content_devis (TextAreaField): Champ renseignant la nature du projet.
        nom (StringField): Champ renseignant le nom du client.
        prenom (StringField): Champ renseignant le prénom du client.
        telephone (TelField): Champ renseignant le numéro de téléphone.
        email (EmailField): Champ renseignant l'email.
        submit (SubmitField): Bouton pour soumettre le formulaire.
        csrf_token (HiddenField) : Champ caché pour la protection CSRF.

    Example :
        form= DevisRequestForm()
    """

    # Nom et prénom du client.
    lastname = StringField(
        "Nom",
        validators=[DataRequired(), Length(max=30)],
        render_kw={"placeholder": "Nom"}
    )
    
    firstname = StringField(
        "Prénom",
        validators=[DataRequired(), Length(max=30)],
        render_kw={"placeholder": "Prénom"}
    )

    # Téléphone du client.
    phone = TelField(
        "Téléphone",
        validators=[
            DataRequired(),
            Regexp(r'^\+?[0-9\s\-]{7,20}$', message="Numéro de téléphone invalide")
            ],
        render_kw={"placeholder": "Numéro de téléphone"}
    )
    
    # Nom de  l'entreprise. Par défault, il s'agit d'un particulier.
    enterprise_name = StringField(
        "Nom de l'entreprise",
        validators=[DataRequired()],
        render_kw={"placeholder": "Nom de votre entreprise"})
    
    # Email du client.
    email = EmailField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"}
    )

    # Type de projet.
    project_type = SelectMultipleField(
        "Type de projet",
        choices=[
            ("web", "Développement Web"),
            ("mobile", "Développement Mobile"),
            ("design", "Conception Graphique"),
            ("autre", "Autre")
        ],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False),
        render_kw={"class": "checkbox-group"}
    )

    # Le contenu de la demande de devis.
    devis_content = TextAreaField(
        "Description du projet",
        validators=[DataRequired(), Length(min=10, message="Veuillez fournir au moins 10 caractères")],
        render_kw={"placeholder": "Décrivez en quelques mots votre projet (fonctionnalités, objectifs, etc.)"}
    )

    # Bouton de soumission.
    submit = SubmitField("Soumettre le devis")

    # Token de sécurité.
    csrf_token = HiddenField()
    
    
    
    #--------------------------------------------------------------------------
    # Fonction realtive à la vérification du devis.
    #--------------------------------------------------------------------------
    
    # fonction vérifiant la validité de la soumission du formulaire.
    def validate_project_type(form, field):
        if not field.data or len(field.data) < 1:
            raise ValidationError("Veuillez sélectionner au moins un type de projet")
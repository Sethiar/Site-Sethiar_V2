"""
Code traitant les informations de demande de chat vidéo avec les employés de SethiarWorks.
"""
 
#-----------------------------------------------------------------------------------#
# Formulaire de demande de chat vidéo + formulaire pour envoyer le lien de la visio #
#-----------------------------------------------------------------------------------# 

from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, DateField, SubmitField, FileField, \
    TimeField, HiddenField

from wtforms.validators import DataRequired


# Formulaire traitant la demande de chat vidéo.
class ChatRequestForm(FlaskForm):
    """
    Formulaire permettant de demander un chat vidéo à l'administrateur.
    
    Attributes:
        enterprise_name(StringField): Champ pour le nom de l'entreprise.
        email(StringField): Champ pour l'email de l'utilisateur demandeur du chat.
        request_content (TextAreaField): Champ pour le contenu de la demande.
        date_rdv (DateField): Champ pour sélectionner la date du chat vidéo.
        heure (TimeField): Champ pour indiquer l'heure du chat vidéo.
        submit (SubmitField): Champ pour la soumission du formulaire.
        csrf_token (HidenField): Champ du jeton csrf pour la sécurité des formulaires.
    """
    
    # Nom de l'entreprise / Défault= particulier.
    enterprise_name = StringField(
        "Nom de l'entreprise",
        validators=[DataRequired()],
        render_kw={"placeholder": "Veuillez renseigner le nom entreprise"}
        )
    
    email = StringField(
        "Email",
        validators=[DataRequired()],
        render_kw={"placeholder": "Veuillez renseigner votre email"}    
    )
    
    # Contenu de la demande.
    request_content = TextAreaField(
        "Contenu de la demande",
        validators=[DataRequired()],
        render_kw={"placeholder": "Veuillez préciser le motif de votre demande pour le chat vidéo"}
    )
    
    # La date envisagée pour le chat vidéo.
    date_rdv = DateField(
        "Veuillez sélectionner la date souhaitée",
        validators=[DataRequired()],
        render_kw={"placeholder": "Date souhaitée de rendez-vous :"}
    )
    
    # Heure souhaitée.
    heure = TimeField(
        "Heure souhaitée",
        validators=[DataRequired()],
        render_kw={"placeholder": "12:00"}
    )
    
    # Action de soumettre le formulaire.
    submit = SubmitField("Soumettre la demande")
    
    # Token de sécurité.
    csrf_token = HiddenField()
    
    
# Formulaire permettant d'envoyer le lien pour la session de chat vidéo à l'utilisateur.
class UserLink(FlaskForm):
    """
    Formulaire pour envoyer le lien à  l'utilisateur.
    """
        
    # Réception du lien pour le chat à envoyer le lien pour la session fde chat à l'utilisateur.
    chat_link = StringField(
        "Chat-link",
        validators=[DataRequired()],
        render_kw={"placeholder": "Veuillez renseigner le lien copié"}
    )
        
    # Action de soumettre le formulaire.
    submit = SubmitField("Soumettre la demande")
    
    # Token de sécurité.
    csrf_token = HiddenField()
    
    
"""
Code permettant de définir les routes concernant les fonctions de mailing du site de l'entreprise de SethiarWorks.
"""

from app.mail import mail_bp
from flask_mail import Message

from flask import current_app, redirect, url_for, flash

from app.Models.user import User

from dotenv import load_dotenv

load_dotenv()


# Fonction qui envoie un mail à l'utilisateur afin de l'avertir du succès de son inscription.
@mail_bp.route('envoi-pour-confirmer-inscription/<string:email>')
def send_confirmation_email_user(email):
    """
    Fonction qui envoie un mail automatique de confirmation d'inscription au site de l'entreprise SethiarWorks.

    :param email: Email de l'utilisateur nouvellement inscrit.
    :return:
    """
    user = User.query.filter_by(email=email).first()
    if not user:
        flash("Utilisateur non trouvé.", "Attention")
        return redirect(url_for('landing_page'))

    # Corps du message.
    msg = Message(
        "Confirmation d'inscription",
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[email]
    )
    msg.body = f"""
    
            Bonjour M. / Mme {user.lastname},
            
            Merci de votre confiance quant à la validation de notre cahier des charges.
            
            Comme indiqué sur ce dernier, nous vous avons inscrit sur le site de notre entreprise afin que vous puissiez,
            si vous le désirez, laisser un commentaire sur le projet que nous avons mené à son terme.
            
            Nous espérons que vous avez été satisfait de notre travail et que vous avez apprécié notre collaboration.
            
            Votre inscription a été confirmée avec succès.
            
            Vos identifiants sont inscrits dans le cahier des charges que nous vous avons donné, en annexe.
            
            Nous espérons que nous vous retrouverons bientôt.
            
            Nous vous souhaitons une bonne continuation.
            
            
            Cordialement,
            L'équipe de SethiarWorks.
            """

    current_app.extensions['mail'].send(msg)
    return redirect(url_for('admin.backend'))


# Fonction qui envoie un mail à l'administrateur afin de l'avertir d'une nouvelle inscription.
@mail_bp.route('envoi-pour-confirmer-inscription/')
def send_confirmation_email_admin():
    """
    Fonction qui envoie un mail à l'administrateur afin de l'avertir
    d'une nouvelle inscription au site de l'entreprise SethiarWorks.

    :param email: Email de l'utilisateur nouvellement inscrit.
    """

    # Corps du message.
    msg = Message(
        "Confirmation d'inscription",
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[current_app.config['MAIL_DEFAULT_SENDER']] 
    )
    msg.body = f"""
            Bonjour Sethiar
            Youpi !!! Une nouvelle inscription sur le site de l'entreprise SethiarWorks.
            
            
            Cordialement,
            L'équipe de SethiarWorks.
            """
    current_app.extensions['mail'].send(msg)



# Méthode qui envoie le lien permettant de faire le changement du mot de passe.
def reset_password_mail(email, reset_url):
    """
    Envoie un mail afin de cliquer sur un lien permettant la réinitialisation du mot de passe.
    Si l'utilisateur n'est pas à l'origine de cette action, le mail inclut un lien d'alerte pour l'administrateur.

    :param reset_url: URL pour réinitialiser le mot de passe
    :param email: Adresse email du destinataire
    :return: None
    """
    user = User.query.filter_by(email=email).first()
    if not user:
        flash("Utilisateur non trouvé.", "attention")
        return redirect(url_for('landing_page'))
    msg = Message(
        "Réinitialisation de votre mot de passe",
        sender='noreply@yourapp.com',
        recipients=[email]
    )
    msg.body = f"""
            Bonjour M. / Mme {user.lastname},
            
            pour réinitialiser votre mot de passe, cliquez sur le lien suivant : {reset_url}
            
            
            Cordialement,
            L'équipe de SethiarWorks.
            """
    current_app.extensions['mail'].send(msg)


# Méthode qui envoie un mail assurant le succès de la réinitialisation du mail.
def password_reset_success_email(user):
    """
    Envoie un e-mail de confirmation de réinitialisation de mot de passe à l'utilisateur.

    :param user: Informations de l'utilisateur qui renouvelle ce mail.
    """
    msg = Message(
        "Confirmation de réinitialisation de mot de passe",
        sender='noreply@yourapp.com',
        recipients=[user.email]
    )
    msg.body = f"""
               
            Bonjour M. / Mme {user.lastname},
               
            Votre mot de passe a été réinitialisé avec succès.
               
               
            Cordialement,
            L'équipe de SethiarWorks.
            """
    current_app.extensions['mail'].send(msg)


# Méthode qui permet d'envoyer un mail à un utilisateur si quelqu'un a
# répondu à son commentaire dans la section commentaire.
def mail_reply_comment(email, subject):
    """
    Envoie un mail à l'auteur du commentaire en cas de réponse à celui-ci.
    :param email: email de l'utilisateur qui a commenté le sujet du forum.
    :param subject_nom : nom du sujet du forum commenté.
    """
    user = User.query.filter_by(email=email).first()

    msg = Message(
        "Quelqu'un a répondu à votre commentaire de la section forum.",
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[user.email]
    )
    msg.body = f"""
               
            Bonjour M. / Mme {user.lastname},
            Un utilisateur a répondu à votre commentaire de la section commentaire du site SethiarWorks dont le sujet est : \"{subject.name}\".
            
            Nous vous invitons à vous connecter à votre compte afin de lire la réponse.
            
            
            Cordialement,
            L'équipe de SethiarWorks.
            """
    current_app.extensions['mail'].send(msg)


# Méthode envoyant un mail de confirmation de la demande de chat vidéo à l'utilisateur.
def send_confirmation_request_reception(email, enterprise_name):
    """
    Fonction qui envoie un mail de confirmation à l'utilisateur de la bonne réception de sa requête de chat vidéo.

    :param request : Informations de l'utilisateur enregistrées dans ChatRequest.
    :return:
    """
    msg = Message(
        "Confirmation de la demande de chat vidéo.",
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[email]
    )
    msg.body = f"""
    
            Bonjour,
            
            Vous avez sollicité une demande de chat pour l'entreprise : {enterprise_name}.
               
            Nous accusons bonne réception de votre demande.
            Nous vous répondrons dans les plus brefs délais afin de valider votre rendez-vous.
               
               
            Cordialement,
            L'équipe de SethiarWorks.
            """
    current_app.extensions['mail'].send(msg)


# Méthode envoyant un mail à l'administrateur du site s'il y a une demande de chat vidéo.
def send_request_admin(enterprise_name, request_content):
    """
    Fonction qui envoie un mail pour informer l'administration d'une requête de chat vidéo.

    :param request : Informations de l'utilisateur enregistrées dans ChatRequest.
    :param request_content : contenu de la requête de l'utilisateur.
    """
    msg = Message(
        "Demande de chat vidéo.",
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[current_app.config['MAIL_DEFAULT_SENDER']]
    )
    msg.body = f"""
               
            Bonjour Sethiar,
               
            l'entreprise {enterprise_name} souhaite avoir un chat vidéo avec vous.
            Voici sa requête :
            {request_content}
               
               
            Bon courage Mec.
            """
    current_app.extensions['mail'].send(msg)
    

# Fonction envoyant un mail à l'utilisateur en générant le lien de connexion au chat vidéo.
def send_mail_validate_request(chat, chat_link):
    """
    Fonction qui envoie un mail pour informer de la validation de la requête par l'administrateur.
    
    :param request: Informations de l'utilisateur enregistrées dans ChatRequest.
    :param chat_link: lien du chat vidéo.
    :return:
    """

    msg = Message(
        "Validation de la requête de chat vidéo.",
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[chat.email]
    )
    msg.body = f"""
    
            Bonjour {chat.enterprise_name}.
               
            L'équipe de SethiarWorks a accepté votre requête de chat vidéo.
            Le rendez-vous est prévu le {chat.date_rdv} à {chat.heure}.
               
            Voici le lien de connexion: {chat_link}
            Nous vous demandons de cliquer sur ce lien quelques minutes
            avant le rendez-vous afin d'être prêt pour le chat vidéo.
               
               
            Cordialement,
            L'équipe de SethiarWorks.
            """
    current_app.extensions['mail'].send(msg)


# Méthode qui envoie un mail de refus de la requête de chat vidéo.
def send_mail_refusal_request(chat):
    """
    Fonction qui envoie un mail pour informer du refus de la requête par l'administrateur.

    :param request: Informations de l'utilisateur qui a envoyé la demande de chat.
    """
    msg = Message(
        "Refus de la requête de chat vidéo.",
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[chat.email]
    )
    msg.body = f"""
            
            Bonjour {chat.enterprise_name},
            
            L'équipe de SethiarWorks est dans l'impossibilité de valider votre rendez-vous.
            Afin de renouveler votre demande, nous vous prions de bien vouloir
            refaire une demande de chat vidéo, ou de bien vouloir nous contacter à cette adresse : 
            
            sethiarworks@gmail.com
            
            Nous pourrons alors convenir d'un rendez-vous de manière plus précise.
            
            
            Cordialement,
            L'équipe de SethiarWorks.
            """
            
    current_app.extensions['mail'].send(msg)


# Méthode qui envoie un mail assurant que la demande a bien été reçue par l'équipe.
def send_mail_validate_demand(devis):
    """
    Fonction qui envoie un mail pour informer de la bonne réception de la demande de devis par l'administrateur.

    :param devis: Informations enregistrées dans la table DevisRequest.
    """
    msg = Message(
        "Nous accusons bonne réception de votre demande de devis.",
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[devis.email]
    )
    msg.body = f"""
               
            Bonjour M. / Mme {devis.lastname},
               
            Nous avons bien reçu votre demande de devis et nous y répondrons sous une semaine.
               
            Afin de mieux cerner votre besoin, je vous proposerai, - une fois le devis validé -
            un entretien téléphonique qui permettra de cerner plus concrètement votre projet.
               
            À l'issue de notre échange, je serai alors apte à vous transmettre le temps nécessaire
            à la réalisation de votre projet, ainsi que le budget qu'il nécessitera.
               
            Vous disposerez alors d'une période de réflexion pour me donner votre réponse. 
            
            Dans le cas où notre partenariat vous intéresserait, nous commencerons, dès votre accord, 
            la rédaction du cahier des charges de votre projet et vous recevrez notre contrat dans les trois jours suivant la validation.
               
               
            Entreprise : {devis.enterprise_name}
            Nom : {devis.lastname}
            Prénom : {devis.firstname}
            Email : {devis.email}
            Téléphone : {devis.phone}
            Type de projet : {', ' .join(devis.project_type)}
            Contenu :
                {devis.devis_content}
               
               
            Cordialement,
            L'équipe de SethiarWorks. 
            """
    current_app.extensions['mail'].send(msg)


# Méthode qui envoie un mail à l'administrateur l'informant d'une demande de devis.
def send_mail_inform_demand():
    """
    Fonction qui envoie un mail à l'administrateur pour informer de la
    bonne réception de la demande de devis.
    """
    msg = Message(
        "Sethiar, tu as un devis.",
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=['sethiarworks@gmail.com']
    )
    msg.body = f"""
            Salut Sethiar,
               
            Nous avons reçu une demande de devis.
               
            Veuillez vous connecter à votre backend afin de vous informer de la demande de devis.
               
               
            Cordialement,
            L'équipe de SethiarWorks.
               
            """
    current_app.extensions['mail'].send(msg)


# Fonction envoyant un mail validant la demande de devis.
def mail_reply_devis_validate(devis):
    """
    Fonction qui envoie un mail pour informer de la validation de la demande de devis par l'administrateur.

    :param devis : Informations enregistrées dans la table DevisRequest.
    """
    msg = Message(
        "Validation de votre devis.",
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[devis.email]
    )
    msg.body = f"""
            Bonjour M. / Mme {devis.lastname},
        
            Nous avons bien reçu votre demande de devis et nous y répondons favorablement.
            Afin de pouvoir nous entretenir de manière plus efficace,
            Nous vous contacterons sous trois jours afin de fixer un entretien téléphonique avec vous.
        
        
            Cordialement,
            L'équipe de SethiarWorks.
            """
    current_app.extensions['mail'].send(msg)


# Fonction envoyant un mail refusant la demande de devis.
def mail_reply_devis_reject(devis):
    """
    Fonction qui envoie un mail pour informer du refus de la demande de devis par l'administrateur.

    :param devis : Informations enregistrées dans la table DevisRequest.
    """
    msg = Message(
        "Refus de votre devis.",
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[devis.email]
    )
    msg.body = f"""
            Bonjour M. / Mme {devis.lastname},
            
            Nous avons bien reçu votre demande de devis mais nous ne pouvons pas y répondre favorablement
            pour le moment.
            
            Nous vous remercions pour votre offre ainsi que pour votre confiance.
            
            Nous vous prions de nous excuser pour la gêne occasionnée et nous vous envoyons
            la meilleure énergie possible afin que votre projet aboutisse.
            
            N'hésitez à nous recontacter si vous aviez un quelconque besoin dans les mois à venir.
            
            
            Cordialement,
            L'équipe de SethiarWorks.
            """
    current_app.extensions['mail'].send(msg)
    
    
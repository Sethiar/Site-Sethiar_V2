"""
Code permettant d'envoyer des mails de manière asynchrone en arrière-plan.
"""
from threading import Thread

# Déclaration de la fonction d'envoi asynchrone.
def sed_async_email(app, msg):
    """
    Envoie le mail de manière asynchrone en utilisant le contexte de l'application.
    
    Args: 
        app (Flask): L'instance de l'applicaiton FLask.
        msg (Message): L'objet Message contenant les détails de l'email à envoyer. 
    """
    with app.app_context():
        app.extensions['mail'].send(msg)
        
        
# Déclaraton de la fonction d'envoi en arrière-plan.
def send_email_in_background(app, msg):
    """
    Lance l'envoi de l'email dans un thread séparé.
    
    Args:
        app (Flask): L'instnace de l'application Flask.
        msg (Message): L'objet Message contenant les détails de l'email à envoyer.
    """
    Thread(target=sed_async_email, args=(app, msg)).start()
"""
Fichier de configuration de l'application Flask.
"""

import os
import logging

from datetime import datetime
from config.config import Config
from markupsafe import Markup

from dotenv import load_dotenv

from itsdangerous import URLSafeTimedSerializer

from flask import Flask, request, redirect, url_for, session, g

from uuid import uuid4

from flask_migrate import Migrate
from flask_login import current_user
from flask_assets import Bundle

from app.Models import db
from app.Models import shutdown_session


from .extensions import mailing, csrf, login_manager, moment, assets

# Importation des modèles nécessaires.
from app.Models.admin import Admin

from app.Models.user import User

from app.Models.anonyme import AnonymousUser

from app.Models.chat_request import ChatRequest
from app.Models.devis_request import DevisRequest

from app.Models.subject import Subject

from app.Models.comment import Comment

from app.Models.reply_comment import ReplyComment
from app.Models.reply_anonymous_comment import ReplyAnonymousComment
from app.Models.reply_anonymous_user_comment import ReplyAnonymousUserComment
from app.Models.reply_user_anonyme_comment import ReplyUserAnonymousComment



# Chargement des variables d'environnement depuis le fichier .env.
load_dotenv()


#----------------------------------------------------
# Création de l'instance de l'application Flask.
#----------------------------------------------------

def create_app(config_class=Config):
    """
    Fonction de création de l'application Flask.
    
    Cette fonction configure l'application Flask en chargeant les paramètres de configuration,
    en initialisant les extensions et en définissant les routes.
    """
    
    
    #------------------------------------------------------
    # Instanciation de l'application Flask.
    #------------------------------------------------------
    
    # Le nom de l'application est défini comme "SethiarWorks".
    app = Flask("SethiarWorks")
    
    
    #-------------------------------------------------------
    # Configuration des blueprints.
    #-------------------------------------------------------
    
    # Enregistrement du blueprint pour les routes administrateur.
    from app.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Enregistrement du blueprint pour les routes d'authentification.
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Enregistement du blueprint pour les routes chat.
    from app.chat import chat_bp
    app.register_blueprint(chat_bp, url_prefix='/chat')
    
    # Enregistrement du blueprint pour les routes utilisateur.
    from app.user import user_bp
    app.register_blueprint(user_bp, url_prefix='/user')
    
    # Enregistrement du blueprint pour les routes de devis.
    from app.devis import devis_bp
    app.register_blueprint(devis_bp, url_prefix='/devis')
    
    # Enregistrement du blueprint pour les routes des focntionnalités basiques.
    from app.functional import functional_bp
    app.register_blueprint(functional_bp, url_prefix='/functional')
    
    # Enregistrement du blueprint pour les routes du frontend.
    from app.frontend import frontend_bp
    app.register_blueprint(frontend_bp, url_prefix='/frontend')
    
    # Enregistrement du blueprint pour les routes de mail.
    from app.mail import mail_bp
    app.register_blueprint(mail_bp, url_prefix='/mail')
    
    # Propagation des erreurs aux gestionnaires d'erreurs des Blueprints.
    app.config['PROPAGATE_EXCEPTIONS'] = True
    #------------------------------------------------------
    
    
    #------------------------------------------------------
    # Configuration du mailing
    #------------------------------------------------------
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    
    mailing.init_app(app)    
    #------------------------------------------------------
    
    
    #------------------------------------------------------
    # Configuration de Flask-Assets.
    #------------------------------------------------------
    
    # Configuration des bundles pour Flask-Assets.
    assets.init_app(app)
    css_bundle = Bundle('SCSS/style.scss', filters='scss', output='gen/style.css')
    assets.register('css_all', css_bundle)
    
    # Rattachement de Flask-Assets à l'instance Flask.
    app.assets = assets
    
    # Empêcher le cache durant le dévelopement.
    app.config['ASSETS_DEBUG'] = True
    
    # Forcer la compilation manuelle.
    with app.app_context():
        css_bundle.build()
    
    #------------------------------------------------------
    
    
    #------------------------------------------------------
    # Chargement de la configuration de l'environnement.
    #------------------------------------------------------
    
    # Configuration de l'environnement de l'application Flask.
    app.config.from_object(Config)
    
    # Chargement de la configuration spécifique en fonction de l'environnement.
    if os.environ.get('FLASK_ENV') == 'development':
        app.config.from_object('config.config.DevelopmentConfig')
    elif os.environ.get('FLASK_ENV') == 'testing':
        app.config.from_object('config.config.TestingConfig')
    else:
        app.config.from_object('config.config.Config')
    
    # Configuration des cookies des sessions.
    env = os.environ.get("FLASK_ENV", "production") #Default: 'production'.
    app.config['SESSION_COOKIE_SECURE'] = True if env == 'production' else False
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = 60 * 60 * 24 * 7  # 7 jours
    #-------------------------------------------------------
    
    
    #------------------------------------------------------
    # Déclaration des données secrètes.
    #------------------------------------------------------

    # Configuration de la clé secrète pour les sessions.
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    # Configuration du sérialiseur pour les tokens de sécurité.
    app.config['SECURITY_TOKEN_SERIALIZER'] = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT')

    #-------------------------------------------------------
    
    
    #===============================================#
    # Enregistrent du hook de fermeture de session  #
    #===============================================#
    
    # Enregistrement du hook de fermeture de session pour la base de données.
    app.teardown_appcontext(shutdown_session)
    #-------------------------------------------------------
    
    
    #==================================#   
    #  Configuration de Flask-Migrate  #
    #==================================#
    
    # Initialisation de Flask-Migrate pour la gestion des migrations de la base de données.
    db.init_app(app)
    
    # Instanciation de Flask-Migrate.
    Migrate(app, db)
    
    # Configuration de Moment.
    moment.init_app(app)
    # Définition de la locale pour Moment.js
    moment.locale = 'fr'
    moment.include_moment = lambda: Markup(
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.1/moment.min.js"></script>'
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.1/locale/fr.js"></script>'
    )
    #--------------------------------------------------------
    
    
    #=================================#
    #  Configuration de Flask-Login   #
    #=================================#
    
    # Configuration de la protection CSRF.
    csrf.init_app(app)
    
    # Configuration de LoginManager.
    login_manager.init_app(app)
    # Message de connexion
    login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."  
    # Catégorie du message de connexion
    login_manager.login_message_category = "info"  
    # Protection de session
    login_manager.session_protection = 'strong'  
    # Gestion des utilisateurs anonymes.
    login_manager.anonymous_user = AnonymousUser
    # Vue de rafraîchissement de la session
    login_manager.refresh_view = 'auth.user_connection'  
    # Message
    login_manager.needs_refresh_message = "Veuillez vous reconnecter pour continuer."  
    # Catégorie du message de rafraîchissement
    login_manager.needs_refresh_message_category = "warning" 
    # Redirection vers la page de connexion
    login_manager.login_view = 'auth.login'  
    #--------------------------------------------------------
    
    
    #==========================================#
    # Fonction de chargement de l'utilisateur  #
    #==========================================#

    # Fonction exécutée avant chaque requête pour charger l'utilisateur connecté.
    @app.before_request
    def load_globals():
        """
       Fonction exécutée avant chaque requête pour charger l'utilisateur connecté.
       Elle stocke l'objet utilisateur courant dans `g.user` et, s'il s'agit d'un administrateur, dans `g.admin`.
       """
    
        # Chargement de l'utilisateur connecté dans l'objet global g.
        g.user = current_user if current_user.is_authenticated else None
        
        # Si l'utilisateur n'est pas authentifié, (utilisateur anonyme),
        if not g.user:
            # On crée un utilisateur anonyme.
            if 'anonymous_id' not in session:
                # Génération d'un identifiant unique pour l'utilisateur anonyme.
                session['anonymous_id'] = str(uuid4())
            g.user = AnonymousUser()
            
        # Utilisateur et / ou administrateur.
        if g.user and isinstance(g.user, Admin):
            g.admin = g.user
        else:
            g.admin = None


    @login_manager.user_loader
    def load_user(user_id):
        """
        Fonction de chargement de l'utilisateur pour Flask-Login.
        
        Cette fonction est appelée par Flask-Login pour charger un utilisateur à partir de son ID.
        
        param user_id: L'ID de l'utilisateur à charger.
        return: L'objet utilisateur correspondant à l'ID, 
        None si l'utilisateur n'existe pas 
        ou admin si l'utilisateur est un administrateur.
        """

        # Retourne un User ou un Admin si trouvé.
        user = User.query.get(user_id) or Admin.query.get(user_id)
        
        if not user:
            # Si l'utilisateur n'est pas trouvé, on crée un utilisateur anonyme.
            user = AnonymousUser(user_id)
        
        return user
    #--------------------------------------------------------
    
    
    #=========================================#
    #    Gestion des utilisateurs anonymes    #
    #=========================================#
   
    @login_manager.unauthorized_handler
    def unauthorized():
        """
        Gestionnaire de redirection pour les utilisateurs non autorisés.
        
        Cette fonction est appelée lorsque l'utilisateur n'est pas connecté et tente d'accéder à une page protégée.
        Elle redirige l'utilisateur vers la page de connexion.
        
        return: Redirection vers la page de connexion ou pessage personnalisé pour les anonymes.
        """
        # Si l'utilisateur est anonyme et essaie d'accéder à une page protégée,
        if g.user and isinstance(g.user, AnonymousUser):
            return redirect(url_for('landing_page'))
        
        # Vérification de l'appel de la fonction depuis une requête AJAX.
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Si c'est une requête AJAX, renvoie un code d'état 401 (Non autorisé).
            return {'error': 'Unauthorized'}, 401
        
        # Si ce n'est pas une requête AJAX, redirige vers la page de connexion.
        session['next'] = request.url
        return redirect(url_for('auth.user_connection', next=request.url))
    #--------------------------------------------------------
    
    
    #==========================================================#
    # Injection des modèles dans le contexte de l'application  #  
    #==========================================================#
    
    @app.context_processor
    def inject_logged_in():
        """
        Injecte l'utilisateur connecté (`user`) et l'administrateur (`admin`) dans le contexte des templates.
        """
        # Cette fonction est appelée avant le rendu de chaque template.
        return {
        'logged_in': g.user.is_authenticated if getattr(g, 'user', None) else False,
        'user': getattr(g, 'user', None),
        'admin': getattr(g, 'admin', None)
    }
    #-------------------------------------------------------
    
    
    #=========================================#
    #    Configuration de la journalisation   #
    #=========================================#
    
    # Configuration du niveau de journalisation.
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    handler = logging.FileHandler("fichier.log")
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.info(f"Application {app.name} démarrée à {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    #-------------------------------------------------------
    
        
    return app

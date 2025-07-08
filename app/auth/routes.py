"""
Code permettant de définir les routes concernant les fonctions d'authentification du site
"""
import bcrypt

from app.auth import auth_bp

from app.forms.admin_login import AdminConnection
from app.forms.user_login import UserConnection
from app.forms.form_password import ForgetPassword, RenamePassword

from flask import render_template, redirect, url_for, session, request, current_app, flash

from app.Models import db

from app.Models.user import User
from app.Models.admin import Admin

from flask_login import logout_user, login_user

from app.mail.routes import reset_password_mail, password_reset_success_email


# Route permettant à l'utilisateur de joindre le formulaire de connexion.
@auth_bp.route("/connexion-utilisateur-formulaire", methods=['GET', 'POST'])
def user_connection():
    """
    Permet à l'utilisateur d'accéder au formulaire de connexion afin de s'identifier.

    Returns:
        Template HTML du formulaire d'authentification utilisateur.

    Description:
        La fonction récupère l'URL de la page précédente via `request.referrer` et la stocke dans la session pour une
        redirection après connexion réussie. Elle crée une instance du formulaire `UserConnection` et
        rend le template `User/user_connection.html` avec le formulaire et l'URL de redirection.

    Example:
        Lorsqu'un utilisateur accède à cette route, il voit le formulaire de connexion. Après avoir entré ses
        identifiants et soumis le formulaire, il est soit redirigé vers la page précédente, soit vers la page d'accueil
        en fonction de l'état de la connexion.
    """
    # Récupération de l'URL de redirection depuis le paramètre `next` ou via le référent.
    next_url = request.args.get('next') or request.referrer
    # Stockage de l'URL de redirection dans la session pour une redirection après connexion.
    session['next_url'] = next_url

    # Instanciation du formulaire.
    form_loginuser = UserConnection()
    return render_template("user/user_login.html", form_loginuser=form_loginuser, next_url=next_url)


# Route permettant à un utilisateur de se connecter au site de l'entreprise.
@auth_bp.route('/connexion-utilisateur', methods=['GET', 'POST'])
def login():
    """
    Gère l'authentification de l'utilisateur.

    Cette fonction valide les informations de connexion de l'utilisateur et l'authentifie s'il réussit.

    Returns:
        Redirige l'utilisateur vers la page précédente ou la page d'accueil après une connexion réussie.

    Description:
        Cette route gère le processus d'authentification de l'utilisateur via le formulaire
        d'authentification 'UserConnection'. Si les informations de connexion sont valides,
        l'utilisateur est authentifié et ses informations sont stockées dans la session Flask.
        Ensuite, il est redirigé vers la page précédente s'il existe, sinon vers la page d'accueil.
        En cas d'échec d'authentification, l'utilisateur est redirigé vers la page de connexion avec un message d'erreur.
    """

    # Récupère next_url depuis la session Flask
    next_url = session.get('next_url')

    # Création de l'instance du formulaire.
    form_loginuser = UserConnection()

    if request.method == 'POST' and form_loginuser.validate_on_submit():
        enterprise_name = form_loginuser.enterprise_name.data
        password = form_loginuser.password.data

        # Recherche de l'utilisateur dans la base de données en fonction du pseudo.
        user = User.query.filter_by(enterprise_name=enterprise_name).first()

        if user is None:
            # Le nom de l'entreprise est incorrect.
            current_app.logger.warning(f"Tentative de connexion échouée : nom de l'entreprise inconnu.")
            flash("Le nom de l'entreprise ou mot de passe incorrect.", "login")
        elif not bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
            # Le mot de passe est incorrect.
            current_app.logger.warning(f"Tentative de connexion échouée pour {enterprise_name} : mot de passe incorrect.")
            flash("Le nom de l'entreprise ou le mot de passe est incorrect.", "login")
       
        else:
            # Authentification réussie.
            login_user(user)
            session["logged_in"] = True
            session["nom de l'entreprise"] = user.enterprise_name
            session["user_id"] = user.id
            current_app.logger.info(f"L'utilisateur {user.enterprise_name} s'est bien connecté.")

            # Redirection vers l'URL précédente ou la page d'accueil.
            return redirect(next_url or url_for('landing_page'))

    flash("Votre authentification a échoué, veuillez recommencer la saisie de vos identifiants.", "error")
    return render_template("user/user_login.html", form_loginuser=form_loginuser)


# Route permettant à un utilisateur de se déconnecter du site de l'entreprise.
@auth_bp.route("/deconnexion-utilisateur")
def user_logout():
    """
    Déconnecte l'utilisateur actuellement authentifié.

    Cette fonction supprime les informations d'identification de l'utilisateur de la session Flask.

    Returns:
        Redirige l'utilisateur vers la page d'accueil après la déconnexion.
    """
    # Supprime les informations d'identification de l'administrateur de la session.
    session.pop("logged_in", None)
    session.pop("identifiant", None)
    session.pop("user_id", None)
    session.pop("Nom de l'entreprise", None)
    # Fonction de déconnexion.
    logout_user()

    # Redirige vers la page d'accueil après la déconnexion.
    return redirect(url_for('landing_page'))


# Route permettant à l'administrateur de joindre le formulaire de connexion.
@auth_bp.route('formulaire-connexion-administrateur', methods=['GET', 'POST'])
def admin_connection():
    """
    Route permettant d'accéder au formulaire de connexion pour l'administrateur.

    Returns:
        Template HTML du formulaire de connexion administrateur.

    Description:
        Cette route affiche un formulaire de connexion spécifiquement conçu pour l'administrateur
        du système.
    """
    # Création de l'instance du formulaire.
    form_admin = AdminConnection()

    return render_template("admin/admin_login.html", form_admin=form_admin)


# Route permettant à un administrateur de se connecter au site de l'entreprise.
@auth_bp.route('/connexion-administrateur', methods=['GET', 'POST'])
def login_admin():
    """
    Gère l'authentification de l'administrateur pour accéder au back-end du blog.

    Cette route affiche un formulaire de connexion pour les administrateurs et traite les soumissions.
    Elle vérifie les informations d'identification et établit une session si l'authentification est réussie.

    :return: La page de connexion pour les administrateurs, ou une redirection en fonction
    du succès de l'authentification.
    """
    # Instanciation du formulaire de connexion.
    form_admin = AdminConnection()

    # Vérification si la méthode de la requête est POST, indiquant la soumission du formulaire.
    if request.method == 'POST' and form_admin.validate_on_submit():
        # Récupération des données soumises dans le formulaire.
        pseudo = form_admin.pseudo.data
        password = form_admin.password.data
        role = form_admin.role.data

        # Recherche de l'administrateur correspondant au pseudo dans la table de données admin.
        admin = Admin.query.filter_by(pseudo=pseudo).first()

        if admin is None:
            # Le pseudo n'existe pas.
            current_app.logger.warning(f"Tentative de connexion échouée : pseudo {admin.pseudo} incorrect.")
            flash("Le pseudo est incorrect.", "login_admin")
            print("Le pseudo n'existe pas.")
        elif not bcrypt.checkpw(password.encode('utf-8'), admin.password_hash):
            # Password incorrect.
            current_app.logger.warning(f"Tentative de connexion échouée pour {admin.pseudo} : mot de passe incorrect.")
            flash("Le mot de passe est incorrect.", "login_admin")
            print("Le mot de passe n'existe pas.")
        elif role != admin.role:
            # Rôle incorrect.
            current_app.logger.warning(f"Tentative de connexion échouée pour {admin.pseudo} : rôle {role} incorrect.")
            flash("Le rôle est incorrect.", "login_admin")
            print("Le rôle n'existe pas.")
        else:
            # Si tout est correct.
            current_app.logger.info(f"L'administrateur {admin.pseudo} s'est bien connecté.")
            login_user(admin)
            session['pseudo'] = admin.pseudo
            print(admin.pseudo)
            session["role"] = admin.role
            print(admin.role)
            return render_template("admin/backend.html")

        return render_template("admin/admin_login.html", form_admin=form_admin)


# Route permettant à l'administrateur de se déconnecter.
@auth_bp.route('/backend/deconnexion-administrateur')
def logout_admin():
    """
    Déconnecte l'administrateur actuellement authentifié.

    Cette fonction supprime les informations d'identification de l'administrateur de la session Flask.

    Returns:
        Redirige l'administrateur vers la page d'accueil après la déconnexion.
    """
    # Supprime les informations d'identification de l'administrateur de la session.
    session.pop("logged_in", None)
    session.pop("identifiant", None)
    session.pop("admin_id", None)
    logout_user()

    # Redirige vers la page d'accueil après la déconnexion.
    return redirect(url_for('landing_page'))


# Route permettant à l'utilisateur de joindre le formulaire de connexion suite à une déconnexion.
@auth_bp.route("/connexion-utilisateur-formulaire-erreur", methods=['GET', 'POST'])
def user_connection_error():
    """
    Permet à l'utilisateur d'accéder au formulaire de connexion en cas d'erreur de connexion précédente.

    Returns:
        Template HTML du formulaire d'authentification utilisateur.

    Description:
        Cette route renvoie le formulaire d'authentification utilisateur pour permettre à l'utilisateur
        de se connecter à nouveau après une tentative de connexion infructueuse.

    Example:
        L'utilisateur accède à cette route via un navigateur web.
        La fonction renvoie le template HTML 'User/user_connection.html' contenant le formulaire de connexion.
        L'utilisateur peut saisir à nouveau ses identifiants pour se connecter.
    """
    # Instanciation du formulaire.
    form = UserConnection()
    return render_template("user/user_connection.html", form=form)


# Route permettant de réinitialiser le mot de passe utilisateur.
@auth_bp.route("/reinitialisation-password", methods=['GET', 'POST'])
def password_reset():
    """
    Réinitialise le mot de passe utilisateur.

    Cette fonction permet à l'utilisateur de réinitialiser son mot de passe en envoyant un e-mail avec un lien
    de réinitialisation. L'utilisateur clique sur le lien et accède au formulaire pour définir un nouveau mot de passe.
    Si l'utilisateur n'est pas à l'origine de la demande, un e-mail est envoyé à l'administrateur.

    Returns:
        Redirige vers une page d'attente avec le token de réinitialisation si le formulaire est soumis correctement.
        Sinon, renvoie le formulaire de réinitialisation du mot de passe.

    :param email(str): Adresse e-mail de l'utilisateur dont le mot de passe doit être réinitialisé.
    """
    # Création de l'instance du formulaire.
    form_password = ForgetPassword()

    # Vérification de la soumission du formulaire.
    if form_password.validate_on_submit():
        # Récupération de l'émail depuis le formulaire.
        email = form_password.email.data

        # Recherche de l'utilisateur dans la base de données en fonction de son email.
        user = User.query.filter_by(email=email).first()

        # Vérification de l'existence de l'utilisateur avec cet e-mail.
        if user:
            # Génération d'un token de réinitialisation du mot de passe.
            serializer = current_app.config['SECURITY_TOKEN_SERIALIZER']
            token = serializer.dumps(email, salt='password-reset-salt')
            reset_url = url_for('auth.recording_new_password', token=token, _external=True)

            # Redirection vers la page wait.html avec le token
            return redirect(url_for('auth.wait', token=token, email=email))

        else:
            # L'email n'existe pas dans la base de données, message d'erreur.
            flash("Cet email n'est pas reconnu dans notre système. Veuillez vérifier et réessayer.", "danger")

    return render_template('functional/reset_password.html', form_password=form_password)


# Route renvoyant une page d'attente.
@auth_bp.route("/patience")
def wait():
    """
    Affiche une page d'attente pendant l'envoi du lien réinitialisant le mot de passe.

    :param token : Jeton de réinitialisation du mot de passe.
    :param email : Email de l'utilisateur.
    """

    # Récupération des paramètres de requête.
    token = request.args.get('token')
    email = request.args.get('email')

    # Validation des paramètres.
    if not token or not email:
        flash('Lien invalide ou expiré.', 'danger')
        return redirect(url_for('auth.password_reset'))

    # Appel direct de la fonction d'envoi d'email.
    reset_url = url_for('auth.recording_new_password', token=token, _external=True)
    reset_password_mail(email, reset_url)

    return render_template('functional/wait.html')


# Route permettant de réinitialiser son mot de passe.
@auth_bp.route("/enregistrement-nouveau-mot-de-passe/<token>", methods=['GET', 'POST'])
def recording_new_password(token):
    """
    Route permettant de réinitialiser son mot de passe.

    :param token: Jeton de réinitialisation du mot de passe.
    :return: Redirige vers la page de connexion après la réinitialisation du mot de passe.
    """
    try:
        # Tentative de décryptage du token pour récupérer l'email associé.
        email = current_app.config['SECURITY_TOKEN_SERIALIZER'].loads(token, salt='password-reset-salt', max_age=3600)
    except Exception:
        flash('Le lien de réinitialisation du mot de passe est invalide ou a expiré.', 'danger')
        return redirect(url_for('landing_page'))

    # Instanciation du formulaire de réinitialisation du mot de passe.
    formpassword = RenamePassword()

    # Vérification de la soumission du formulaire.
    if formpassword.validate_on_submit():
        # Vérification que les deux mots de passe correspondent.
        if formpassword.new_password.data != formpassword.confirm_password.data:
            flash("Les mots de passe ne correspondent pas. Veuillez réessayer.", "danger")
            return redirect(url_for('auth.recording_new_password', token=token))

        # Recherche de l'utilisateur dans la base de données en fonction de son email.
        user = User.query.filter_by(email=email).first()

        # Si l'utilisateur est trouvé, mise à jour du mot de passe.
        if user:
            user.set_password(formpassword.new_password.data)
            db.session.commit()
            # Envoi d'un email de confirmation de réinitialisation réussie.
            password_reset_success_email(user)
            flash("Votre mot de passe a été mis à jour avec succès.", "success")

        # Redirection vers la page de connexion après succès.
        return redirect(url_for("auth.login"))

    return render_template('functional/recording_password.html', formpassword=formpassword, token=token)


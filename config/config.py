"""
Fichier de configuaration de l'application.
"""

# Ce fichier gère la mise en production, le développement et les tests établis par défaut.

import os

from dotenv import load_dotenv
from datetime import datetime

# Configuration des fichiers uploadés.
UPLOAD_FOLDER = "static/images/images_profil"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


class Config:
    """
    Config de base de l'application.
    
    Cette classe défiit les paramètres de configuration de base pour l'application Flask. 
    Il concerne le testing, le développement et la production.
    """
    
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = True
    
    # Configuration de la base de données.
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Monolithe8@localhost:5432/db_sethiarworks"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Clé secrète pour la session.
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # PAramètres de sécurité. des cookies de session.
    SESSION_COOKIE_SECURE = False # True en production
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 7  # 7 jours
    
    # Dossier des téléchargements.
    UPLOAD_FOLDER = UPLOAD_FOLDER
    
    
# Configuration de l'environnement de production.
class ProductionConfig(Config):
    """
    Configuration de l'environnement de production.
    
    Cette classe étend la configuration de base (Config) et ajuste les
    paramètres spécifiques à l'environnement de production.
    """
        
    # Chargement des variables d'environnement depuis le fichier .env
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
            
# Configuration de l'environnement de développement.
class DevelopmentConfig(Config):
    """
    Configuration de l'environnement de développement.
        
    Cette classe étend la configuration de base (Config) et ajuste les
    paramètres spécifiques à l'environnement de développement.
    """
        
    # Chargement des variables d'environnement depuis le fichier .env
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False
        
# Configuration de l'environnement de test.
class TestingConfig(Config):
    """
    Configuration de l'environnement de test.
        
    Cette classe étend la configuration de base (Config) et ajuste les
    paramètres spécifiques à l'environnement de test.
    """
        
    # Chargement des variables d'environnement depuis le fichier .env
    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False
    
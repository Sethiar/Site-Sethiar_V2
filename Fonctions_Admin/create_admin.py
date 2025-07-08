"""
Ce code crée un administrateur pour le site Sethiarworks. 

Il utilse bcrypt afin de hacher le mot de passe et le stocker de manière sécurisée.
"""

import sys
import os
import bcrypt

# Chemin absolu du répertoire courant.
current_dir = os.path.abspath(os.path.dirname(__file__))

# Chemin absolu du répertoire courant.
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Ajout du répertoire paent au sys.path.
sys.path.append(parent_dir)

# Import de la fonction conn() depuis db_sethiarworks.py.
from database_config.db_sethiarworks import conn


# Si besoin de changer les identifiants, c'est ici : 
pseudo = "Sethiar1er"
password = "Carmelithe3"
role = "SuperAdmin"

# Généraion d'un sel aléatoire pour le hachage du mot de passe.c
salt = bcrypt.gensalt()

# Hachage du mot de passe avec le sel généré.
password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)
# Vérification.
print("Le processus de hachage a bien fonctionné.")

# Sélection du curseur pour action sur base de données.
cur = conn.cursor()

# Insertion de l'identifiant et du mot de passe haché dans la base de données.
cur.execute(
    "INSERT INTO admin (pseudo, role, password_hash, salt) VALUES (%s, %s, %s, %s)",
    (pseudo, role, password_hash, salt)
)

# Vérification.
print("Les identifiants et le rôle de l'administrateur on t bin été enregistrés dans la table de données.")

# Validation de la procédure et enregistrement au sein de la base de données.
conn.commit()

# Génération d'un message affirmant que la procédure a bien fonctionné.
print("Tout roule. :)")
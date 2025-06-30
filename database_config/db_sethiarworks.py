#--------------------------------------------------------
# Configuration de la base de données.
#--------------------------------------------------------


"""
Ce script configure la connexion à la base de données du site entreprise de SethiarWorks

Il ermet de se connecter à la base de données PostgreSQL 'db_sethiarworks' en utilisant les paramètres spécifiés
(user, password, host, port et database).

Ensuite, il crée un curseur pour effectuer des opéraiton sur la base de données.

Finalement, il affiche la version de la base de données PostgreSQL.
"""

import psycopg2

# Paramètres de la base de données db_sethiarworks.

conn = psycopg2.connect(
    user="postgres",
    password="Monolithe8",
    host="localhost",
    port=5432,
    database="db_sethiarworks"
)

# Création du curseur pour pouvoir agir sur la base de données.
cur = conn.cursor()

# Affichage de la version PostgreSQL.
cur.execute("SELECT version();")
version = cur.fetchone()
print("Version de la base :", version, "\n")


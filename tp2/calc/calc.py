import socket
import sys
import logging
from datetime import datetime, timedelta
import re
import os

# Configuration du logger pour qu'il écrive tous les logs en sortie standard
logger = logging.getLogger("bs_server")
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# Vérification et récupération de la variable d'environnement CALC_PORT
port = os.getenv('CALC_PORT', 5000)  # Port par défaut si CALC_PORT n'est pas défini
try:
    # Convertir la valeur d'environnement en entier et la valider
    port = int(port)
    if not 0 <= port <= 65535:
        logger.error("Le port spécifié n'est pas un port possible (de 0 à 65535).")
        sys.exit(1)
    if 0 <= port <= 1024:
        logger.error("Le port spécifié est un port privilégié. Spécifiez un port au-dessus de 1024.")
        sys.exit(2)
except ValueError:
    logger.error("La valeur de CALC_PORT doit être un entier.")
    sys.exit(3)

host = '0.0.0.0'  # Écoute sur toutes les interfaces

# Lancement du serveur
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
logger.info(f"Le serveur tourne sur {host}:{port}")

last_client_time = datetime.now()

def safe_eval(expr):
    """ Évalue une expression arithmétique en toute sécurité. """
    # Autoriser uniquement les opérations arithmétiques de base avec des nombres entiers
    if not re.match(r'^[\d\+\-\*\/\(\) ]+$', expr):
        raise ValueError("Opération non autorisée.")
    # Évaluer l'expression
    return eval(expr, {'__builtins__': None}, {})

try:
    while True:
        conn, addr = s.accept()
        logger.info(f"Un client {addr[0]} s'est connecté.")
        last_client_time = datetime.now()

        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                try:
                    expression = data.decode().strip()
                    result = safe_eval(expression)
                    response = f"Le résultat de '{expression}' est {result}."
                except (ValueError, SyntaxError):
                    response = "Erreur : Opération non autorisée ou invalide."
                except Exception as e:
                    response = f"Erreur : {e}"
                
                conn.sendall(response.encode())
                logger.info(f"Calcul reçu : {expression}, réponse envoyée : {response}")

        except socket.error as e:
            logger.error(f"Une erreur de socket est survenue : {e}")
        finally:
            conn.close()

        # Vérification de la connexion client
        if datetime.now() - last_client_time > timedelta(minutes=1):
            logger.warning("Aucun client depuis plus de une minute.")
            last_client_time = datetime.now()

except KeyboardInterrupt:
    logger.info("Arrêt du serveur initié par l'utilisateur.")
finally:
    s.close()

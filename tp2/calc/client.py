import logging
import socket
import sys
import re

# logger = logging.getLogger("bs_client")
# logger.setLevel(logging.INFO)

# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# file_handler = logging.FileHandler("/var/log/bs_clients/bs_clients.log")
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

# class CustomStreamHandler(logging.StreamHandler):
#     def __init__(self):
#         super().__init__()

#     def emit(self, record):
#         red_color = '\033[91m'
#         reset_color = '\033[0m'
#         original_formatter = self.formatter

#         if record.levelno == logging.ERROR:
#             self.formatter = logging.Formatter(f"{red_color}{original_formatter._fmt}{reset_color}", datefmt='%Y-%m-%d %H:%M:%S')

#         super().emit(record)

#         self.formatter = original_formatter

# stream_handler = CustomStreamHandler()
# stream_handler.setFormatter(formatter)
# logger.addHandler(stream_handler)

# On définit la destination de la connexion
host = '127.0.0.1' 
port = 5000        

def validate_expression(expression):
    # Valide les composants individuels de l'expression
    for part in re.split(r'\s*[\+\-\*\/]\s*', expression):
        if part:
            number = int(part)
            if number < -100000 or number > 100000:
                return False
    return True

try:
    # Création de l'objet socket de type TCP (SOCK_STREAM)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connexion au serveur
    s.connect((host, port))
    logger.info(f"Connecté avec succès au serveur {host} sur le port {port}")

    while True:
        # Demande à l'utilisateur de saisir une opération arithmétique
        operation = input("Entrez une opération arithmétique ou 'exit' pour quitter: ")
        if operation.lower() == 'exit':
            break

        # Vérification de la validité de l'opération à l'aide d'une expression régulière
        if not re.match(r'^[-+]?[0-9]+(\s*[-+*/]\s*[-+]?[0-9]+)*$', operation):
            logger.error("Opération invalide.")
            continue
        
        # Vérification supplémentaire pour les limites des nombres
        if not validate_expression(operation):
            logger.error("Les nombres doivent être compris entre -100000 et +100000.")
            continue

        # Envoi de l'opération au serveur
        s.sendall(operation.encode())
        logger.info(f"Opération envoyée: {operation}")

        # Réception de la réponse du serveur
        response = s.recv(1024).decode('utf-8')
        logger.info(f"Réponse reçue: {response}")

except Exception as e:
    logger.error(f"Une erreur est survenue: {e}")
    sys.exit(1)

finally:
    s.close()
    logger.info("Connexion fermée.")
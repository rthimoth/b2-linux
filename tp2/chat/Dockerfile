# Utiliser une image Python 3.11 de base
FROM python:3.11

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY chat.py /app

# Exposer le port (par défaut 5000, mais peut être changé avec CHAT_PORT)
EXPOSE 5000

# Commande pour exécuter l'application
CMD ["python", "chat.py"]

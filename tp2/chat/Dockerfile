# Utiliser une image Python 3.11 de base
FROM python:3.11

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY chat.py /app

# Créer le répertoire pour les logs et donner les permissions appropriées
RUN mkdir -p /app/www && chmod 755 /app/www

# Exposer le port (par défaut 5000, mais peut être changé avec CHAT_PORT)
EXPOSE 5000

# Commande pour exécuter l'application
CMD ["python", "chat.py"]

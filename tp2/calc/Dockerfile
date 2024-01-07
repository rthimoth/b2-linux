# Utiliser une image Python de base
FROM python:3.11

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY calc.py /app

# Exposer le port (par défaut 5000, mais peut être changé avec CALC_PORT)
EXPOSE 5000

# Commande pour exécuter l'application
CMD ["python", "calc.py"]

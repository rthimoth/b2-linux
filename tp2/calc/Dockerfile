# Utiliser une image Python de base
FROM python:3.11

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier calc.py dans le répertoire de travail (déjà défini comme /app)
COPY calc.py /app

# Créer le répertoire pour les logs et donner les permissions appropriées
RUN mkdir -p /var/log/bs_server && chmod 755 /var/log/bs_server

# Exposer le port (par défaut 5000, mais peut être changé avec CALC_PORT)
EXPOSE 5000

# Commande pour exécuter l'application
CMD ["python", "calc.py"]


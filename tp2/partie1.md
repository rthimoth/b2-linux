TP2 Commun : Stack PHP

Copain PHP.
Droit au but : vous allez conteneuriser votre projet PHP Symfony.

Installer MySQL et Apache sur votre machine avec WAMP/LAMP/MAMP c'est bien si on s'en passe non ?

Le but donc :
➜ avoir un seul docker-compose.yml qui lance tout

un conteneur avec Apache/PHP installés qui fait tourner votre code
un conteneur base de données MySQL
un conteneur PHPMyAdmin pour gérer la base

➜ on utilise des images officielles dans l'idéal

on évite de rédiger des Dockerfile si on peut
surtout si c'est des images officielles

➜ donc pour bosser sur le projet :

docker compose up
tu dév sur ta machine, ça s'exécute sur des conteneurs

docker compose down quand t'as fini de dév, plus rien qui tourne

➜ et surtout : juste un fichier docker-compose.yml à se partager au sein du groupe

quelques lignes
pour avoir exactement le même environnement
à la racine du projet dans le dépôt git c'est carré


Sommaire


TP2 Commun : Stack PHP

Sommaire


0. Setup
I. Packaging de l'app PHP


0. Setup
➜ Dans le TP, l'emoji 📜 figurera à la fin de chaque partie pour t'indiquer quels fichiers tu dois rendre
Bon, je vais pas y couper, et j'vais découvrir encore plein de trucs que j'ai ps envie de découvrir.
T'es un dév. Tu dév avec ta machine, ton OS. Donc ça veut dire...
➜ Installer Docker sur votre PC

pas dans une VM quoi, sur ton PC
doc officielle
je préviens tout de suite pour les Windowsiens :

Docker nécessite soit WSL soit Hyper-V
je vous recommande WSL parce que Hyper-V il va péter votre VirtualBox
et même avec WSL, magic happens
on l'a vu en cours et premier TP, Docker, c'est une techno Linux...




Même si j'étais dév sous Windows, je préférerai lancer moi-même une VM Linux et faire deux trois bails d'intégration pour que je puisse lancer des commandes docker run sur mon PC qui lance des conteneurs dans la VM. Je peux vous apprendre c'est pas compliqué, faut juste lancer la VM quand tu veux use Docker (au lieu de lancer Docker, ça revient au même quoi finalement, t'façon il lance un noyau Linux pour toi le bougre si tu le fais pas toi-même). J'suis ptet trop un hippie après hein.



I. Packaging de l'app PHP
J'vous oriente dans la démarche :
➜ on a dit qu'on voulait 3 conteneurs

parce qu'on est pas des animaux à tout mettre dans le même
un conteneur = un process please

➜ d'abord on prend des infos sur les images dispos


PHP y'a une image officielle, lisez le README pour voir comment s'en servir

on dirait que le plus simple c'est de faire votre propre Dockerfile
surtout si vous avez besoin d'ajouter des libs
à vous de voir, lisez attentivement le README



idem pour MySQL

là pas besoin de Dockerfile, on utilise direct l'image
on peut config :

un user et son password, ainsi qu'une database à créer au lancement du conteneur
direct via des variables d'environnement
c'est de ouf pratique


on peut aussi jeter un fichier .sql dans le bon dossier (lire le README) avec un volume, et il sera exécuté au lancement

parfait pour créer un schéma de base




par contre pour PHPMyAdmin

pas d'image officielle
cherchez sur le Docker Hub y'a plusieurs gars qui l'ont packagé
c'est très répandu, donc y'a forcément une image qui fonctionne bien



➜ ensuite on run les bails

vous pouvez jouer avec des docker run un peu pour utiliser les images et voir comment elles fonctionnent
rapidement passer à la rédaction d'un docker-compose.yml qui lance les trois
lisez bien les README de vos images, y'a tout ce qu'il faut

Pour ce qui est du contenu du docker-compose.yml, à priori :


il déclare 3 conteneurs


PHP + Apache

un volume qui place votre code PHP dans le conteneur
partage de port pour accéder à votre site



MySQL

définition d'un user, son mot de passe, un nom de database à créer avec des variables d'environnement
injection d'un fichier .sql

pour créer votre schéma de base au lancement du conteneur
injecter des données simulées je suppose ?





PHPMyAdmin

dépend de l'image que vous utilisez
partage de port pour accéder à l'interface de PHPMyAdmin




en fin de TP1, vous avez vu que vous pouviez ping <NOM_CONTENEUR>

donc dans ton code PHP, faut changer l'IP de la base de données à laquelle tu te co
ça doit être vers le nom du conteneur de base de données




Donc : dès qu'un conteneur est déclaré dans un docker-compose.yml il peut joindre tous les autres via leurs noms sur le réseau. Et c'est bien pratique. Nik les adresses IPs.

Bon j'arrête de blabla, voilà le soleil.
🌞 docker-compose.yml

```
dans le fichier ecommerce/docker 


version: '3'

services:
  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: ecommercedev
    volumes:
      - ../db:/var/lib/mysql
      - ../seed/ecommercedev.sql:/docker-entrypoint-initdb.d/ecommercedev.sql
      - ./init-db.sh:/docker-entrypoint-initdb.d/init-db.sh
    networks:
      - ecommerce-network

  web:
    image: fyleeds/ecommerce:v2
    ports:
      - "80:80"
    depends_on:
      - db
    networks:
      - ecommerce-network

  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    environment:
      PMA_HOST: db
      PMA_USER: root
      PMA_PASSWORD: rootpassword
    ports:
      - "8080:80"
    depends_on:
      - db
    networks:
      - ecommerce-network

networks:
  ecommerce-network:
    driver: bridge
```


Dockerfile
```
FROM php:8.1-apache

# Install PHP extensions
ADD https://github.com/mlocati/docker-php-extension-installer/releases/latest/download/install-php-extensions /usr/local/bin/
RUN chmod +x /usr/local/bin/install-php-extensions && \
    install-php-extensions pdo pdo_mysql mysqli gd opcache intl zip calendar dom mbstring xsl && \
    a2enmod rewrite

# Install APCu
RUN pecl install apcu && docker-php-ext-enable apcu

# Install Composer
RUN curl -sS https://getcomposer.org/installer -o composer-setup.php && \
    php composer-setup.php --install-dir=/usr/local/bin --filename=composer && \
    rm composer-setup.php

# Install additional packages
RUN apt update && apt install -yqq nodejs npm locales coreutils apt-utils git libicu-dev g++ libpng-dev libxml2-dev libzip-dev libonig-dev libxslt-dev;

# Copy application source
COPY . /var/www/

# Configure Apache
COPY ./docker/apache-config.conf /etc/apache2/sites-available/ecommerce.conf
RUN a2dissite 000-default && a2ensite ecommerce

# Set permissions for the Symfony log directory
RUN mkdir -p /var/www/var/log 
# Install composer dependencies and run npm build

RUN cd /var/www && \
    touch .env && \
    echo "APP_ENV=dev" >> .env && \
    echo "APP_SECRET=92d36690c31f1efd2bb3f444bcee3a4c" >> .env && \
    echo "DATABASE_URL=\"mysql://root:rootpassword@db:3306/ecommercedev?serverVersion=5.7&charset=utf8mb4\"" >> .env


RUN cd /var/www && \
    composer install && \
    npm install --force && \
    npm run build 

RUN chown -R www-data:www-data /var/www/var && \
    chmod -R 755 /var/www/var

# Set the working directory
WORKDIR /var/www/

# Expose port 80
EXPOSE 80

```


genre tp2/php/docker-compose.yml dans votre dépôt git de rendu
votre code doit être à côté dans un dossier src : tp2/php/src/tous_tes_bails.php

s'il y a un script SQL qui est injecté dans la base à son démarrage, il doit être dans tp2/php/sql/seed.sql

on appelle ça "seed" une database quand on injecte le schéma de base et éventuellement des données de test


bah juste voilà ça doit fonctionner : je git clone ton truc, je docker compose up et ça doit fonctionne :)
ce serait cool que l'app affiche un truc genre App is ready on http://localhost:80 truc du genre dans les logs !

➜ Un environnement de dév local propre avec Docker

3 conteneurs, donc environnement éphémère/destructible
juste un docker-compose.yml donc facilement transportable
TRES facile de mettre à jour chacun des composants si besoin

oh tiens il faut ajouter une lib !
oh tiens il faut une autre version de PHP !
tout ça c'est np
II. Images


II. Images

1. Images publiques
2. Construire une image




1. Images publiques
🌞 Récupérez des images

avec la commande docker pull

récupérez :

l'image python officielle en version 3.11 (python:3.11 pour la dernière version)
l'image mysql officielle en version 5.7
l'image wordpress officielle en dernière version

c'est le tag :latest pour récupérer la dernière version
si aucun tag n'est précisé, :latest est automatiquement ajouté


l'image linuxserver/wikijs en dernière version

ce n'est pas une image officielle car elle est hébergée par l'utilisateur linuxserver contrairement aux 3 précédentes
on doit donc avoir un moins haut niveau de confiance en cette image




listez les images que vous avez sur la machine avec une commande docker

```
[ranvin@node1 ~]$ docker images
REPOSITORY           TAG       IMAGE ID       CREATED        SIZE
linuxserver/wikijs   latest    869729f6d3c5   6 days ago     441MB
mysql                5.7       5107333e08a8   8 days ago     501MB
python               latest    fc7a60e86bae   13 days ago    1.02GB
wordpress            latest    fd2f5a0c6fba   2 weeks ago    739MB
python               3.11      22140cbb3b0c   2 weeks ago    1.01GB
nginx                latest    d453dd892d93   8 weeks ago    187MB
hello-world          latest    d2c94e258dcb   7 months ago   13.3kB
```
```
[ranvin@node1 ~]$ docker ps -a
CONTAINER ID   IMAGE         COMMAND                  CREATED       STATUS                           PORTS                                               NAMES
11b6916c8525   python:3.11   "bash"                   2 hours ago   Exited (0) 2 hours ago                                                               tender_hertz
81347ece9ea3   python        "bash"                   3 hours ago   Exited (255) About an hour ago                                                       festive_pare
df496df1630e   nginx         "/docker-entrypoint.…"   3 hours ago   Exited (255) About an hour ago   80/tcp, 0.0.0.0:9999->8080/tcp, :::9999->8080/tcp   confident_wiles
da42e8e65053   nginx         "/docker-entrypoint.…"   3 hours ago   Created                                                                              flamboyant_sanderson
aa53a6e2557f   nginx         "/docker-entrypoint.…"   4 hours ago   Exited (0) 3 hours ago                                                               pedantic_fermi
4a3b6d652a6a   hello-world   "/hello"                 4 hours ago   Exited (0) 4 hours ago                                                               trusting_mayer
d9d614999d30   hello-world   "/hello"                 4 hours ago   Exited (0) 4 hours ago                                                               interesting_liskov
```


Quand on tape docker pull python par exemple, un certain nombre de choses est implicite dans la commande. Les images, sauf si on précise autre chose, sont téléchargées depuis le Docker Hub. Rendez-vous avec un navigateur sur le Docker Hub pour voir la liste des tags disponibles pour une image donnée. Sachez qu'il existe d'autres répertoires publics d'images comme le Docker Hub, et qu'on peut facilement héberger le nôtre. C'est souvent le cas en entreprise. On appelle ça un "registre d'images".

🌞 Lancez un conteneur à partir de l'image Python

lancez un terminal bash ou sh

vérifiez que la commande python est installée dans la bonne version


Sympa d'installer Python dans une version spéficique en une commande non ? Peu importe que Python soit déjà installé sur le système ou pas. Puis on détruit le conteneur si on en a plus besoin.

```
[ranvin@node1 ~]$ docker run -it python:3.11 bash
root@11b6916c8525:/# python --version
Python 3.11.7
```


2. Construire une image
Pour construire une image il faut :

créer un fichier Dockerfile

exécuter une commande docker build pour produire une image à partir du Dockerfile


🌞 Ecrire un Dockerfile pour une image qui héberge une application Python

l'image doit contenir

une base debian (un FROM)
l'installation de Python (un RUN qui lance un apt install)

il faudra forcément apt update avant
en effet, le conteneur a été allégé au point d'enlever la liste locale des paquets dispos
donc nécessaire d'update avant de install quoique ce soit


l'installation de la librairie Python emoji (un RUN qui lance un pip install)
ajout de l'application (un COPY)
le lancement de l'application (un ENTRYPOINT)


le code de l'application :


import emoji

print(emoji.emojize("Cet exemple d'application est vraiment naze :thumbs_down:"))



pour faire ça, créez un dossier python_app_build

pas n'importe où, c'est ton Dockerfile, ton caca, c'est dans ton homedir donc /home/<USER>/python_app_build

dedans, tu mets le code dans un fichier app.py

tu mets aussi le Dockerfile dedans

```
[ranvin@node1 python_app_build]$ cat Dockerfile
FROM debian

# Mise à jour et installation de Python
RUN apt-get update && apt-get install -y python3 python3-pip

# Installation de la bibliothèque emoji
RUN pip3 install emoji

# Ajout de l'application dans le conteneur
COPY app.py /app.py

# Définition du point d'entrée de l'application
ENTRYPOINT ["python3", "/app.py"]
```


J'y tiens beaucoup à ça, comprenez que Docker c'est un truc que le user gère. Sauf si vous êtes un admin qui vous en servez pour faire des trucs d'admins, ça reste dans votre /home. Les dévs quand vous bosserez avec Windows, vous allez pas stocker vos machins dans C:/Windows/System32/ si ? Mais plutôt dans C:/Users/<TON_USER>/TonCaca/ non ? Alors pareil sous Linux please.

🌞 Build l'image

déplace-toi dans ton répertoire de build cd python_app_build


docker build . -t python_app:version_de_ouf

le . indique le chemin vers le répertoire de build (. c'est le dossier actuel)

-t python_app:version_de_ouf permet de préciser un nom d'image (ou tag)


une fois le build terminé, constater que l'image est dispo avec une commande docker

```
[ranvin@node1 python_app_build]$ cd /home/ranvin/python_app_build
docker build . -t python_app:version_de_ouf
[+] Building 38.8s (5/8)                                                                                                                     docker:default
 => [internal] load .dockerignore                                                                                                                      0.2s
 => => transferring context: 2B                                                                                                                        0.0s
 => [internal] load build definition from Dockerfile                                                                                                   0.2s
 => => transferring dockerfile: 427B                                                                                                                   0.0s
 => [internal] load metadata for docker.io/library/debian:latest                                                                                       2.1s
 => [1/4] FROM docker.io/library/debian@sha256:bac353db4cc04bc672b14029964e686cd7bad56fe34b51f432c1a1304b9928da                                        0.2s
 => => resolve docker.io/library/debian@sha256:bac353db4cc04bc672b14029964e686cd7bad56fe34b51f432c1a1304b9928da                                        0.1s
 => => sha256:bac353db4cc04bc672b14029964e686cd7bad56fe34b51f432c1a1304b9928da 1.85kB / 1.85kB                                                         0.0s
 => => sha256:0dc902c61cb495db4630a6dc2fa14cd45bd9f8515f27fbb12e3d73a119d30bf1 529B / 529B                                                             0.0s
 => => sha256:2a033a8c63712da54b5a516f5d69d41606cfb5c4ce9aa1690ee55fc4f9babb92 1.46kB / 1.46kB                                                         0.0s
 => [internal] load build context                                                                                                                      0.1s
 => => transferring context: 187B                                                                                                                      0.0s
 => [2/4] RUN apt-get update && apt-get install -y python3 python3-pip
```


🌞 Lancer l'image

lance l'image avec docker run :


docker run python_app:version_de_oufw

```

```
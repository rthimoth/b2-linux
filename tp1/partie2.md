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



Quand on tape docker pull python par exemple, un certain nombre de choses est implicite dans la commande. Les images, sauf si on précise autre chose, sont téléchargées depuis le Docker Hub. Rendez-vous avec un navigateur sur le Docker Hub pour voir la liste des tags disponibles pour une image donnée. Sachez qu'il existe d'autres répertoires publics d'images comme le Docker Hub, et qu'on peut facilement héberger le nôtre. C'est souvent le cas en entreprise. On appelle ça un "registre d'images".

🌞 Lancez un conteneur à partir de l'image Python

lancez un terminal bash ou sh

vérifiez que la commande python est installée dans la bonne version


Sympa d'installer Python dans une version spéficique en une commande non ? Peu importe que Python soit déjà installé sur le système ou pas. Puis on détruit le conteneur si on en a plus besoin.


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




J'y tiens beaucoup à ça, comprenez que Docker c'est un truc que le user gère. Sauf si vous êtes un admin qui vous en servez pour faire des trucs d'admins, ça reste dans votre /home. Les dévs quand vous bosserez avec Windows, vous allez pas stocker vos machins dans C:/Windows/System32/ si ? Mais plutôt dans C:/Users/<TON_USER>/TonCaca/ non ? Alors pareil sous Linux please.

🌞 Build l'image

déplace-toi dans ton répertoire de build cd python_app_build


docker build . -t python_app:version_de_ouf

le . indique le chemin vers le répertoire de build (. c'est le dossier actuel)

-t python_app:version_de_ouf permet de préciser un nom d'image (ou tag)


une fois le build terminé, constater que l'image est dispo avec une commande docker


🌞 Lancer l'image

lance l'image avec docker run :


docker run python_app:version_de_oufw
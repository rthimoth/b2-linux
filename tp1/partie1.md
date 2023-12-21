I. Init


I. Init

1. Installation de Docker
2. Vérifier que Docker est bien là
3. sudo c pa bo
4. Un premier conteneur en vif
5. Un deuxième conteneur en vif




1. Installation de Docker
Pour installer Docker, il faut toujours (comme d'hab en fait) se référer à la doc officielle.
Je vous laisse donc suivre les instructions de la doc officielle pour installer Docker dans la VM.

Il n'y a pas d'instructions spécifiques pour Rocky dans la doc officielle, mais rocky est très proche de CentOS. Vous pouvez donc suivre les instructions pour CentOS 9.


2. Vérifier que Docker est bien là

# est-ce que le service Docker existe ?
systemctl status docker

# si oui, on le démarre alors
sudo systemctl start docker

# voyons si on peut taper une commande docker
sudo docker info
sudo docker ps



3. sudo c pa bo
On va faire en sorte que vous puissiez taper des commandes docker sans avoir besoin des droits root, et donc de sudo.
Pour ça il suffit d'ajouter votre utilisateur au groupe docker.

Pour que le changement de groupe prenne effet, il faut vous déconnecter/reconnecter de la session SSH (pas besoin de reboot la machine, pitié).

🌞 Ajouter votre utilisateur au groupe docker

vérifier que vous pouvez taper des commandes docker comme docker ps sans avoir besoin des droits root


➜ Vous pouvez même faire un alias pour docker
Genre si tu trouves que taper docker c'est long, et tu préférerais taper dk tu peux faire : alias dk='docker'. Si tu écris cette commande dans ton fichier ~/.bashrc alors ce sera effectif dans n'importe quel bash que tu ouvriras plutar.

4. Un premier conteneur en vif

Je rappelle qu'un "conteneur" c'est juste un mot fashion pour dire qu'on lance un processus un peu isolé sur la machine.

Bon trève de blabla, on va lancer un truc qui juste marche.
On va lancer un conteneur NGINX qui juste fonctionne, puis custom un peu sa conf. Ce serait par exemple pour tester une conf NGINX, ou faire tourner un serveur NGINX de production.

Hé les dévs, jouez le jeu bordel. NGINX c'est pas votre pote OK, mais on s'en fout, c'est une app comme toutes les autres, comme ta chatroom ou ta calculette. Ou Netflix ou LoL ou Spotify ou un malware. NGINX il est réputé et standard, c'est juste un outil d'étude pour nous là. Faut bien que je vous fasse lancer un truc. C'est du HTTP, c'est full standard, vous le connaissez, et c'est facile à tester/consommer : avec un navigateur.

🌞 Lancer un conteneur NGINX

avec la commande suivante :


docker run -d -p 9999:80 nginx



Si tu mets pas le -d tu vas perdre la main dans ton terminal, et tu auras les logs du conteneur directement dans le terminal. -d comme daemon : pour lancer en tâche de fond. Essaie pour voir !

🌞 Visitons

vérifier que le conteneur est actif avec une commande qui liste les conteneurs en cours de fonctionnement
afficher les logs du conteneur
afficher toutes les informations relatives au conteneur avec une commande docker inspect

afficher le port en écoute sur la VM avec un sudo ss -lnpt

ouvrir le port 9999/tcp (vu dans le ss au dessus normalement) dans le firewall de la VM
depuis le navigateur de votre PC, visiter le site web sur http://IP_VM:9999


➜ On peut préciser genre mille options au lancement d'un conteneur, go docker run --help pour voir !
➜ Hop, on en profite pour voir un truc super utile avec Docker : le partage de fichiers au moment où on docker run

en effet, il est possible de partager un fichier ou un dossier avec un conteneur, au moment où on le lance
avec NGINX par exemple, c'est idéal pour déposer un fichier de conf différent à chaque conteneur NGINX qu'on lance

en plus NGINX inclut par défaut tous les fichiers dans /etc/nginx/conf.d/*.conf

donc suffit juste de drop un fichier là-bas


ça se fait avec -v pour volume (on appelle ça "monter un volume")


C'est aussi idéal pour créer un conteneur qui setup un environnement de dév par exemple. On prépare une image qui contient Python + les libs Python qu'on a besoin, et au moment du docker run on partage notre code. Ainsi, on peut dév sur notre PC, et le code s'exécute dans le conteneur. On verra ça plus tard les dévs !

🌞 On va ajouter un site Web au conteneur NGINX

créez un dossier nginx

pas n'importe où, c'est ta conf caca, c'est dans ton homedir donc /home/<TON_USER>/nginx/



dedans, deux fichiers : index.html (un site nul) site_nul.conf (la conf NGINX de notre site nul)
exemple de index.html :


<h1>MEOOOW</h1>



config NGINX minimale pour servir un nouveau site web dans site_nul.conf :


server {
    listen        8080;

    location / {
        root /var/www/html;
    }
}



lancez le conteneur avec la commande en dessous, notez que :

on partage désormais le port 8080 du conteneur (puisqu'on l'indique dans la conf qu'il doit écouter sur le port 8080)
on précise les chemins des fichiers en entier
note la syntaxe du -v : à gauche le fichier à partager depuis ta machine, à droite l'endroit où le déposer dans le conteneur, séparés par le caractère :

c'est long putain comme commande




docker run -d -p 9999:8080 -v /home/<USER>/nginx/index.html:/var/www/html/index.html -v /home/<USER>/nginx/site_nul.conf:/etc/nginx/conf.d/site_nul.conf nginx


🌞 Visitons

vérifier que le conteneur est actif
aucun port firewall à ouvrir : on écoute toujours port 9999 sur la machine hôte (la VM)
visiter le site web depuis votre PC


5. Un deuxième conteneur en vif
Cette fois on va lancer un conteneur Python, comme si on voulait tester une nouvelle lib Python par exemple. Mais sans installer ni Python ni la lib sur notre machine.
On va donc le lancer de façon interactive : on lance le conteneur, et on pop tout de suite un shell dedans pour faire joujou.
🌞 Lance un conteneur Python, avec un shell

il faut indiquer au conteneur qu'on veut lancer un shell
un shell c'est "interactif" : on saisit des trucs (input) et ça nous affiche des trucs (output)

il faut le préciser dans la commande docker run avec -it



ça donne donc :


# on lance un conteneur "python" de manière interactive
# et on demande à ce conteneur d'exécuter la commande "bash" au démarrage
docker run -it python bash



Ce conteneur ne vit (comme tu l'as demandé) que pour exécuter ton bash. Autrement dit, si ce bash se termine, alors le conteneur s'éteindra. Autrement diiiit, si tu quittes le bash, le processus bash va se terminer, et le conteneur s'éteindra. C'est vraiment un conteneur one-shot quoi quand on utilise docker run comme ça.

🌞 Installe des libs Python

une fois que vous avez lancé le conteneur, et que vous êtes dedans avec bash

installez deux libs, elles ont été choisies complètement au hasard (avec la commande pip install):

aiohttp
aioconsole


tapez la commande python pour ouvrir un interpréteur Python
taper la ligne import aiohttp pour vérifier que vous avez bien téléchargé la lib


Notez que la commande pip est déjà présente. En effet, c'est un conteneur python, donc les mecs qui l'ont construit ont fourni la commande pip avec !

➜ Tant que t'as un shell dans un conteneur, tu peux en profiter pour te balader. Tu peux notamment remarquer :

si tu fais des ls un peu partout, que le conteneur a sa propre arborescence de fichiers
si t'essaies d'utiliser des commandes usuelles un poil évoluées, elles sont pas là

genre t'as pas ip a ou ce genre de trucs
un conteneur on essaie de le rendre le plus léger possible
donc on enlève tout ce qui n'est pas nécessaire par rapport à un vrai OS
juste une application et ses dépendances
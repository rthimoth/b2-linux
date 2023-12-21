III. Docker compose
Pour la fin de ce TP on va manipuler un peu docker compose.
🌞 Créez un fichier docker-compose.yml

dans un nouveau dossier dédié /home/<USER>/compose_test

le contenu est le suivant :


version: "3"

services:
  conteneur_nul:
    image: debian
    cmd: sleep 9999
  conteneur_flopesque:
    image: debian
    cmd: sleep 9999


Ce fichier est parfaitement équivalent à l'enchaînement de commandes suivantes (ne les faites pas hein, c'est juste pour expliquer) :

$ docker network create compose_test
$ docker run --name conteneur_nul --network compose_test debian sleep 9999
$ docker run --name conteneur_flopesque --network compose_test debian sleep 9999


🌞 Lancez les deux conteneurs avec docker compose

déplacez-vous dans le dossier compose_test qui contient le fichier docker-compose.yml

go exécuter docker compose up -d



Si tu mets pas le -d tu vas perdre la main dans ton terminal, et tu auras les logs des deux conteneurs. -d comme daemon : pour lancer en tâche de fond.

🌞 Vérifier que les deux conteneurs tournent

toujours avec une commande docker

tu peux aussi use des trucs comme docker compose ps ou docker compose top qui sont cools dukoo


docker compose --help pour voir les bails



🌞 Pop un shell dans le conteneur conteneur_nul

référez-vous au mémo Docker
effectuez un ping conteneur_flopesque (ouais ouais, avec ce nom là)

un conteneur est aussi léger que possible, aucun programme/fichier superflu : t'auras pas la commande ping !
il faudra installer un paquet qui fournit la commande ping pour pouvoir tester
juste pour te faire remarquer que les conteneurs ont pas besoin de connaître leurs IP : les noms fonctionnent
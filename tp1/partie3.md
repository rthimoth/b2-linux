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

```
[ranvin@node1 ~]$ sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
[sudo] password for ranvin:
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100 56.8M  100 56.8M    0     0  20.6M      0  0:00:02  0:00:02 --:--:-- 28.0M
[ranvin@node1 ~]$ sudo chmod +x /usr/local/bin/docker-compose
*[ranvin@node1 ~]$ sudo chmod +x /usr/local/bin/docker-compose
[ranvin@node1 ~]$ docker-compose --version
Docker Compose version v2.23.0
```

🌞 Lancez les deux conteneurs avec docker compose

déplacez-vous dans le dossier compose_test qui contient le fichier docker-compose.yml

go exécuter docker compose up -d

```
[ranvin@node1 compose_test]$ docker-compose up -d
[+] Running 3/3
 ✔ conteneur_flopesque Pulled                                                                                                                          2.7s
 ✔ conteneur_nul 1 layers [⣿]      0B/0B      Pulled                                                                                                   2.7s
   ✔ bc0734b949dc Already exists                                                                                                                       0.0s
[+] Building 0.0s (0/0)                                                                                                                      docker:default
[+] Running 3/3
 ✔ Network compose_test_default                  Created                                                                                               0.3s
 ✔ Container compose_test-conteneur_flopesque-1  Started                                                                                               0.1s
 ✔ Container compose_test-conteneur_nul-1        Started
```

Si tu mets pas le -d tu vas perdre la main dans ton terminal, et tu auras les logs des deux conteneurs. -d comme daemon : pour lancer en tâche de fond.

🌞 Vérifier que les deux conteneurs tournent

toujours avec une commande docker

tu peux aussi use des trucs comme docker compose ps ou docker compose top qui sont cools dukoo


docker compose --help pour voir les bails

```
[ranvin@node1 compose_test]$ docker-compose ps
NAME                                 IMAGE     COMMAND        SERVICE               CREATED          STATUS          PORTS
compose_test-conteneur_flopesque-1   debian    "sleep 9999"   conteneur_flopesque   19 seconds ago   Up 17 seconds
compose_test-conteneur_nul-1         debian    "sleep 9999"   conteneur_nul         19 seconds ago   Up 17 seconds
[ranvin@node1 compose_test]$ docker compose top
compose_test-conteneur_flopesque-1
UID    PID    PPID   C    STIME   TTY   TIME       CMD
root   1904   1855   0    10:21   ?     00:00:00   sleep 9999

compose_test-conteneur_nul-1
UID    PID    PPID   C    STIME   TTY   TIME       CMD
root   1897   1856   0    10:21   ?     00:00:00   sleep 9999
```


🌞 Pop un shell dans le conteneur conteneur_nul

référez-vous au mémo Docker
effectuez un ping conteneur_flopesque (ouais ouais, avec ce nom là)

un conteneur est aussi léger que possible, aucun programme/fichier superflu : t'auras pas la commande ping !
il faudra installer un paquet qui fournit la commande ping pour pouvoir tester
juste pour te faire remarquer que les conteneurs ont pas besoin de connaître leurs IP : les noms fonctionnent

```
[ranvin@node1 compose_test]$ docker exec -it compose_test-conteneur_nul-1 bash
```

```
apt-get update && apt-get install -y iputils-ping
```

```
root@7ac3911600de:/# ping conteneur_flopesque
PING conteneur_flopesque (172.18.0.2) 56(84) bytes of data.
64 bytes from compose_test-conteneur_flopesque-1.compose_test_default (172.18.0.2): icmp_seq=1 ttl=64 time=0.097 ms
64 bytes from compose_test-conteneur_flopesque-1.compose_test_default (172.18.0.2): icmp_seq=2 ttl=64 time=0.091 ms
64 bytes from compose_test-conteneur_flopesque-1.compose_test_default (172.18.0.2): icmp_seq=3 ttl=64 time=0.085 ms
64 bytes from compose_test-conteneur_flopesque-1.compose_test_default (172.18.0.2): icmp_seq=4 ttl=64 time=0.069 ms
64 bytes from compose_test-conteneur_flopesque-1.compose_test_default (172.18.0.2): icmp_seq=5 ttl=64 time=0.066 ms
^C
--- conteneur_flopesque ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4008ms
rtt min/avg/max/mdev = 0.066/0.081/0.097/0.012 ms
```
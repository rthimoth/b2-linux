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

```
sudo usermod -aG docker ranvin

```

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


```
docker run -d -p 9999:80 nginx
[ranvin@node1 ~]$ docker run -d -p 9999:80 nginx
Unable to find image 'nginx:latest' locally
latest: Pulling from library/nginx
af107e978371: Pull complete
336ba1f05c3e: Pull complete
8c37d2ff6efa: Pull complete
51d6357098de: Pull complete
782f1ecce57d: Pull complete
5e99d351b073: Pull complete
7b73345df136: Pull complete
Digest: sha256:bd30b8d47b230de52431cc71c5cce149b8d5d4c87c204902acf2504435d4b4c9
Status: Downloaded newer image for nginx:latest
aa53a6e2557f6fee10c34c7976985befed58bb6947293762e8df80d7643b776e

```



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


```
[ranvin@node1 ~]$ docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED              STATUS              PORTS                                   NAMES
aa53a6e2557f   nginx     "/docker-entrypoint.…"   About a minute ago   Up About a minute   0.0.0.0:9999->80/tcp, :::9999->80/tcp   pedantic_fermi

[ranvin@node1 ~]$ docker logs aa53a6e2557f
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2023/12/21 13:51:39 [notice] 1#1: using the "epoll" event method
2023/12/21 13:51:39 [notice] 1#1: nginx/1.25.3
2023/12/21 13:51:39 [notice] 1#1: built by gcc 12.2.0 (Debian 12.2.0-14)
2023/12/21 13:51:39 [notice] 1#1: OS: Linux 5.14.0-362.13.1.el9_3.x86_64
2023/12/21 13:51:39 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1073741816:1073741816
2023/12/21 13:51:39 [notice] 1#1: start worker processes
2023/12/21 13:51:39 [notice] 1#1: start worker process 28

[ranvin@node1 ~]$ docker inspect aa53a6e2557f
[
    {
        "Id": "aa53a6e2557f6fee10c34c7976985befed58bb6947293762e8df80d7643b776e",
        "Created": "2023-12-21T13:51:39.363604325Z",
        "Path": "/docker-entrypoint.sh",
        "Args": [
            "nginx",
            "-g",
            "daemon off;"
        ],
        "State": {
            "Status": "running",
            "Running": true,
            "Paused": false,
            "Restarting": false,
            "OOMKilled": false,
            "Dead": false,
            "Pid": 6909,
            "ExitCode": 0,
            "Error": "",
            "StartedAt": "2023-12-21T13:51:39.843820551Z",
            "FinishedAt": "0001-01-01T00:00:00Z"
        },
        "Image": "sha256:d453dd892d9357f3559b967478ae9cbc417b52de66b53142f6c16c8a275486b9",
        "ResolvConfPath": "/var/lib/docker/containers/aa53a6e2557f6fee10c34c7976985befed58bb6947293762e8df80d7643b776e/resolv.conf",
        "HostnamePath": "/var/lib/docker/containers/aa53a6e2557f6fee10c34c7976985befed58bb6947293762e8df80d7643b776e/hostname",
        "HostsPath": "/var/lib/docker/containers/aa53a6e2557f6fee10c34c7976985befed58bb6947293762e8df80d7643b776e/hosts",
        "LogPath": "/var/lib/docker/containers/aa53a6e2557f6fee10c34c7976985befed58bb6947293762e8df80d7643b776e/aa53a6e2557f6fee10c34c7976985befed58bb6947293762e8df80d7643b776e-json.log",
        "Name": "/pedantic_fermi",
        "RestartCount": 0,
        "Driver": "overlay2",
        "Platform": "linux",
        "MountLabel": "",
        "ProcessLabel": "",
        "AppArmorProfile": "",
        "ExecIDs": null,
        "HostConfig": {
            "Binds": null,
            "ContainerIDFile": "",
            "LogConfig": {
                "Type": "json-file",
                "Config": {}
            },
            "NetworkMode": "default",
            "PortBindings": {
                "80/tcp": [
                    {
                        "HostIp": "",
                        "HostPort": "9999"
                    }
                ]
            },
            "RestartPolicy": {
                "Name": "no",
                "MaximumRetryCount": 0
            },
            "AutoRemove": false,
            "VolumeDriver": "",
            "VolumesFrom": null,
            "ConsoleSize": [
                39,
                76
            ],
            "CapAdd": null,
            "CapDrop": null,
            "CgroupnsMode": "private",
            "Dns": [],
            "DnsOptions": [],
            "DnsSearch": [],
            "ExtraHosts": null,
            "GroupAdd": null,
            "IpcMode": "private",
            "Cgroup": "",
            "Links": null,
            "OomScoreAdj": 0,
            "PidMode": "",
            "Privileged": false,
            "PublishAllPorts": false,
            "ReadonlyRootfs": false,
            "SecurityOpt": null,
            "UTSMode": "",
            "UsernsMode": "",
            "ShmSize": 67108864,
            "Runtime": "runc",
            "Isolation": "",
            "CpuShares": 0,
            "Memory": 0,
            "NanoCpus": 0,
            "CgroupParent": "",
            "BlkioWeight": 0,
            "BlkioWeightDevice": [],
            "BlkioDeviceReadBps": [],
            "BlkioDeviceWriteBps": [],
            "BlkioDeviceReadIOps": [],
            "BlkioDeviceWriteIOps": [],
            "CpuPeriod": 0,
            "CpuQuota": 0,
            "CpuRealtimePeriod": 0,
            "CpuRealtimeRuntime": 0,
            "CpusetCpus": "",
            "CpusetMems": "",
            "Devices": [],
            "DeviceCgroupRules": null,
            "DeviceRequests": null,
            "MemoryReservation": 0,
            "MemorySwap": 0,
            "MemorySwappiness": null,
            "OomKillDisable": null,
            "PidsLimit": null,
            "Ulimits": null,
            "CpuCount": 0,
            "CpuPercent": 0,
            "IOMaximumIOps": 0,
            "IOMaximumBandwidth": 0,
            "MaskedPaths": [
                "/proc/asound",
                "/proc/acpi",
                "/proc/kcore",
                "/proc/keys",
                "/proc/latency_stats",
                "/proc/timer_list",
                "/proc/timer_stats",
                "/proc/sched_debug",
                "/proc/scsi",
                "/sys/firmware",
                "/sys/devices/virtual/powercap"
            ],
            "ReadonlyPaths": [
                "/proc/bus",
                "/proc/fs",
                "/proc/irq",
                "/proc/sys",
                "/proc/sysrq-trigger"
            ]
        },
        "GraphDriver": {
            "Data": {
                "LowerDir": "/var/lib/docker/overlay2/c62b5258b22a0a10571b5b0d0873a1e5ea55ba1c212b15ed933b17ff60baf93a-init/diff:/var/lib/docker/overlay2/0e905ce1e2742d54c61a3fcee80f3a261cbca87e1849c05c8e1494f58ef58ad3/diff:/var/lib/docker/overlay2/b655e4336baabd6eb09c5c9e39d65f98581a7a8dca334fcbcc05fe539abd9bc0/diff:/var/lib/docker/overlay2/d1af2436febb99ac9fc6adc632fcb5a21f2561760bd8111f17d260364bc2b5c8/diff:/var/lib/docker/overlay2/2dbad575654a892f5acc236b5ff08f27e54a8ee7c5be715cdb87925c04db757c/diff:/var/lib/docker/overlay2/a7a4190170fba96fdd2050932214d5e8a854b709342d04ad38d6fc5317c5f8eb/diff:/var/lib/docker/overlay2/24d97aa11fb02d7484de08708832c0a71e227c57b69c7128b3959f5abc63ff71/diff:/var/lib/docker/overlay2/e6eb0c078bb2b8f0912a927aa3c3ce7693e576a2ab27e198efd4bae2bd3d6fd7/diff",
                "MergedDir": "/var/lib/docker/overlay2/c62b5258b22a0a10571b5b0d0873a1e5ea55ba1c212b15ed933b17ff60baf93a/merged",
                "UpperDir": "/var/lib/docker/overlay2/c62b5258b22a0a10571b5b0d0873a1e5ea55ba1c212b15ed933b17ff60baf93a/diff",
                "WorkDir": "/var/lib/docker/overlay2/c62b5258b22a0a10571b5b0d0873a1e5ea55ba1c212b15ed933b17ff60baf93a/work"
            },
            "Name": "overlay2"
        },
        "Mounts": [],
        "Config": {
            "Hostname": "aa53a6e2557f",
            "Domainname": "",
            "User": "",
            "AttachStdin": false,
            "AttachStdout": false,
            "AttachStderr": false,
            "ExposedPorts": {
                "80/tcp": {}
            },
            "Tty": false,
            "OpenStdin": false,
            "StdinOnce": false,
            "Env": [
                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                "NGINX_VERSION=1.25.3",
                "NJS_VERSION=0.8.2",
                "PKG_RELEASE=1~bookworm"
            ],
            "Cmd": [
                "nginx",
                "-g",
                "daemon off;"
            ],
            "Image": "nginx",
            "Volumes": null,
            "WorkingDir": "",
            "Entrypoint": [
                "/docker-entrypoint.sh"
            ],
            "OnBuild": null,
            "Labels": {
                "maintainer": "NGINX Docker Maintainers <docker-maint@nginx.com>"
            },
            "StopSignal": "SIGQUIT"
        },
        "NetworkSettings": {
            "Bridge": "",
            "SandboxID": "598f9a9da7ff83ff376a63619a4833b10f6ae3c956cc38ab8095097a4db0ee8a",
            "HairpinMode": false,
            "LinkLocalIPv6Address": "",
            "LinkLocalIPv6PrefixLen": 0,
            "Ports": {
                "80/tcp": [
                    {
                        "HostIp": "0.0.0.0",
                        "HostPort": "9999"
                    },
                    {
                        "HostIp": "::",
                        "HostPort": "9999"
                    }
                ]
            },
            "SandboxKey": "/var/run/docker/netns/598f9a9da7ff",
            "SecondaryIPAddresses": null,
            "SecondaryIPv6Addresses": null,
            "EndpointID": "b3593fab0037d3ee3fa5dbbd56b32d4a281779c387f72bf00b8c8a997b9d9d45",
            "Gateway": "172.17.0.1",
            "GlobalIPv6Address": "",
            "GlobalIPv6PrefixLen": 0,
            "IPAddress": "172.17.0.2",
            "IPPrefixLen": 16,
            "IPv6Gateway": "",
            "MacAddress": "02:42:ac:11:00:02",
            "Networks": {
                "bridge": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": null,
                    "NetworkID": "224b68153c4d0e555eda3b5d8d2e3b53d7587f8e196cd51da69141a46b13bda3",
                    "EndpointID": "b3593fab0037d3ee3fa5dbbd56b32d4a281779c387f72bf00b8c8a997b9d9d45",
                    "Gateway": "172.17.0.1",
                    "IPAddress": "172.17.0.2",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "MacAddress": "02:42:ac:11:00:02",
                    "DriverOpts": null
                }
            }
        }
    }
]

[ranvin@node1 ~]$ sudo ss -lnpt
[sudo] password for ranvin:
State     Recv-Q    Send-Q       Local Address:Port          Peer Address:Port    Process
LISTEN    0         4096               0.0.0.0:9999               0.0.0.0:*        users:(("docker-proxy",pid=6868,fd=4))
LISTEN    0         511                0.0.0.0:26848              0.0.0.0:*        users:(("nginx",pid=1108,fd=6),("nginx",pid=1107,fd=6))
LISTEN    0         128                0.0.0.0:22                 0.0.0.0:*        users:(("sshd",pid=711,fd=3))
LISTEN    0         4096                  [::]:9999                  [::]:*        users:(("docker-proxy",pid=6873,fd=4))
LISTEN    0         511                   [::]:26848                 [::]:*        users:(("nginx",pid=1108,fd=7),("nginx",pid=1107,fd=7))
LISTEN    0         80                       *:3306                     *:*        users:(("mariadbd",pid=1017,fd=19))
LISTEN    0         128                   [::]:22                    [::]:*        users:(("sshd",pid=711,fd=4))
LISTEN    0         511                      *:80                       *:*        users:(("httpd",pid=752,fd=4),("httpd",pid=751,fd=4),("httpd",pid=750,fd=4),("httpd",pid=705,fd=4))




[ranvin@node1 ~]$ curl http://10.1.2.11:9999
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>

```


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


```
[ranvin@node1 nginx]$ docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS                                               NAMES
df496df1630e   nginx     "/docker-entrypoint.…"   4 seconds ago   Up 3 seconds   80/tcp, 0.0.0.0:9999->8080/tcp, :::9999->8080/tcp   confident_wiles
[ranvin@node1 nginx]$ curl http://10.1.2.11:9999
<h1>MEOOOW</h1>
```


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

```
[ranvin@node1 nginx]$ docker run -it python bash
Unable to find image 'python:latest' locally
latest: Pulling from library/python
bc0734b949dc: Pull complete
b5de22c0f5cd: Pull complete
917ee5330e73: Pull complete
b43bd898d5fb: Extracting [========================>                          ]  101.4MB/211.1MB
7fad4bffde24: Download complete
d685eb68699f: Download complete
107007f161d0: Download complete
02b85463d724: Download complete
```


Ce conteneur ne vit (comme tu l'as demandé) que pour exécuter ton bash. Autrement dit, si ce bash se termine, alors le conteneur s'éteindra. Autrement diiiit, si tu quittes le bash, le processus bash va se terminer, et le conteneur s'éteindra. C'est vraiment un conteneur one-shot quoi quand on utilise docker run comme ça.

🌞 Installe des libs Python

une fois que vous avez lancé le conteneur, et que vous êtes dedans avec bash

installez deux libs, elles ont été choisies complètement au hasard (avec la commande pip install):

aiohttp
aioconsole


tapez la commande python pour ouvrir un interpréteur Python
taper la ligne import aiohttp pour vérifier que vous avez bien téléchargé la lib

```
root@81347ece9ea3:/# pip install aiohttp aioconsole
Collecting aiohttp
  Obtaining dependency information for aiohttp from https://files.pythonhosted.org/packages/75/5f/90a2869ad3d1fb9bd984bfc1b02d8b19e381467b238bd3668a09faa69df5/aiohttp-3.9.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata
  Downloading aiohttp-3.9.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (7.4 kB)
Collecting aioconsole
  Obtaining dependency information for aioconsole from https://files.pythonhosted.org/packages/f7/39/b392dc1a8bb58342deacc1ed2b00edf88fd357e6fdf76cc6c8046825f84f/aioconsole-0.7.0-py3-none-any.whl.metadata
  Downloading aioconsole-0.7.0-py3-none-any.whl.metadata (5.3 kB)
Collecting attrs>=17.3.0 (from aiohttp)
  Downloading attrs-23.1.0-py3-none-any.whl (61 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 61.2/61.2 kB 1.6 MB/s eta 0:00:00
Collecting multidict<7.0,>=4.5 (from aiohttp)
  Downloading multidict-6.0.4.tar.gz (51 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 51.3/51.3 kB 5.2 MB/s eta 0:00:00
  Installing build dependencies ... done
```

```
root@81347ece9ea3:/etc# python
Python 3.12.1 (main, Dec 19 2023, 20:14:15) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import aiohttp
```

Notez que la commande pip est déjà présente. En effet, c'est un conteneur python, donc les mecs qui l'ont construit ont fourni la commande pip avec !

➜ Tant que t'as un shell dans un conteneur, tu peux en profiter pour te balader. Tu peux notamment remarquer :

si tu fais des ls un peu partout, que le conteneur a sa propre arborescence de fichiers
si t'essaies d'utiliser des commandes usuelles un poil évoluées, elles sont pas là

genre t'as pas ip a ou ce genre de trucs
un conteneur on essaie de le rendre le plus léger possible
donc on enlève tout ce qui n'est pas nécessaire par rapport à un vrai OS
juste une application et ses dépendances
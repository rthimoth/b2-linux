# Calculatrice Réseau

## Construction de l'image Docker

Pour construire l'image Docker, exécutez :

```bash
docker build -t calc .


docker run -it -p 13337:13337 calc bash


python calc.py

```

```
ranvin@ranvin-Nitro-AN515-57:~/b2-linux/tp2/calc$ docker run -it -p 13337:13337 calc bash
root@28672f1eedd0:/app# python calc.py 
2024-02-11 15:47:47 - INFO - Le serveur tourne sur 0.0.0.0:13337
2024-02-11 15:47:51 - INFO - Un client 172.17.0.1 s'est connecté.
2024-02-11 15:57:05 - INFO - Un client 172.17.0.1 s'est connecté.
```



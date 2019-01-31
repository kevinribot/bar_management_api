# Bar Management API

## Description

Il s'agit un webservice permettant de gérer un bar.
Une personne anonyme peut :
  - Passer une commande (**'/api/order/*{PK_COMPTOIR}*/'**)
  - Afficher la liste des références disponible (**'/api/menu/'**)
  
Une personne authentifié peut :
  - Afficher la liste des références (**'/api/references/'**)
  - Afficher la liste des comptoirs (**'/api/bars/'**)
  - Afficher les stocks  (**'/api/stock/*{PK_COMPTOIR}*/*'**)
  - Afficher la liste des références disponible (**'/api/menu/'**)
  - Afficher la liste des commandes effectuées (**'/api/order/*{PK}*'**)
  - Afficher le contenu d'une commande (**'/api/order/*{PK}*/'**)
  - Afficher des informations sur les comptoir (**'/api/bars/ranking/'**)

En plus, un administrateur peut :
  - Gérer les réferences (**'/api/references/'**)
  - Gérer les comptoirs (**'/api/bars/'**)
  - Gérer les stocks (**'/api/bars/'**)

## Technologie

![Python 3.1](https://img.shields.io/badge/dev-Python%203.1-green.svg)
![Django Rest Framework](https://img.shields.io/badge/framework-Django%20Rest%20Framework-yellowgreen.svg)

## Mise en place

### Installation 'Django Rest Framework'

J'ai utilisé la documentation [Django Rest Framework](https://www.django-rest-framework.org/) pour développeur ce programme.

## Installation

## Première éxécution

```
# Stop gitlab and remove its supervision process
sudo gitlab-ctl uninstall

# Debian/Ubuntu
sudo dpkg -r gitlab-ce

# Redhat/Centos
sudo rpm -e gitlab-ce
```

## Test unitiares

```
# Stop gitlab and remove its supervision process
sudo gitlab-ctl uninstall

# Debian/Ubuntu
sudo dpkg -r gitlab-ce

# Redhat/Centos
sudo rpm -e gitlab-ce
```

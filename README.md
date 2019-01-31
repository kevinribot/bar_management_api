# Bar Management API

## Description

This program is a webservice allowing to manage a bar.
An anonymous person can:
  - To place an order (**'/api/order/*{PK_BAR}*/'**)
  - Show the available list of references (**'/api/menu/'** or **'/api/menu/*{PK_BAR}*'**)
  
An authenticated person can:
  - Show the list of references (**'/api/references/'**)
  - Show the list of bars (**'/api/bars/'**)
  - Show the stock  (**'/api/stock/*{PK_BAR}*/*'**)
  - Show the available list of references (**'/api/menu/'** or **'/api/menu/*{PK_BAR}*'**)
  - Show the list of orders (**'/api/order/*{PK}*'**)
  - Show the contents of an order (**'/api/order/*{PK}*/'**)
  - Show informations of bars (**'/api/bars/ranking/'**)

An administrator can in more :
  - Manage references (**'/api/references/'**)
  - Manage bars (**'/api/bars/'**)
  - Manage stocks (**'/api/bars/'**)

## Technology

![Python 3.1](https://img.shields.io/badge/dev-Python%203.1-green.svg)
![Django Rest Framework](https://img.shields.io/badge/framework-Django%20Rest%20Framework-yellowgreen.svg)

## Installation 'Django Rest Framework'

```
# Stop gitlab and remove its supervision process
sudo gitlab-ctl uninstall

# Debian/Ubuntu
sudo dpkg -r gitlab-ce

# Redhat/Centos
sudo rpm -e gitlab-ce
```

## Première éxécution

```
# Stop gitlab and remove its supervision process
sudo gitlab-ctl uninstall

# Debian/Ubuntu
sudo dpkg -r gitlab-ce

# Redhat/Centos
sudo rpm -e gitlab-ce
```

## Unit Tests

```
# Stop gitlab and remove its supervision process
sudo gitlab-ctl uninstall

# Debian/Ubuntu
sudo dpkg -r gitlab-ce

# Redhat/Centos
sudo rpm -e gitlab-ce
```

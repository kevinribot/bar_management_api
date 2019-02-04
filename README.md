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
![PyCharm](https://img.shields.io/badge/IDE-PyCharm-yellow.svg)

## Installation 'Django Rest Framework'

```
pip install djangorestframework
pip install markdown       # Markdown support for the browsable API.
pip install django-filter  # Filtering support
```

## Première éxécution

```
python manage.py makemigrations bars
python manage.py migrate
python manage.py runserver
```

To initialize the database with test data you can use the following commands: 

```
python manage.py loaddata users_data.json
python manage.py loaddata references_data.json
python manage.py loaddata bars_data.json
python manage.py loaddata stocks_data.json
```

## Unit Tests

To run all unit tests you can use the following command:
```
python manage.py test
```

You can run them one by one:
```
python manage.py test bars.tests.%ClassName%.%MethodName%
```
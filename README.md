# Flux-RSS
Projet lecteur de flux de syndication

D'abord installer les dépendances

```
pipenv install
```
Ensuite ouvrez le shell de pipenv

```
pipenv shell
```

Puis initialiser la database

```
flask initdb
```

Enfin Vous pouvez lancer l'application avec

```
flask run
```
# Détails

Les définitions de routes sont dans app.py.

2 template sont proposé :
  - base.htm qui est la page de selection et de connexion/inscription
  - connected.html qui est la page de l'utilisateur lorqu'il est connecté

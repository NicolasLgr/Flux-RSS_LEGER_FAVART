from peewee import *
from flask_login import UserMixin

database = SqliteDatabase("database.sqlite3")

class BaseModel(Model):
    class Meta:
        database = database


#Base de donnés des Utilisateurs
class Utilisateur(BaseModel, UserMixin): 
    user = CharField(unique=True)
    password = CharField()

#Base de donnés des Flux
class Flux(BaseModel): 
    idUser = BigIntegerField()
    lienFlux = CharField()

#Création de la Base de donné
def create_tables():
    with database:
        database.create_tables([Utilisateur, Flux ])
        print("Creation tables")

#Suppression Baase de donné
def drop_tables():
    with database:
        database.drop_tables([Utilisateur, Flux ])
        print("Drop tables")

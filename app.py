from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import *
from forms import *
import os
import hashlib
import feedparser


import click

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'secretkey'

login_manager = LoginManager() 
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.get(id=user_id)

#Page d'accueil. Choix entre inscription ou connexion
@app.route('/')
def homepage():
    return render_template('base.html')

#Page d'inscription
@app.route('/inscription.html', methods=['GET', 'POST',])
def inscription():
    form = Inscription()
    if form.validate_on_submit():
        utilisateur = form.user.data
        MotDePasse = form.password.data
        MotDePasse=hashlib.sha1(MotDePasse.encode()).hexdigest()
        user = Utilisateur.select().where(Utilisateur.user == utilisateur).first()
        #Si l'utilisateur n'est pas créé alors on le rajoute dans la table
        if(user == None):
            login = Utilisateur()
            login.user = utilisateur.upper()
            login.password = MotDePasse
            login.save()
            return redirect(url_for('homepage'))
        #sinon on informe que l'utilisateur existe déjà et on le revoie sur homepage
        else:
            return redirect(url_for('homepage'))
    return render_template('inscription.html', form=form)

#Page de connexion
@app.route('/connexion.html', methods=['GET', 'POST'])
def connexion():
    form = Connexion()
    if form.validate_on_submit():
        user = form.user.data.upper()
        password = hashlib.sha1(form.password.data.encode()).hexdigest()
        user = Utilisateur.select().where((Utilisateur.user == user) & (Utilisateur.password == password)).first()
        print(user)
        if (user == None):
            print("Le pseudo ou le mot de passe ne correspond pas")
        else:
            login_user(user)
            current_user.idUtilisateur = user.id
            return redirect(url_for('accueil'))
    return render_template('connexion.html', form=form)

#Une fois l'user connecté
@app.route('/accueil.html')
@login_required
def accueil():
    listeFluxParse = []
    listeFluxUser = Flux.select().where(Flux.idUser == current_user.id)
    for item in listeFluxUser :
        fluxparse = feedparser.parse(item.lienFlux) 
        listeFluxParse.append(fluxparse)
    return render_template('accueil.html',listeFluxParse=listeFluxParse,listeFluxUser=listeFluxUser,zip=zip(listeFluxParse,listeFluxUser))



# Ajouter un Flux
@app.route('/AddFlux.html', methods=['GET', 'POST', ])
@login_required
def addFlux():
    form = AjoutFlux()
    if form.validate_on_submit():
        monfluxBDD = Flux.select().where((Flux.lienFlux == form.lien.data) & (Flux.idUser == current_user.id)).first()
        if(monfluxBDD == None): #Ajout du flux si il n'existe pas
            flow = Flux()
            flow.idUser = current_user.id
            flow.lienFlux = form.lien.data
            flow.save()
            flash('Flux ajouté')
            return redirect(url_for('accueil'))   
        else: ##Sinon on reste sur la page
            return redirect(url_for('addFlux'))
    return render_template('AddFlux.html',form=form)


#Voir le flux en détail
@app.route('/flux', methods=['GET', 'POST'])
@login_required
def visionnerFlux():
    linkFlux = request.args.get('linkFlux')
    fluxparse = feedparser.parse(linkFlux)
    element = feedparser.parse(linkFlux).entries
    return render_template('SeeFlux.html',fluxparse=fluxparse, element=element)


# Supprime un flux
@app.route('/supprimerFlux', methods=['GET','POST'])
@login_required
def supprimerFlux():
    idFluxUser = request.args.get('idFluxUser')
    linkFlux = request.args.get('linkFlux')
    requete = Flux.delete().where((Flux.idUser == idFluxUser) & (Flux.lienFlux == linkFlux))
    requete.execute()
    return redirect(url_for('accueil'))

# Deconnecte et renvoie l'utilisateur sur la page homepage
@app.route('/deconnexion')
@login_required
def deconnexion():
    logout_user()
    return redirect(url_for('homepage'))

#Creation de la base
@app.cli.command()
def initdb():
    create_tables()

#supression de la base
@app.cli.command()
def dropdb():
    drop_tables()


@app.cli.command()
def requete():
    """recherche lancé"""

    for flux in Flux.select():
        click.echo(flux.lienFlux)
        click.echo(flux.idUser)
    click.echo('fin recherche')

#initialisation des users pour les tests
@app.cli.command()
def inituser():
    utilisateur = Utilisateur()
    utilisateur.user = "Test"
    password = "test"
    utilisateur.password = hashlib.sha1(password.encode()).hexdigest()
    utilisateur.save()

    print('User Test created pasword: test')
#Import delle librerie necessari a Flask https://flask.palletsprojects.com/en/2.0.x/
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import *
from crypt import *
#Creo l'applicazione
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'hello world!'
#Inizializzazione variabili del server
app.config['UPLOADS'] = 'static/uploads/'
app.config['GAMES-UPLOADS'] = "static/uploads/games/"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config['VISITS'] = 0
app.config['HOSTS'] = []
#Funzione per generare lo slug di ogni articolo (Titolo articolo -> titolo-articolo)
def generate_slug(string):
    string.lower()
    slug=string.replace(" ", "-")
    return slug

#Inizializzazione del Database (file SQLite3)
db = SQLAlchemy(app)

#Modello dell'articolo
#Flask rispetta il Pattern MVC (Model-View-Control)
#e apporta una piccola modifica chiamandolo (Model-View-Template)
class Articolo(db.Model):
    __tablename__ = "articoli"
    titolo = db.Column("titolo", db.String(50), unique=True, primary_key=True)
    contenuto = db.Column("contenuto", db.Text)
    immagini = db.Column("immagini", db.String(200))
    categoria = db.Column("categoria", db.String(20))
    data_pubblicazione = db.Column("data_pubblicazione", db.Date)
    visualizzazioni = db.Column("visualizzazioni", db.Integer)
    anteprima = db.Column("anteprima_testo", db.Text)
    slug = db.Column("slug", db.String(40), unique=True)
    post_rel = db.Column("post", db.String(100), db.ForeignKey("post_salvati.post"))
    def __init__(self, titolo, contenuto, categoria, immagine, anteprima):
        self.titolo = titolo
        self.contenuto = contenuto
        self.categoria = categoria
        self.immagini = immagine
        self.anteprima = anteprima
        self.data_pubblicazione = datetime.today()
        self.visualizzazioni = 0
        self.slug = generate_slug(self.titolo)

class Gioco(db.Model):
    __tablename__ = "giochi"
    titolo = db.Column("titolo_gioco", db.String(255), primary_key=True)
    data_pubblicazione = db.Column("data_pubblicazione", db.Date)
    nome_file = db.Column("nome_file", db.String(255))
    downloads = db.Column("downloads", db.Integer)
    descrizione = db.Column("descrizione_gioco", db.Text)
    def __init__(self, titolo, descrizione, downloads, filename):
        self.titolo = titolo
        self.descrizione = descrizione
        self.downloads = downloads
        self.nome_file = filename
        self.data_pubblicazione = datetime.today()

class Utente(db.Model):
    __tablename__ = "utenti"
    username = db.Column("username", db.String(16), primary_key=True, unique=True)
    email = db.Column("email", db.String(50), unique=True)
    password = db.Column("password", db.String(100))
    newsletter = db.Column("newsletter", db.Boolean)
    admin_permissions = db.Column("permessi_admin", db.Boolean)
    user_rel = db.Column("user", db.String(255), db.ForeignKey("post_salvati.user"))
    def __init__(self, username, email, password, admin_permissions):
        self.username = username
        self.password = password
        self.email = email
        self.newsletter = 1
        self.admin_permissions = admin_permissions

class Commento(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    testo = db.Column("testo", db.Text)
    user = db.relationship("Utente", backref="utenti", lazy=True)
    title = db.relationship("Articolo", backref="articoli", lazy=True)
    username = db.Column("utente", db.String(16), db.ForeignKey("utenti.username"))
    titolo_articolo = db.Column("articolo", db.String(255), db.ForeignKey("articoli.titolo"))

    def __init__(self, testo, username, articolo):
        self.testo = testo
        self.username = username
        self.titolo_articolo = articolo

class PostSalvato(db.Model):
    __tablename__ = "post_salvati"
    id = db.Column("id", db.Integer, primary_key=True)
    utente = db.Column("user", db.String(16))
    articolo = db.Column("post", db.String(255))
    art_rel = db.relationship("Articolo", backref='articles')
    user_rel = db.relationship("Utente", backref='users')

class Punteggio(db.Model):
    __tablename__ = "punteggi"
    id = db.Column("id", db.Integer, primary_key=True)
    nome_utente = db.Column("nome_utente", db.String(20))
    titolo_gioco = db.Column("titolo_gioco", db.String(255))
    punteggio = db.Column("punteggio", db.Integer)

class Segnalazione(db.Model):
    __tablename__ = 'segnalazioni'
    id = db.Column('id', db.Integer, primary_key=True)
    nome_utente = db.Column("nome_utente", db.String(20))
    testo = db.Column('testo', db.String(255))

    def __init__(self, usr, txt):
        self.nome_utente = usr
        self.testo = txt
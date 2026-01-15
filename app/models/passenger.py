from flask_sqlalchemy import SQLAlchemy
from app import db

class Passenger(db.Model):
    __tablename__ = 'passengers'  # nome della tabella

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    eta = db.Column(db.Integer, nullable=False)
    CF = db.Column(db.String(50), unique=True, nullable=False)
    prelievo = db.Column(db.String(200), nullable=True)
    password = db.Column(db.String(100), nullable=False)
    punti = db.Column(db.Integer, default=0)

    def __init__(self, nome, cognome, email, eta, CF, prelievo, password, punti=0):
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.eta = eta
        self.CF = CF
        self.prelievo = prelievo
        self.password = password
        self.punti = punti
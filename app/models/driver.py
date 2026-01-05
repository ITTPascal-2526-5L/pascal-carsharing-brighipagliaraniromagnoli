from flask_sqlalchemy import SQLAlchemy
from app import db

class Driver(db.Model):
    __tablename__ = 'drivers'  # nome della tabella nel DB

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    eta = db.Column(db.Integer, nullable=False)
    CF = db.Column(db.String(50), unique=True, nullable=False)
    NrPatente = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, nome, cognome, email, eta, CF, NrPatente, password):
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.eta = eta
        self.CF = CF
        self.NrPatente = NrPatente
        self.password = password
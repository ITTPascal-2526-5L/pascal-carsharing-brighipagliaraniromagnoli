from flask_sqlalchemy import SQLAlchemy

from app import db

class School(db.Model):
    __tablename__ = 'schools'  # nome della tabella

    id = db.Column(db.Integer, primary_key=True)
    nomeScuola = db.Column(db.String(100), nullable=False)
    indirizzo = db.Column(db.String(200), nullable=False)
    suffix = db.Column(db.String(100), nullable=False)

    def __init__(self, nomeScuola, indirizzo, suffix):
        self.nomeScuola = nomeScuola
        self.indirizzo = indirizzo
        self.suffix = suffix

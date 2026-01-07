from flask import Blueprint, render_template, redirect, request, flash
from app.models.driver import Driver
from app.models.passenger import Passenger
from app.models.school import School
from app import db
import json
import os

registration_bp = Blueprint("registration", __name__)

# Cartella JSON (per backup)
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "..", "json")

def save_to_json(data, filename):
    filepath = os.path.join(DATA_FOLDER, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    existing_data.append(data)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)

# ---------------------- DRIVER ----------------------
@registration_bp.route("/registration_driver", methods=["GET", "POST"])
def registration_driver():
    if request.method == "POST":
        nome = request.form.get("nome")
        cognome = request.form.get("cognome")
        email = request.form.get("email")
        eta = request.form.get("eta")
        CF = request.form.get("CF")
        NrPatente = request.form.get("Pat")
        password = request.form.get("password")

        if not (nome and cognome and email and eta and CF and NrPatente and password):
            flash("Tutti i campi sono obbligatori.")
            return render_template("driverLogin.html")

        # Salvataggio su JSON
        driver_data = {
            "nome": nome,
            "cognome": cognome,
            "email": email,
            "eta": eta,
            "CF": CF,
            "NrPatente": NrPatente,
            "password": password
        }
        save_to_json(driver_data, "driver.json")

        # Salvataggio su DB
        driver = Driver(nome=nome, cognome=cognome, email=email, eta=int(eta),
                        CF=CF, NrPatente=NrPatente, password=password)
        db.session.add(driver)
        db.session.commit()

        flash("Registrazione avvenuta con successo! Effettua il login.")
        return render_template("login.html")

    return render_template("driverLogin.html")


# ---------------------- PASSENGER ----------------------
@registration_bp.route("/registration_passenger", methods=["GET", "POST"])
def registration_passenger():
    if request.method == "POST":
        nome = request.form.get("nome")
        cognome = request.form.get("cognome")
        email = request.form.get("email")
        eta = request.form.get("eta")
        CF = request.form.get("CF")
        prelievo = request.form.get("prelievo")
        password = request.form.get("password")

        if not (nome and cognome and email and eta and CF and prelievo and password):
            flash("Tutti i campi sono obbligatori.")
            return render_template("passengerLogin.html")

        passenger_data = {
            "nome": nome,
            "cognome": cognome,
            "email": email,
            "eta": eta,
            "CF": CF,
            "prelievo": prelievo,
            "password": password
        }
        save_to_json(passenger_data, "passenger.json")

        passenger = Passenger(nome=nome, cognome=cognome, email=email,
                              eta=int(eta), CF=CF, prelievo=prelievo, password=password)
        db.session.add(passenger)
        db.session.commit()

        flash("Registrazione avvenuta con successo! Effettua il login.")
        return render_template("login.html")

    return render_template("passengerLogin.html")


# ---------------------- SCHOOL ----------------------
@registration_bp.route("/registration_school", methods=["GET", "POST"])
def registration_school():
    if request.method == "POST":
        nomeScuola = request.form.get("nomeScuola")
        indirizzo = request.form.get("indirizzo")
        suffix = request.form.get("suffix")

        if not (nomeScuola and indirizzo and suffix):
            flash("Tutti i campi sono obbligatori.")
            return render_template("schoolLogin.html")

        school_data = {
            "nomeScuola": nomeScuola,
            "indirizzo": indirizzo,
            "suffix": suffix
        }
        save_to_json(school_data, "school.json")

        school = School(nomeScuola=nomeScuola, indirizzo=indirizzo, suffix=suffix)
        db.session.add(school)
        db.session.commit()

        flash("Registrazione avvenuta con successo! Effettua il login.")
        return render_template("login.html")

    return render_template("schoolLogin.html")


# ---------------------- VIEW ----------------------
@registration_bp.route("/view")
def view():
    # Legge i record dal database
    passengers = Passenger.query.all()
    drivers = Driver.query.all()
    schools = School.query.all()
    
    return render_template("view.html", passengers=passengers, drivers=drivers, schools=schools)
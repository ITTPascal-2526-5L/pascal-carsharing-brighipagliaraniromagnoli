from flask import Blueprint, render_template, redirect, request, flash
from app.models.driver import Driver
from app.models.passenger import Passenger
import json
import os

registration_bp = Blueprint("registration", __name__)

# json.dumps()
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "..", "json")

def save_to_json(data, filename):
    #os.makedirs(DATA_FOLDER, exist_ok=True)
    filepath = os.path.join(DATA_FOLDER, filename)

    # Se il file esiste, carica i dati esistenti
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    # Aggiunge il nuovo record
    existing_data.append(data)

    # Scrive nel file
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)

drivers = [] 
passengers = [] 
schools=[]

@registration_bp.route("/registration_driver", methods=["GET", "POST"])
def registration_driver():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        if not (name and email and password):
            flash("Tutti i campi sono obbligatori.")
            return render_template("driverLogin.html")
        driver = Driver(name, email, password)
        #drivers.append(driver)
        save_to_json(driver, "driver.json")
        flash("Registrazione avvenuta con successo!")
        return redirect("/registration_driver")
    return render_template("driverLogin.html")

@registration_bp.route("/registration_passenger")
def registration_passenger():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        if not (name and email and password):
            flash("Tutti i campi sono obbligatori.")
            return render_template("passsengerRegistration.html")
        passenger = Passenger(name, email, password)
        save_to_json(passenger, "passenger.json")
        #passengers.append(passenger)
        flash("Registrazione avvenuta con successo!")
        return redirect("/registration_passenger")
    return render_template("passengerLogin.html")

@registration_bp.route("/registration_school", methods=["GET", "POST"])
def registration_school():
    if request.method == "POST":
        name = request.form.get("nomeScuola")
        ind = request.form.get("indirizzo")
        suffix = request.form.get("suffix")
        if not (name and ind and suffix):
            flash("Tutti i campi sono obbligatori.")
            return render_template("schoolLogin.html")

        # Meglio salvare come dizionario, non lista
        school = {
            "nomeScuola": name,
            "indirizzo": ind,
            "suffix": suffix
        }

        save_to_json(school, "school.json")

        flash("Registrazione avvenuta con successo!")
        return redirect("/registration_school")

    # GET -> Mostra il form
    return render_template("schoolLogin.html")
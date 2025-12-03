from flask import Blueprint, render_template, redirect, request, flash
from app.models.driver import Driver
from app.models.passenger import Passenger
import json
import os

registration_bp = Blueprint("registration", __name__)

# json.dumps()
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

drivers = [] 
passengers = [] 
schools=[]

@registration_bp.route("/registration_driver", methods=["GET", "POST"])
def registration_driver():
    if request.method == "POST":
        name = request.form.get("nome")
        cognome = request.form.get("cognome")
        email = request.form.get("email")
        eta = request.form.get("eta")
        CF = request.form.get("CF")
        IdPatente = request.form.get("Pat")
        password=request.form.get("password")
        if not (name and email and eta and CF and IdPatente and password):
            flash("Tutti i campi sono obbligatori.")
            return render_template("driverLogin.html")
        #driver = Driver(name, email, password)

        driver = {
            "nome": name,
            "cognome": cognome,
            "email": email,
            "eta":eta,
            "CF":CF,
            "NrPatente":IdPatente,
            "password":password
        }

        #drivers.append(driver)
        save_to_json(driver, "driver.json")
        flash("Registrazione avvenuta con successo! Effettua il login.")
        #return redirect("/login")
        return render_template("login.html")
    return render_template("driverLogin.html")

@registration_bp.route("/registration_passenger", methods=["GET", "POST"])
def registration_passenger():
    if request.method == "POST":
        name = request.form.get("nome")
        cognome = request.form.get("cognome")
        email = request.form.get("email")
        eta = request.form.get("eta")
        CF = request.form.get("CF")
        prelievo = request.form.get("prelievo")
        password = request.form.get("password")
        
        if not (name and email and eta and CF and prelievo and password):
            flash("Tutti i campi sono obbligatori.")
            return render_template("passengerLogin.html")
        passenger = {
            "nome": name,
            "cognome": cognome,
            "email": email,
            "eta":eta,
            "CF":CF,
            "prelievo":prelievo,
            "password":password
        }
        save_to_json(passenger, "passenger.json")
        flash("Registrazione avvenuta con successo! Effettua il login.")
        return render_template("login.html")
        #return redirect("/login")
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

        school = {
            "nomeScuola": name,
            "indirizzo": ind,
            "suffix": suffix
        }

        save_to_json(school, "school.json")
        flash("Registrazione avvenuta con successo! Effettua il login.")
        #return redirect("/login")
        return render_template("login.html")
    return render_template("schoolLogin.html")

@registration_bp.route("/view")
def view():
    passenger_path = os.path.join(DATA_FOLDER, "passenger.json")
    driver_path = os.path.join(DATA_FOLDER, "driver.json")
    school_path = os.path.join(DATA_FOLDER, "school.json")

    passengers = []
    drivers = []
    schools = []

    if os.path.exists(passenger_path):
        with open(passenger_path, "r", encoding="utf-8") as f:
            passengers = json.load(f)

    if os.path.exists(driver_path):
        with open(driver_path, "r", encoding="utf-8") as f:
            drivers = json.load(f)

    if os.path.exists(school_path):
        with open(school_path, "r", encoding="utf-8") as f:
            schools = json.load(f)

    return render_template("view.html",passengers=passengers,drivers=drivers,schools=schools)
 

 
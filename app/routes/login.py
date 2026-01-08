from flask import Blueprint, render_template, redirect, request, flash, session
import json
import os
from werkzeug.utils import secure_filename
from app.models.driver import Driver
from app.models.passenger import Passenger
from app.models.school import School
from app import db


login_bp = Blueprint("login", __name__)

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "..", "json")

def check_credentials(email, password):
    # Controlla Passenger
    passenger = Passenger.query.filter_by(email=email, password=password).first()
    if passenger:
        return passenger.nome

    # Controlla Driver
    driver = Driver.query.filter_by(email=email, password=password).first()
    if driver:
        return driver.nome

    # Controlla School (login con nomeScuola e suffix come password)
    school = School.query.filter_by(nomeScuola=email, suffix=password).first()
    if school:
        return school.nomeScuola
    return None

# @login_bp.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         nameLogin=request.form.get("email")
#         password=request.form.get("password")
#         if(check_credentials(nameLogin,password)):
#             return render_template("menu.html")
#         else:
#             return render_template("login.html")
#     else:
#         return render_template("login.html")
    
@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = check_credentials(email, password)

        if user:
            session["username"] = user
            return redirect("/menu")

        flash("Credenziali errate")
        return redirect("/login")

    return render_template("login.html")
    

@login_bp.route("/menu")
def menu():
    username = session.get("username")
    if not username:
        return redirect("/login")

    # Se è driver
    user_type = "passenger" 
    driver_path = os.path.join(DATA_FOLDER, "driver.json")
    if os.path.exists(driver_path):
        with open(driver_path, "r", encoding="utf-8") as f:
            drivers = json.load(f)
            for d in drivers:
                if d.get("nome") == username:
                    user_type = "driver"
                    break
    # Controlla se è passenger
    user_type = "passenger" 
    passenger_path = os.path.join(DATA_FOLDER, "passenger.json")
    if os.path.exists(passenger_path):
        with open(passenger_path, "r", encoding="utf-8") as f:
            passengers = json.load(f)
            for p in passengers:
                if p.get("nome") == username:
                    user_type = "passenger"
                    break

        # Controlla se è school
    user_type = "" 
    school_path = os.path.join(DATA_FOLDER, "school.json")
    if os.path.exists(school_path):
        with open(school_path, "r", encoding="utf-8") as f:
            schools = json.load(f)
            for s in schools:
                if s.get("nomeScuola") == username:
                    user_type = "school"
                    break

    return render_template("menu.html", user=username, user_type=user_type)


ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}
UPLOAD_FOLDER = os.path.join(DATA_FOLDER, "app/static/img")  # cartella dove salva i file


os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_bp.route("/upload", methods=["POST"])
def upload_file():
    username = session.get("username")
    if not username:
        flash("Devi fare il login")
        return redirect("/login")

    # Qui controlla se l'utente è un driver
    # Puoi leggere il JSON driver per confermare
    driver_path = os.path.join(DATA_FOLDER, "driver.json")
    is_driver = False
    if os.path.exists(driver_path):
        with open(driver_path, "r", encoding="utf-8") as f:
            drivers = json.load(f)
            for d in drivers:
                if d.get("nome") == username:
                    is_driver = True
                    break

    if not is_driver:
        flash("Solo i driver possono caricare file")
        return redirect("/menu")

    if 'file' not in request.files:
        flash("Nessun file selezionato")
        return redirect("/menu")

    file = request.files['file']

    if file.filename == '':
        flash("Nessun file selezionato")
        return redirect("/menu")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        flash(f"File {filename} caricato con successo!")
        return redirect("/menu")
    else:
        flash("Tipo di file non consentito!")
        return redirect("/menu")
   

@login_bp.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")



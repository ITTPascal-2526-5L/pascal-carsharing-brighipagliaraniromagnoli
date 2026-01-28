from flask import Blueprint, render_template, redirect, request, flash, session
import json
import os
from werkzeug.utils import secure_filename
from app.models.driver import Driver
from app.models.passenger import Passenger
from app.models.school import School
from app import db
import random
import string
from flask import jsonify


login_bp = Blueprint("login", __name__)

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "..", "json")

def check_credentials(email, password):
    # Controlla Passenger
    passenger = Passenger.query.filter_by(email=email, password=password).first()
    if passenger:
        return passenger.nome, "passenger"

    # Controlla Driver
    driver = Driver.query.filter_by(email=email, password=password).first()
    if driver:
        return driver.nome, "driver"

    # Controlla School (login con nomeScuola e suffix come password)
    school = School.query.filter_by(nomeScuola=email, suffix=password).first()
    if school:
        return school.nomeScuola, "school"
    return None, None

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

        user, user_type = check_credentials(email, password)

        if user:
            session["username"] = user
            session["user_type"] = user_type
            return redirect("/menu")

        flash("Credenziali errate")
        return redirect("/login")

    return render_template("login.html")
    

@login_bp.route("/menu")
def menu():
    username = session.get("username")
    user_type = session.get("user_type")
    punti = 0
    if not username or not user_type:
        return redirect("/login")
    if user_type == "passenger":
        user = Passenger.query.filter_by(nome=username).first()
        if user:
            punti = user.punti
    elif user_type == "driver":
        user = Driver.query.filter_by(nome=username).first()
        if user:
            punti = user.punti
    return render_template("menu.html", user=username, user_type=user_type, punti=punti)


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

@login_bp.route("/negozio")
def negozio():
    username = session.get("username")
    user_type = session.get("user_type")
    if not username or not user_type:
        return redirect("/login")
    return render_template("negozio.html", user=username, user_type=user_type)

@login_bp.route("/acquista_premio", methods=["POST"])
def acquista_premio():
    if "username" not in session or "user_type" not in session:
        return jsonify({"success": False, "message": "Devi essere loggato."}), 401
    if session["user_type"] != "passenger":
        return jsonify({"success": False, "message": "Solo i passeggeri possono acquistare premi."}), 403
    from app.models.passenger import Passenger
    user = Passenger.query.filter_by(nome=session["username"]).first()
    if not user:
        return jsonify({"success": False, "message": "Utente non trovato."}), 404
    premio = request.json.get("premio")
    costi = {
        "colazione": 20,
        "bus": 35,
        "carburante": 50,
        "checkup": 60,
        "ombrello": 40,
        "gadget": 25
    }
    if premio not in costi:
        return jsonify({"success": False, "message": "Premio non valido."}), 400
    costo = costi[premio]
    if user.punti < costo:
        return jsonify({"success": False, "message": "Punti insufficienti."}), 400
    user.punti -= costo
    codice = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    db.session.commit()
    return jsonify({"success": True, "codice": codice, "message": "Premio acquistato con successo!"})

@login_bp.route("/crea_corsa", methods=["GET", "POST"])
def crea_corsa():
    username = session.get("username")
    user_type = session.get("user_type")
    if not username or user_type != "driver":
        return redirect("/login")
    
    if request.method == "POST":
        flash("La tua corsa è stata creata con successo!")
        return redirect("/menu")
        
    return render_template("crea_corsa.html", user=username)

@login_bp.route("/corse_disponibili", methods=["GET", "POST"])
def corse_disponibili():
    username = session.get("username")
    user_type = session.get("user_type")
    if not username or user_type != "passenger":
        return redirect("/login")
    
    # Mock data for available rides
    rides = [
        {"id": 1, "driver": "Marco", "partenza": "Bologna", "arrivo": "Cesena", "raggio": 2},
        {"id": 2, "driver": "Giacomo", "partenza": "Rimini", "arrivo": "Cesena", "raggio": 3}
    ]
    
    if request.method == "POST":
        flash("Richiesta inviata con successo!")
        return redirect("/menu")
        
    return render_template("corse_disponibili.html", user=username, rides=rides)

from flask import Blueprint, render_template, redirect, request, flash, session
import json
import os
from werkzeug.utils import secure_filename


login_bp = Blueprint("login", __name__)

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "..", "json")

def check_credentials(email, password):

    passenger_path = os.path.join(DATA_FOLDER, "passenger.json")
    if os.path.exists(passenger_path):
        with open(passenger_path, "r", encoding="utf-8") as f:
            passengers = json.load(f)
            for p in passengers:
                if p.get("email") == email and p.get("password") == password:
                    return p.get("nome", "Utente")

    driver_path = os.path.join(DATA_FOLDER, "driver.json")
    if os.path.exists(driver_path):
        with open(driver_path, "r", encoding="utf-8") as f:
            drivers = json.load(f)
            for d in drivers:
                if d.get("email") == email and d.get("password") == password:
                    return d.get("nome", "Utente")

    school_path = os.path.join(DATA_FOLDER, "school.json")
    if os.path.exists(school_path):
        with open(school_path, "r", encoding="utf-8") as f:
            schools = json.load(f)
            for s in schools:
                if s.get("nomeScuola") == email and s.get("suffix") == password:
                    return s.get("nomeScuola", "Scuola")
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

    # Controlla se è driver
    user_type = "passenger" 
    driver_path = os.path.join(DATA_FOLDER, "driver.json")
    if os.path.exists(driver_path):
        with open(driver_path, "r", encoding="utf-8") as f:
            drivers = json.load(f)
            for d in drivers:
                if d.get("nome") == username:
                    user_type = "driver"
                    break

    return render_template("menu.html", user=username, user_type=user_type)


ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}
UPLOAD_FOLDER = os.path.join(DATA_FOLDER, "app/static/img")  # cartella dove salvare i file


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
          
        
     
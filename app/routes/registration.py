from flask import Blueprint, render_template, redirect, request, flash
from app.models.driver import Driver

registration_bp = Blueprint("registration", __name__)

drivers = []  # Lista temporanea per i driver registrati

@registration_bp.route("/registration_driver", methods=["GET", "POST"])
def registration_driver():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        if not (name and email and password):
            flash("Tutti i campi sono obbligatori.")
            return render_template("driverRegistration.html")
        driver = Driver(name, email, password)
        drivers.append(driver)
        flash("Registrazione avvenuta con successo!")
        return redirect("/registration_driver")
    return render_template("driverRegistration.html")

@registration_bp.route("/registration_passenger")
def registration_passenger():
        if request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")
        if not (name and email and password):
            flash("Tutti i campi sono obbligatori.")
            return render_template("driverRegistration.html")
        driver = Driver(name, email, password)
        drivers.append(driver)
        flash("Registrazione avvenuta con successo!")
        return redirect("/registration_driver")
    
    return render_template("passengerLogin.html")
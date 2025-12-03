from flask import Blueprint, render_template, redirect

main_bp = Blueprint("main", __name__)

@main_bp.route("/")

def homepage():
    # TODO: Add login session logic here 

    return render_template("index.html")

@main_bp.route("/access")
def access():
    return render_template("access.html")
from flask import Blueprint, render_template, redirect, request, flash, session
import json
import os

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    return 
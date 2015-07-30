from piewhole import piewhole
from flask import render_template
from flask import flash
from flask.ext.login import login_user
from flask.ext.login import login_required
from flask.ext.login import current_user
from flask.ext.login import logout_user
from werkzeug.security import check_password_hash
from .models import User

@piewhole.route("/")
def index():
    return render_template("intro.html")

@piewhole.route("/login")
def login():
    return render_template("intro.html")

@piewhole.route("/food")
@login_required
def fooddiary():
    return render_template("intro.html")

@piewhole.route("/weight")
def weightinfo():
    return render_template("intro.html")

@piewhole.route("/profile")
def userprofile():
    return render_template("intro.html")
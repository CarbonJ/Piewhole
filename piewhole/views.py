from piewhole import piewhole
from flask import render_template

@piewhole.route("/")
def index():
    return render_template("intro.html")

@piewhole.route("/login")
def login():
    return render_template("intro.html")

@piewhole.route("/food")
def fooddiary():
    return render_template("intro.html")

@piewhole.route("/weight")
def weightinfo():
    return render_template("intro.html")

@piewhole.route("/profile")
def userprofile():
    return render_template("intro.html")
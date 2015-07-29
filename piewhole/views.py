from piewhole import piewhole
from flask import render_template

@piewhole.route("/")
def index():
    return render_template("intro.html")

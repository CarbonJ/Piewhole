from piewhole import piewhole

from .database import session
from .models import User

from flask import render_template
from flask import request, redirect, url_for
from flask import flash

from flask.ext.login import login_user
from flask.ext.login import login_required
from flask.ext.login import current_user
from flask.ext.login import logout_user
from werkzeug.security import check_password_hash




@piewhole.route("/")
def index():
    return render_template("intro.html")

@piewhole.route("/login", methods=['GET'])
def login():
    return render_template("login.html")

@piewhole.route("/login", methods=['POST'])
def login_post():
    print(request.form['email'])
    email = request.form['email']
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Incorrect user name or password', 'danger')
        return redirect(url_for('login'))

    login_user(user)
    return redirect(url_for('index'))

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
from piewhole import piewhole

from .database import session
from .models import User

from flask import render_template
from flask import request, redirect, url_for
from flask import flash
from werkzeug.security import check_password_hash
from flask.ext.login import login_user
from flask.ext.login import login_required
from flask.ext.login import current_user
from flask.ext.login import logout_user

@piewhole.route("/")
def index():
    return render_template("intro.html")

@piewhole.route("/login", methods=['GET'])
def login():
    return render_template("login.html")

@piewhole.route("/login", methods=['POST'])
def login_post():
    print('form_email: {}'.format(request.form['email']))
    print('form_password: {}'.format(request.form['password']))

    email = request.form['email']
    password = request.form['password']
    user = session.query(User).filter_by(email=email).first()
    print('User: {}'.format(user))
    print('User ID: {}'.format(user.id))
    print('Username: {}'.format(user.username))
    print('User password: {}'.format(user.password))
    if not user or not check_password_hash(user.password, password):
        print('No user found')
        flash('Incorrect user name or password', 'danger')
        return redirect(url_for('login'))

    login_user(user)
    return redirect(url_for('index'))

@piewhole.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@piewhole.route("/food")
@login_required
def fooddiary():
    return render_template("intro.html")

@piewhole.route("/weight")
@login_required
def weightinfo():
    return render_template("intro.html")

@piewhole.route("/profile")
@login_required
def userprofile():
    return render_template("intro.html")
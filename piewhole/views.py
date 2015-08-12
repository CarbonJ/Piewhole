from piewhole import piewhole

from .database import session
from .models import Users, Goals, Food

from flask import render_template
from flask import request, redirect, url_for
from flask import flash
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask.ext.login import login_user
from flask.ext.login import login_required
from flask.ext.login import current_user
from flask.ext.login import logout_user


from validate_email import validate_email

@piewhole.route("/")
def index():
    return render_template("intro.html")

@piewhole.route('/register', methods=['GET'])
def register_user_get():
    return render_template('register.html')

@piewhole.route('/register', methods=['POST'])
def register_user_post():
    username = request.form['username']
    email = request.form['email'].lower()
    password1 = request.form['password1']
    password2 = request.form['password2']

    user = session.query(Users).filter_by(email=email).first()

    if user:
        print('Email already exists')
        flash('A user already exists with that email address', 'danger')
        return redirect(url_for('register_user_get'))
    else:
        print('No pre-existing user found')
        if validate_email(email) == True:
            print('check if password match')
            if password1 == password2:
                print('passwords good')
                user = Users(username=username, email=email, password=generate_password_hash(password1))
                session.add(user)
                session.commit()
                login_user(user, remember=True)
                return redirect(url_for('fooddiary'))
            else:
                flash('passwords dont match', 'warning')
                return render_template("register.html")
            return render_template("login.html")
        else:
            print('Bad email')
            flash('Bad email', 'warning')
            return render_template("register.html")


@piewhole.route("/login", methods=['GET'])
def login():
    return render_template("login.html")

@piewhole.route("/login", methods=['POST'])
def login_post():
    # TODO: add check if email not in write format
    #print('form_email: {}'.format(request.form['email']))
    #print('form_password: {}'.format(request.form['password']))

    email = request.form['email']
    password = request.form['password']
    user = session.query(Users).filter_by(email=email).first()
    #print('User: {}'.format(user))
    #print('User ID: {}'.format(user.id))
    #print('Username: {}'.format(user.username))
    #print('User password: {}'.format(user.password))
    if not user or not check_password_hash(user.password, password):
        print('No user found')
        flash('Incorrect user name or password', 'danger')
        return redirect(url_for('login'))

    login_user(user)
    return redirect(url_for('profile'))

@piewhole.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@piewhole.route("/food")
@login_required
def fooddiary():
    return render_template("food.html")

@piewhole.route("/food")
@login_required
def fooddiary_post():
    return render_template("food.html")


@piewhole.route("/weight")
@login_required
def weightinfo():
    return render_template("weight.html")

@piewhole.route("/profile", methods=['GET'])
@login_required
def profile():
    print('-- GET: Profile page rendered. --')
    print('GET - User: {}'.format(current_user.username))
    print('GET - ID: {}'.format(current_user.id))

    u = session.query(Users).filter_by(id=current_user.id).first()
    print('GET - Queried User: {}'.format(u.username))

    goal = session.query(Goals).filter_by(user_id=current_user.id).first()

    if goal:
        wtg = goal.weight_goal
        gdg = (goal.health_goal * 100)
        print('GET - Goal Weight: {}'.format(wtg))
        print('GET - Goal Health: {}'.format(gdg))
    else:
        flash('Please enter a weight and health goal.', 'warning')
        wtg = 0
        gdg = 0

    return render_template("profile.html", weightgoal=wtg, healthgoal=gdg)

@piewhole.route("/profile", methods=['POST'])
@login_required
def profile_post():

    def update_goal():
        print('POST USER: {}'.format(current_user.username))
        print('POST WG: {}'.format(request.form['weightgoal']))
        print('POST HG: {}'.format(request.form['goodgoal']))


    if request.form['submit'] == 'user':
        print('-- POST: User section submitted --')
    elif request.form['submit'] == 'goal':
        print('-- POST: Goal section submitted --')
        update_goal()
    elif request.form['submit'] == 'password':
        print('-- POST: Password section submitted --')
    else:
        print('what the hell button as pushed?')


    try:
        weightgoal = request.form['weightgoal']
        goodgoal = (float(request.form['goodgoal']) * .01)
        # print('Weight Goal: {}'.format(weightgoal))
        # print('Health Goal: {}'.format(goodgoal))

        print('Trying to make changes')
        testweight = session.query(Goals).filter_by(user_id=current_user.id).first()

        if not testweight:
            if weightgoal and goodgoal > 0:
                print("goals don't exist")
                print('POST WG: {}'.format(weightgoal))
                print('POST HG: {}'.format(goodgoal))
                newgoals = Goals(user_id=current_user.id, weight_goal=weightgoal, health_goal=goodgoal)
                print(newgoals)
                session.add(newgoals)
                session.commit()
                print("commit done")
                return redirect(url_for('profile'))

                #return render_template("profile.html")
            else:
                flash('Need both a weight goal and health percentage.', 'danger')
        else:
            print('weight existings, update')
            session.query(Goals).filter_by(user_id=current_user.id).update({"weight_goal": weightgoal})
            session.query(Goals).filter_by(user_id=current_user.id).update({"health_goal": goodgoal})
            session.commit()
    except (ValueError) as error:
        print('Failed: {}'.format(error))

    return redirect(url_for('profile'))

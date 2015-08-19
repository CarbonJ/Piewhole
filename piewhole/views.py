import logging
import datetime

import pygal
from pygal.style import Style
from pygal import Config
from flask_table import Table, Col
from piewhole import piewhole

from .database import session
from .models import Users, Goals, Food, Ranks, Weight
from sqlalchemy import desc

from flask import render_template
from flask import request, redirect, url_for
from flask import flash
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask.ext.login import login_user
from flask.ext.login import login_required
from flask.ext.login import current_user
from flask.ext.login import logout_user
from flask_table import Table, Col

from validate_email import validate_email

logging.basicConfig(filename="piewhole.log", level=logging.DEBUG)


class FoodTable(Table):
    '''Column configuration for food entries'''
    classes = ["table table-striped"]
    food = Col('Food Entry')
    food_date = Col('Date')
    rankdesc = Col('Rank')


class WeightTable(Table):
    '''Column configuration for weight entries'''
    classes = ["table table-striped"]
    weight = Col('Weight Entry')
    weight_date = Col('Date')


def myround(num):
    return(round(num * (10**2)) / float(10**2))


def genweightchart():
    '''Generate weight chart with Pygal'''
    weighthistory = session.query(Weight) \
        .filter_by(user_id=current_user.id) \
        .order_by(Weight.id.desc()) \
        .all()

    maxweight = session.query(Weight) \
        .filter_by(user_id=current_user.id) \
        .order_by(Weight.id.desc()) \
        .first()

    if maxweight is None:
        maxrange = 100
    else:
        maxrange = (int(maxweight.weight) + 50)

    custom_style = Style(
                background='transparent',
                value_font_size=24,
                title_font_size=36,
                margin=1,
                plot_background='transparent',
                foreground='#53E89B',
                foreground_strong='#53A0E8',
                foreground_subtle='#630C0D',
                opacity='.6',
                opacity_hover='.9',
                transition='400ms ease-in',
                colors=('#5cb85c', '#f0ad4e', '#d9534f'))
    config = Config()
    config.show_legend = True
    config.legend_at_bottom=True
    config.y_labels = range(0, maxrange, 25)
    config.human_readable = True
    config.fill = True
    config.style=custom_style
    config.print_labels=True
    config.no_data_text='Add weight measurements!'

    wlist = []
    for entry in enumerate(weighthistory):
        wlist.append(entry[1].weight)

    line_chart = pygal.Line(config)
    line_chart.title = "Weight History"
    line_chart.add('Values', wlist)
    chart = line_chart.render(is_unicode=True)
    return chart

def genfoodchart():
    '''Generate food chart with Pygal'''
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    goodcount = session.query(Food) \
        .filter_by(user_id=current_user.id) \
        .filter_by(food_date=now).join(Ranks) \
        .filter_by(rank=1).add_columns(Ranks.rank).count()
    okaycount = session.query(Food) \
        .filter_by(user_id=current_user.id) \
        .filter_by(food_date=now).join(Ranks) \
        .filter_by(rank=2).add_columns(Ranks.rank).count()
    badcount = session.query(Food) \
        .filter_by(user_id=current_user.id) \
        .filter_by(food_date=now).join(Ranks) \
        .filter_by(rank=3).add_columns(Ranks.rank).count()

    custom_style = Style(
                    background='transparent',
                    value_font_size=24,
                    title_font_size=36,
                    margin=1,
                    plot_background='transparent',
                    foreground='#53E89B',
                    foreground_strong='#53A0E8',
                    foreground_subtle='#630C0D',
                    opacity='.6',
                    opacity_hover='.9',
                    transition='400ms ease-in',
                    colors=('#5cb85c', '#f0ad4e', '#d9534f'))

    config = Config()
    config.show_legend = True
    config.legend_at_bottom=True
    config.legend_at_bottom_columns=1
    config.legend_box_size=10
    config.human_readable = True
    config.fill = True
    config.style=custom_style
    config.print_labels=True
    config.print_values=True
    config.no_data_text='Need to add some food!'

    pie_chart = pygal.Pie(config)
    pie_chart.title = "Current Food Stats"
    pie_chart.add('Good', goodcount)
    pie_chart.add('Okay', okaycount)
    pie_chart.add('Bad', badcount)
    chart = pie_chart.render(is_unicode=True)
    return chart

@piewhole.route("/")
def index():
    '''Route to index page'''
    return render_template("intro.html")

@piewhole.route('/register', methods=['GET'])
def register_user_get():
    '''Route to registration page'''
    return render_template('register.html')

@piewhole.route('/register', methods=['POST'])
def register_user_post():
    '''Register a new user.  Ensure email is valid and not already in use.'''
    #Rollback any old/stale transaction
    session.rollback()

    username = request.form['username']
    email = request.form['email'].lower()
    password1 = request.form['password1']
    password2 = request.form['password2']
    user = session.query(Users).filter_by(email=email).first()
    logging.debug("REGISTER_USER_POST: username = '{}' ".format(username))
    logging.debug("REGISTER_USER_POST: email = '{}' ".format(email))

    if user:
        logging.info("REGISTER_USER_POST: '{}' already exists, warning user".format(email))
        flash('A user already exists with that email address, please re-enter a new', 'danger')
        return redirect(url_for('register_user_get'))
    else:
        logging.info("REGISTER_USER_POST: attempting to create '{}'".format(email))
        if validate_email(email) == True:
            if password1 == password2:
                logging.debug("REGISTER_USER_POST: user '{}' passwords match".format(email))
                user = Users(username=username, \
                            email=email, \
                            password=generate_password_hash(password1))
                session.add(user)
                session.commit()
                login_user(user, remember=True)
                logging.info("REGISTER_USER_POST: user '{}' created".format(email))
                return redirect(url_for('profile'))
            else:
                flash("Passwords don't match, please try again.", 'warning')
                return render_template("register.html")
            return render_template("login.html")
        else:
            logging.info("REGISTER_USER_POST: '{}' is a'bad' email, warning user".format(email))
            flash('Incorrect email format entered, please try again.', 'warning')
            return render_template("register.html")


@piewhole.route("/login", methods=['GET'])
def login():
    '''Route to login page'''
    return render_template("login.html")

@piewhole.route("/login", methods=['POST'])
def login_post():
    '''Authenticate user'''
    email = request.form['email']
    password = request.form['password']
    user = session.query(Users).filter_by(email=email).first()
    logging.debug("LOGIN_POST: email = '{}' ".format(email))

    if not user or not check_password_hash(user.password, password):
        logging.info("LOGIN_POST: '{}' can't login, warning user".format(email))
        flash('Incorrect user name or password', 'danger')
        return redirect(url_for('login'))

    login_user(user)

    existinggoal = session.query(Goals).filter_by(user_id=current_user.id).first()

    if existinggoal:
        return redirect(url_for('fooddiary'))
    else:
        return redirect(url_for('profile'))

@piewhole.route('/logout')
def logout():
    '''Logout user'''
    logout_user()
    return redirect(url_for('index'))

@piewhole.route("/food", methods=['GET'])
@login_required
def fooddiary():
    '''Quick entry food to food diary'''
    now = datetime.datetime.now().strftime("%Y-%m-%d")

    items = session.query(Food) \
        .filter_by(user_id=current_user.id) \
        .filter_by(food_date=now) \
        .join(Ranks) \
        .add_columns(Food.food, Food.food_date, Ranks.rankdesc) \
        .order_by(Food.id.desc()).all()

    table = FoodTable(items)

    #Generate chart for page load
    chart = genfoodchart()

    return render_template("food.html", table=table, chart=chart)

@piewhole.route("/food", methods=['POST'])
@login_required
def fooddiary_post():
    ''' Add to food diary'''
    session.rollback()
    food = request.form['quickentry']
    now = datetime.datetime.now().strftime("%Y-%m-%d")

    items = session.query(Food) \
        .filter_by(user_id=current_user.id) \
        .filter_by(food_date=now).join(Ranks) \
        .add_columns(Food.food, Food.food_date, Ranks.rankdesc) \
        .order_by(Food.id.desc()).all()
    table = FoodTable(items)

    def update_food(food, rank, user_id, date):
        rank = session.query(Ranks).filter_by(rank=rank).first()
        newfood = Food(food=food, food_date=now, rank_id=rank.id, user_id=current_user.id)
        session.add(newfood)
        session.commit()

    if request.form['submit'] == 'good':
        update_food(food, 1, current_user.id, now)
    elif request.form['submit'] == 'ok':
        update_food(food, 2, current_user.id, now)
    elif request.form['submit'] == 'bad':
        update_food(food, 3, current_user.id, now)
    else:
        logging.info("PROFILE_POST: Unknown submision made, no registered button")

    return redirect(url_for('fooddiary', table=table))


@piewhole.route("/weight", methods=['GET'])
@login_required
def weightinfo():
    ''' Get weight info'''
    # now = datetime.datetime.now().strftime("%Y-%m-%d")

    goals = session.query(Goals) \
        .filter_by(user_id=current_user.id) \
        .first()
    weight = session.query(Weight) \
        .filter_by(user_id=current_user.id) \
        .order_by(Weight.id.desc()) \
        .first()

    if goals is None:
        weightgoal = 0
    else:
        weightgoal = goals.weight_goal

    if weight is None:
        currentweight = 0
    else:
        currentweight = weight.weight

    delta = currentweight - weightgoal

    if delta > 0:
        delta = delta
    else:
        delta = 0

    entries = session.query(Weight) \
        .filter_by(user_id=current_user.id) \
        .order_by(Weight.id.desc()) \
        .all()
    table = WeightTable(entries)
    chart = genweightchart()

    return render_template("weight.html", goal=weightgoal, \
                            weight=currentweight, delta=myround(delta), table=table, chart=chart)

@piewhole.route("/weight", methods=['POST'])
@login_required
def weightinfo_post():
    ''' Update weight info '''
    session.rollback()
    weight = request.form['quickentry']
    now = datetime.datetime.now().strftime("%Y-%m-%d")

    newweight = Weight(weight=weight, weight_date=now, user_id=current_user.id)

    session.add(newweight)
    session.commit()

    return redirect(url_for('weightinfo'))

@piewhole.route("/profile", methods=['GET'])
@login_required
def profile():
    '''
    Get user profile details, provide temp values as needed
    '''
    # u = session.query(Users).filter_by(id=current_user.id).first()
    goal = session.query(Goals).filter_by(user_id=current_user.id).first()

    if goal:
        wtg = goal.weight_goal
        gdg = (goal.health_goal * 100)
    else:
        flash('Please enter a weight and health goal.', 'warning')
        wtg = 0
        gdg = 0

    return render_template("profile.html", weightgoal=wtg, healthgoal=gdg)

@piewhole.route("/profile", methods=['POST'])
@login_required
def profile_post():
    '''
    Updates a user's profile via (user details, goals, and password)
    '''
    session.rollback()

    def update_goal():
        weightgoal = request.form['weightgoal']

        try:
            goodgoal = (float(request.form['goodgoal']) * .01)
        except (ValueError) as error:
            logging.debut('PROFILE_POST: Failed weight update with error {}'.format(error))
            flash('Need weight and health in number format.', 'danger')
            return

        testweight = session.query(Goals).filter_by(user_id=current_user.id).first()

        if not testweight:
            if weightgoal and goodgoal > 0:
                newgoals = Goals(user_id=current_user.id, weight_goal=weightgoal, health_goal=goodgoal)
                session.add(newgoals)
                session.commit()
                return redirect(url_for('profile'))
            else:
                flash('Need both a weight goal and health percentage.', 'danger')
        else:
            session.query(Goals) \
                .filter_by(user_id=current_user.id) \
                .update({"weight_goal": weightgoal})
            session.query(Goals).filter_by(user_id=current_user.id).update({"health_goal": goodgoal})
            session.commit()


    def update_user():
        username = request.form['username']
        email = request.form['email']

        emailtest = session.query(Users).filter_by(email=email).first()

        if emailtest and email != current_user.email:
            flash('That email address is already in use.', 'danger')
        else:
            session.query(Users).filter_by(id=current_user.id).update({"username": username})
            session.query(Users).filter_by(id=current_user.id).update({"email": email})
            session.commit()

    def update_password():
        pwd = request.form['originalpassword']
        pw1 = request.form['password1']
        pw2 = request.form['password2']

        user = session.query(Users).filter_by(id=current_user.id).first()

        if user and check_password_hash(user.password, pwd):
            if pw1 == pw2:
                session.query(Users) \
                .filter_by(id=current_user.id) \
                .update({'password': generate_password_hash(pw1)})
                session.commit()
            else:
                flash('The new passwords do not match, please try again.', 'warning')
        else:
            flash('Incorrect password.', 'danger')


    if request.form['submit'] == 'user':
        logging.debug("PROFILE_POST: userid {} changed user details".format(current_user.id))
        update_user()
    elif request.form['submit'] == 'goal':
        logging.debug("PROFILE_POST: userid {} changed goal details".format(current_user.id))
        update_goal()
    elif request.form['submit'] == 'password':
        logging.debug("PROFILE_POST: userid {} changed passwrd details".format(current_user.id))
        update_password()
    else:
        logging.info("PROFILE_POST: Unknown submision made, no registered button")

    return redirect(url_for('profile'))

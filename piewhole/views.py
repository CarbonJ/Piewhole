import datetime
from flask_table import Table, Col
from piewhole import piewhole

from .database import session
from .models import Users, Goals, Food, Ranks
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

class ItemTable(Table):
    classes = ["table table-striped"]
    food = Col('Food Entry')
    food_date = Col('Date')
    #rank_id = Col('Rank')
    rankdesc = Col('Rank')

class Item(object):
    def __init__(self, entry, date, rank):
        self.entry = entry
        self.date = date
        self.rank = rank


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

@piewhole.route("/food", methods=['GET'])
@login_required
def fooddiary():
    now = datetime.datetime.now().strftime("%Y-%m-%d")

    print('-- GET: Food page rendered. --')
    print('GET - User: {}'.format(current_user.username))
    print('GET - ID: {}'.format(current_user.id))


#     q = (session.query(Group, Member, Item, Version)
#         .join(Member)
#         .join(Item)
#         .join(Version)
#         .filter(Version.name == my_version)
#         .order_by(Group.number)
#         .order_by(Member.number)
#         ).all()
# print_tree(q)

    items = session.query(Food).filter_by(user_id=current_user.id).filter_by(food_date=now).join(Ranks).add_columns(Food.food, Food.food_date, Ranks.rankdesc).order_by(Food.id.desc()).all()

    table = ItemTable(items)
    print(table)
    # print(table.__html__())


    return render_template("food.html", table=table)

@piewhole.route("/food", methods=['POST'])
@login_required
def fooddiary_post():
    food = request.form['quickentry']
    now = datetime.datetime.now().strftime("%Y-%m-%d")

    items = session.query(Food).filter_by(user_id=current_user.id).filter_by(food_date=now).join(Ranks).add_columns(Food.food, Food.food_date, Ranks.rankdesc).order_by(Food.id.desc()).all()
    table = ItemTable(items)

    print('-- POST: Food page rendered. --')
    print('POST - User: {}'.format(current_user.username))
    print('POST - ID: {}'.format(current_user.id))
    print('POST - Food: {}'.format(request.form['quickentry']))


    def update_food(food, rank, user_id, date):
        rank = session.query(Ranks).filter_by(rank=rank).first()

        print('POST - in update_food function')
        print("POST - Trying {} for date".format(date))
        print("POST - Trying {} for food".format(food))
        print("POST - Trying '{}' for rank".format(rank.rankdesc))

        newfood = Food(food=food, food_date=now, rank_id=rank.id, user_id=current_user.id)
        session.add(newfood)
        session.commit()

    if request.form['submit'] == 'good':
        print('-- POST: Good food submitted --')
        update_food(food, 1, current_user.id, now)
    elif request.form['submit'] == 'ok':
        print('-- POST: Okay food submitted --')
        update_food(food, 2, current_user.id, now)
    elif request.form['submit'] == 'bad':
        print('-- POST: Bad food submitted --')
        update_food(food, 3, current_user.id, now)
    else:
        print('What the hell button as pushed?')

    return redirect(url_for('fooddiary', table=table))
    # return render_template("food.html", table=table)


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

        weightgoal = request.form['weightgoal']

        try:
            goodgoal = (float(request.form['goodgoal']) * .01)
        except (ValueError) as error:
            print('Failed: {}'.format(error))
            flash('Need weight and health in number format.', 'danger')
            return

        print('POST: Trying to make changes')
        testweight = session.query(Goals).filter_by(user_id=current_user.id).first()

        if not testweight:
            if weightgoal and goodgoal > 0:
                print('POST: New goals, so inserting.')
                print('POST WG: {}'.format(weightgoal))
                print('POST HG: {}'.format(goodgoal))
                newgoals = Goals(user_id=current_user.id, weight_goal=weightgoal, health_goal=goodgoal)
                print(newgoals)
                session.add(newgoals)
                session.commit()
                print("POST: Commit done")
                return redirect(url_for('profile'))
            else:
                flash('Need both a weight goal and health percentage.', 'danger')
        else:
            print('POST: Goals already exists, so updating.')
            session.query(Goals).filter_by(user_id=current_user.id).update({"weight_goal": weightgoal})
            session.query(Goals).filter_by(user_id=current_user.id).update({"health_goal": goodgoal})
            session.commit()


    def update_user():
        print('POST USER: {}'.format(current_user.username))
        print('POST USERFORM: {}'.format(request.form['username']))
        print('POST EMAILFORM: {}'.format(request.form['email']))

        username = request.form['username']
        email = request.form['email']

        emailtest = session.query(Users).filter_by(email=email).first()

        if emailtest and email != current_user.email:
            flash('That email address is already in use.', 'danger')
        else:
            print('POST: Trying to make changes')
            session.query(Users).filter_by(id=current_user.id).update({"username": username})
            session.query(Users).filter_by(id=current_user.id).update({"email": email})
            session.commit()
            print('POST: Changes commited')

    def update_password():
        print('POST USER: {}'.format(current_user.username))

        pwd = request.form['originalpassword']
        pw1 = request.form['password1']
        pw2 = request.form['password2']

        user = session.query(Users).filter_by(id=current_user.id).first()

        if user and check_password_hash(user.password, pwd):
            if pw1 == pw2:
                print('POST: New passwords good.')
                session.query(Users).filter_by(id=current_user.id).update({'password': generate_password_hash(pw1)})
                session.commit()
            else:
                flash('The new passwords do not match, please try again.', 'warning')
        else:
            flash('Incorrect password.', 'danger')


    if request.form['submit'] == 'user':
        print('-- POST: User section submitted --')
        update_user()
    elif request.form['submit'] == 'goal':
        print('-- POST: Goal section submitted --')
        update_goal()
    elif request.form['submit'] == 'password':
        print('-- POST: Password section submitted --')
        update_password()
    else:
        print('What the hell button as pushed?')

    return redirect(url_for('profile'))

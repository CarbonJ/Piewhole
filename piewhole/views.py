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
    email = request.form['email'].upper()
    password1 = request.form['password1']
    password2 = request.form['password2']

    user = session.query(Users).filter_by(email=email).first()
    if user is None:
        print('bad"')

    #FIX FIX FIX
    # IF USER

    if validate_email(email) == True:
        print('submitted email valid')
        #user = session.query(User).filter_by(email=email).first()
        if user.email.upper() == email.upper():
            print('Email already exists')
            flash('A user already exists with that email address', 'danger')
            return redirect(url_for('register_user_get'))
        else:
            print('build account')
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

@piewhole.route("/weight")
@login_required
def weightinfo():
    return render_template("weight.html")

@piewhole.route("/profile", methods=['GET'])
@login_required
def profile():
    print('GET USER: {}'.format(current_user.username))
    goal = session.query(Goals).filter_by(id=current_user.id).first()
    wtg = goal.weight_goal
    hlg = goal.health_goal
    print('GET WGT: {}'.format(wtg))
    print('GET WGT: {}'.format(hlg))

    return render_template("profile.html", weightgoal=wtg)

@piewhole.route("/profile", methods=['POST'])
@login_required
def profile_post():
    print('POST: {}'.format(current_user.username))
    weightgoal = request.form['weightgoal']
    print('Weight Goal: {}'.format(weightgoal))

    session.query(Goals).filter_by(id=current_user.id).update({"weight_goal": weightgoal})
    session.commit()

    return render_template("profile.html")


# class Goals(Base):
#     __tablename__ = 'Goals'
#     id = Column(Integer, primary_key=True, unique=True)
#     user_id = Column(Integer, ForeignKey('User.id'))
#     weight_goal = Column(Float)
#     health_goal = Column(Float)

# content = mistune.markdown(request.form["content"])

#     session.query(Post).filter_by(id=postid).update(
#         {"title": title, "content": content})
#     session.commit()
#     return redirect(url_for("posts"))
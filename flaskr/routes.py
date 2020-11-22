import atexit
from flask import current_app as app

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required

from flaskr.forms import LoginForm
from flaskr.models import db, User, Setup
from flaskr.rover import Rover as rover
from flaskr import rover_controller

view = Blueprint("view", __name__)

rover_controller.gpioSetup()

@view.route("/", methods=["GET", "POST"])
def homepage():
    if current_user.is_authenticated:
    
        commandRequest = request.form.get('command')
        if commandRequest != None :
            execute_command('CHANGE_STATUS', commandRequest)
        
        powerSlider = request.form.get('powerSlider')
        if powerSlider != None :
            execute_command('CHANGE_POWER', powerSlider)
        
        setup = Setup.query.filter_by(id=1).first()
        return render_template("homepage.html", user=current_user, setup=setup, rover_controller=rover_controller)

    return redirect(url_for('view.login'))

@view.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('view.homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            msg = "Invalid credentials"
            flash(msg)
            return redirect(url_for('view.login'))
        elif user.enabled == 0:
            msg = "User disabled"
            flash(msg)
            return redirect(url_for('view.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('view.homepage'))
    return render_template("login.html", form=form)

@view.route("/logout")
def logout():
    logout_user()
    rover_controller.cleanUp()
    return redirect(url_for('view.homepage'))

@view.route("/users")
@login_required
def users():
    if not current_user.role == 'ADMIN':
        return render_template("homepage.html")
    users = User.query.all()
    return render_template("users.html", users=users)

@view.route("/setup")
@login_required
def setup():
    if not current_user.role == 'ADMIN':
        return render_template("homepage.html")
    setup = Setup.query.filter_by(id=1).first()
    return render_template("setup.html", setup=setup)

@view.route("/new")
@login_required
def new():
    if not current_user.role == 'ADMIN':
        return render_template("homepage.html")    
    return render_template('new.html')

@view.route("/edit/<int:id>")
@login_required
def edit(id):
    if not current_user.role == 'ADMIN':
        return render_template("homepage.html")
    user = User.query.filter_by(id=id).first()
    return render_template("edit.html", user=user)

@view.route("/remove/<int:id>")
@login_required
def remove(id):
    if not current_user.role == 'ADMIN':
        return render_template("homepage.html")
    user = User.query.filter_by(id=id).first()
    return render_template("remove.html", user=user)

@view.route("/add_user", methods=["POST"])
@login_required
def add_user():
    if not current_user.role == 'ADMIN':
        return render_template("homepage.html")
    try:
        username = request.form.get("username")        
        password = request.form.get("password")
        role = request.form.get("role")
        email = request.form.get("email")
        enabled = request.form.get("enabled")
        user = User(username=username)
        user.set_password_hash(password)
        user.role = role
        user.email = email
        user.enabled = 0
        if enabled == 'on':
            user.enabled = 1
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        msg = "Failed to add user {}".format(username)
        flash(msg)
        return redirect("/new")
    return redirect("/users")

@view.route("/update_user", methods=["POST"])
@login_required
def update_user():
    if not current_user.role == 'ADMIN':
        return render_template("homepage.html")
    try:
        newUsername = request.form.get("newUsername")
        oldUsername = request.form.get("oldUsername")
        password = request.form.get("password")
        oldPassword = request.form.get("oldPassword")
        role = request.form.get("role")
        email = request.form.get("email")
        enabled = request.form.get("enabled")
        user = User.query.filter_by(username=oldUsername).first()
        user.username = newUsername
        if oldPassword != password:
            user.set_password_hash(password)
        user.role = role
        user.email = email
        user.enabled = 0
        if enabled == 'on':
            user.enabled = 1
        db.session.commit()
    except Exception as e:
        msg = "Failed to update user {}".format(oldUsername)
        flash(msg)
        return redirect("/edit")
    return redirect("/users")

@view.route("/delete", methods=["POST"])
@login_required
def delete():
    if not current_user.role == 'ADMIN':
        return render_template("homepage.html")
    try:
        username = request.form.get("username")
        user = User.query.filter_by(username=username).first()
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        msg = "Failed to delete user {}".format(username)
        flash(msg)
    return redirect("/users")

@view.route("/save_setup", methods=["POST"])
@login_required
def save_setup():
    if not current_user.role == 'ADMIN':
        return render_template("homepage.html")
    try:
        camera_ip = request.form.get("camera_ip")
        gps_interval = request.form.get("gps_interval")
        gps_store = request.form.get("gps_store")
        stop_on_lost_connection_interval = request.form.get("stop_on_lost_connection_interval")

        setup = Setup.query.filter_by(id=1).first()
        setup.camera_ip = camera_ip
        setup.gps_interval = int(gps_interval)
        setup.gps_store = 0
        if gps_store == 'on':
            setup.gps_store = 1
        setup.stop_on_lost_connection_interval = int(stop_on_lost_connection_interval)

        db.session.commit()
        msg = "Setup successfully saved"
        flash(msg)
    except Exception as e:
        msg = "Failed to save setup"
        flash(msg)
    return redirect("/setup")

def execute_command(command, value): 
    print('Command:{0} Value:{1}'.format(command, value))
    if (command == 'CHANGE_STATUS'):
        if (value == 'STOP'):
            rover_controller.stopMotors()
            rover_controller.rover.status = value
        elif (value == 'FORWARD'):
            rover_controller.stopMotors()
            rover_controller.setLeftMotorsDirection(value)
            rover_controller.setRightMotorsDirection(value)
            rover_controller.startMotors()
            rover_controller.rover.status = value
        elif (value == 'BACKWARD'):
            rover_controller.stopMotors() 
            rover_controller.setLeftMotorsDirection(value)
            rover_controller.setRightMotorsDirection(value)
            rover_controller.startMotors()
            rover_controller.rover.status = value
        elif (value == 'CLOCKWISE'):
            rover_controller.stopMotors() 
            rover_controller.setLeftMotorsDirection('FORWARD')
            rover_controller.setRightMotorsDirection('BACKWARD')
            rover_controller.startMotors()
            rover_controller.rover.status = value
        elif (value == 'COUNTER-CLOCKWISE'):
            rover_controller.stopMotors()
            rover_controller.setLeftMotorsDirection('BACKWARD')
            rover_controller.setRightMotorsDirection('FORWARD')
            rover_controller.startMotors()
            rover_controller.rover.status = value
    elif (command == 'CHANGE_POWER'):
        rover_controller.setPower(int(value))
    else:
        print('Unknown command')

# Safe terminating
def cleanUp():  
    print('Safe terminating')
    rover_controller.cleanUp()

atexit.register(cleanUp)

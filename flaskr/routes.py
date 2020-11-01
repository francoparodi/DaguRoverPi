from flask import current_app as app

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required

from flaskr.forms import LoginForm
from flaskr.models import db, User, Setup

view = Blueprint("view", __name__)

@view.route("/")
def homepage():
    if current_user.is_authenticated:
        setup = Setup.query.filter_by(id=1).first()
        return render_template("homepage.html", user=current_user, setup=setup)
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
        print(e)
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
        print(e)
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
        print(e)
    return redirect("/users")

@view.route("/save_setup", methods=["POST"])
@login_required
def save_setup():
    if not current_user.role == 'ADMIN':
        return render_template("homepage.html")
    try:
        camera_enabled = request.form.get("camera_enabled")
        setup = Setup.query.filter_by(id=1).first()
        setup.camera_enabled = 0
        if camera_enabled == 'on':
            setup.camera_enabled = 1
        db.session.commit()
    except Exception as e:
        msg = "Failed to save setup"
        flash(msg)
        print(e)
        return redirect("/setup")
    return render_template("homepage.html", user=current_user, setup=setup)

import atexit, threading, time, string
from flask import current_app as app

from flask import Blueprint, render_template, redirect, url_for, flash, request, copy_current_request_context
from flask_login import current_user, login_user, logout_user, login_required

from flaskr.forms import LoginForm
from flaskr.models import db, User, Setup, GpsData
from flaskr.rover import Rover as rover
from flaskr import rover_controller, gps_controller

checkConnectionDaemonStopEvent = threading.Event()
GPSDaemonStopEvent = threading.Event()
isCheckConnectionDaemonStarted = False
isGPSDaemonStarted = False

checkConnectionDaemon = threading.Thread()
GPSDaemon = threading.Thread()

view = Blueprint("view", __name__)

rover_controller.gpioSetup()

@view.route("/clientConnected", methods=["GET", "POST"])
# end-point called by js post client
def clientConntected():
    if current_user.is_authenticated:
        setup = Setup.query.filter_by(id=1).first()
        clientConnected = request.form.get('clientConnected')
        if clientConnected == 'True' :
            log('Client status: connected (keep-alive received every {0}s.)'.format(setup.client_keepalive_interval))
            rover_controller.rover.clientConnected = True
        return render_template("homepage.html", user=current_user, setup=setup, rover_controller=rover_controller, gps_controller=gps_controller)

    return redirect(url_for('view.login'))

@view.route("/", methods=["GET", "POST"])
def homepage():
    if current_user.is_authenticated:
        setup = Setup.query.filter_by(id=1).first()
        startCheckConnectionDaemon()
        startGPSDaemon()
        commandRequest = request.form.get('command')
        if commandRequest != None :
            rover_controller.execute_command('CHANGE_STATUS', commandRequest)
        powerSlider = request.form.get('powerSlider')
        if powerSlider != None :
            rover_controller.execute_command('CHANGE_POWER', powerSlider)
        return render_template("homepage.html", user=current_user, setup=setup, rover_controller=rover_controller, gps_controller=gps_controller)

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
            flash(msg, category='warning')
            return redirect(url_for('view.login'))
        elif user.enabled == 0:
            msg = "User disabled"
            flash(msg, category='warning')
            return redirect(url_for('view.login'))
        
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('view.homepage'))
    
    return render_template("login.html", form=form)

@view.route("/logout")
def logout():
    logout_user()
    cleanUp()
    return redirect(url_for('view.login'))

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
    except Exception:
        msg = "Failed to add user {0}".format(username)
        flash(msg, category='danger')
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
    except Exception:
        msg = "Failed to update user {0}".format(oldUsername)
        flash(msg, category='danger')
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
    except Exception:
        msg = "Failed to delete user {0}".format(username)
        flash(msg, category='danger')

    return redirect("/users")

@view.route("/save_setup", methods=["POST"])
@login_required
def save_setup():
    if not current_user.role == 'ADMIN':
        return render_template("homepage.html")
    try:
        camera_ip = request.form.get("camera_ip")
        gps_interval = request.form.get("gps_interval")
        url_geomap = request.form.get("url_geomap")
        gps_store = request.form.get("gps_store")
        stop_on_lost_connection_interval = request.form.get("stop_on_lost_connection_interval")
        client_keepalive_interval = request.form.get("client_keepalive_interval")

        setup = Setup.query.filter_by(id=1).first()
        setup.camera_ip = camera_ip
        setup.gps_interval = int(gps_interval)
        setup.gps_store = int(gps_store)
        setup.url_geomap = url_geomap
        setup.stop_on_lost_connection_interval = int(stop_on_lost_connection_interval)
        setup.client_keepalive_interval = int(client_keepalive_interval)

        db.session.commit()
        msg = "Setup successfully saved"
        flash(msg, category='info')
    except Exception:
        msg = "Failed to save setup"
        flash(msg, category='danger')

    return redirect("/setup")

@view.route("/gpsdatalist")
@login_required
def gpsdatalist():
    if not current_user.role == 'ADMIN':
        return render_template("homepage.html")

    gpsdatalist = GpsData.query.all()
    return render_template("gpsdatalist.html", gpsdatalist=gpsdatalist)

@view.route("/deleteGpsData")
def deleteGpsData():
    try:
        db.session.query(GpsData).delete()
        db.session.commit()
        msg = "All GPS data successfully deleted"
        flash(msg, category='info')
    except Exception as e:
        msg = "Failed to delete GPS data"
        print(e)
        flash(msg, category='danger')
    return redirect("/gpsdatalist")

# Daemon to check client connection every 'interval' seconds, due to 'interval' setup value.
def startCheckConnectionDaemon():
    global isCheckConnectionDaemonStarted
    
    if isCheckConnectionDaemonStarted:
        return
    stop_on_lost_connection_interval = Setup.query.filter_by(id=1).first().stop_on_lost_connection_interval
    if stop_on_lost_connection_interval < 1:
        log('checkConnectionDaemon not startable due to interval value {0}s.'.format(stop_on_lost_connection_interval))
        return 

    @copy_current_request_context
    def checkConnectionDaemonProcess(name, checkConnectionDaemonStopEvent):
        while not checkConnectionDaemonStopEvent.is_set():
            stop_on_lost_connection_interval = Setup.query.filter_by(id=1).first().stop_on_lost_connection_interval
            log('checking client connection alive (every {0}s.)'.format(stop_on_lost_connection_interval))
            time.sleep(stop_on_lost_connection_interval)
            if not rover_controller.rover.clientConnected:
                log('client connection lost!')
                rover_controller.stopMotors()
            rover_controller.rover.clientConnected = False
    
    log('isCheckConnectionDaemonStarted: {0}'.format(isCheckConnectionDaemonStarted))

    if not isCheckConnectionDaemonStarted:
        checkConnectionDaemon.__init__(target=checkConnectionDaemonProcess, args=('CheckConnectionDaemon', checkConnectionDaemonStopEvent), daemon=True)
        checkConnectionDaemon.start()
        isCheckConnectionDaemonStarted = True
        log('isCheckConnectionDaemonStarted: {0}'.format(isCheckConnectionDaemonStarted))

def stopCheckConnectionDaemon():
    log('stopping CheckConnection daemon...')
    global isCheckConnectionDaemonStarted
    log('isCheckConnectionDaemonStarted: {0}'.format(isCheckConnectionDaemonStarted))
    if isCheckConnectionDaemonStarted:
        checkConnectionDaemonStopEvent.set()
        checkConnectionDaemon.join()
        checkConnectionDaemonStopEvent.clear()
        isCheckConnectionDaemonStarted = False
        log('isCheckConnectionDaemonStarted: {0}'.format(isCheckConnectionDaemonStarted))

# Daemon to get GPS position every 'interval' seconds, due to 'interval' setup value.
def startGPSDaemon():
    global isGPSDaemonStarted
    gps_interval = Setup.query.filter_by(id=1).first().gps_interval

    # Started but need to stop due to setup settings
    if isGPSDaemonStarted and gps_interval < 1:
        log('Stop GPSDaemon due to interval value {0}s.'.format(gps_interval))
        stopGPSDaemon()
        return

    # Not started and not startable
    if gps_interval < 1:
        log('GPSDaemon not startable due to interval value {0}s.'.format(gps_interval))
        return

    @copy_current_request_context
    def GPSDaemonProcess(name, GPSDaemonStopEvent):
        while not GPSDaemonStopEvent.is_set():
            gps_interval = Setup.query.filter_by(id=1).first().gps_interval
            log('retrieve GPS position (every {0}s.)'.format(gps_interval))
            gps_controller.gpsGetGPGGA()
            time.sleep(gps_interval)
            if not gps_controller.gps.online:
                log('GPS position not available, GPSOnline: {0}'.format(gps_controller.gps.online))
            else:
                gps_store = Setup.query.filter_by(id=1).first().gps_store
                if gps_store > -1:
                    url_geomap = Setup.query.filter_by(id=1).first().url_geomap
                    storeGpsData(gps_store, url_geomap)
    
    log('isGPSDaemonStarted: {0}'.format(isGPSDaemonStarted))

    if not isGPSDaemonStarted:
        GPSDaemon.__init__(target=GPSDaemonProcess, args=('GPSDaemon', GPSDaemonStopEvent), daemon=True)
        GPSDaemon.start()
        isGPSDaemonStarted = True
        gps_controller.gps.online = True
        log('isGPSDaemonStarted: {0}'.format(isGPSDaemonStarted))

def stopGPSDaemon():
    log('Stopping GPS daemon...')
    global isGPSDaemonStarted
    log('isGPSDaemonStarted: {0}'.format(isGPSDaemonStarted))
    gps_controller.gps.online = False
    if isGPSDaemonStarted:
        GPSDaemonStopEvent.set()
        GPSDaemon.join()
        GPSDaemonStopEvent.clear()
        isGPSDaemonStarted = False
        log('isGPSDaemonStarted: {0}'.format(isGPSDaemonStarted))


# Safe terminating
def cleanUp():  
    log('Safe terminating')
    stopCheckConnectionDaemon()
    stopGPSDaemon()
    rover_controller.cleanUp()
    gps_controller.cleanUp()

atexit.register(cleanUp)

# print
def log(msg):
    print(msg)

def storeGpsData(gps_store, url_geomap):
    # Clear data record if reached limits
    num_record = GpsData.query.count()
    if (gps_store < num_record):
        deleteGpsData()
    
    try:    
        gpsData = GpsData()
        gpsData.satellites = gps_controller.gps.satellites
        gpsData.gps_quality = gps_controller.gps.gpsQuality
        gpsData.altitude = gps_controller.gps.altitude
        lat_lon_degree = to_degrees(gps_controller.gps.latitude, gps_controller.gps.longitude)
        gpsData.latitude = lat_lon_degree[0] + gps_controller.gps.latitude_dir 
        gpsData.longitude = lat_lon_degree[1] + gps_controller.gps.longitude_dir
        gpsData.url = url_geomap.format(lat_lon_degree[0], lat_lon_degree[1]) 
        db.session.add(gpsData)
        db.session.commit()
    except Exception:
        log('Failed to save gpsData')

def to_degrees(lat, lon):
    lat_deg = lat[0:2]
    lat_mins = lat[2:]
    latitude = float(lat_deg) + (float(lat_mins)/60)

    lon_deg = lon[0:3]
    lon_mins = lon[3:]
    longitude = float(lon_deg) + (float(lon_mins)/60)

    return [latitude, longitude

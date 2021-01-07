from datetime import datetime

from flask_login import UserMixin, LoginManager
from werkzeug.security import check_password_hash, generate_password_hash

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    username = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.String(50), unique=False, default='USER')
    email = db.Column(db.String(50), unique=True, nullable=False)
    enabled = db.Column(db.Boolean, default=False, unique=False, nullable=False)
    password = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f"User('{ self.id }', '{ self.created_at }', '{ self.username }', '{ self.password }', '{ self.role }', '{ self.email }' , '{ self.enabled }')"

    def set_password_hash(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Setup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    camera_ip = db.Column(db.String(128), unique=False, default='')
    gps_interval = db.Column(db.Integer, default=0)
    gps_store = db.Column(db.Boolean, default=False, unique=False, nullable=False)
    stop_on_lost_connection_interval = db.Column(db.Integer, default=0)
    client_keepalive_interval = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"Setup('{ self.id }', '{ self.created_at }', '{ self.camera_enabled }', '{ self.gps_interval }')"

class GpsData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    satellites = db.Column(db.Integer, default=0)
    gps_quality = db.Column(db.Integer, default=0)
    altitude = db.Column(db.String(32), unique=False, default='')
    latitude = db.Column(db.String(32), unique=False, default='')
    longitude = db.Column(db.String(32), unique=False, default='')
    url = db.Column(db.String(512), unique=False, default='')
    
    def __repr__(self):
        return f"GpsData('{ self.id }', '{ self.created_at }', '{ self.satellites }', '{ self.gps_quality }', '{ self.altitude }', '{ self.latitude }', '{ self.longitude }' )"

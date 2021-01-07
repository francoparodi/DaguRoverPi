import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config, Logger
from flaskr.models import db, User, Setup, GpsData
from flaskr import create_app

try:
    log_type = "[SETUP]"
    message = 'Process started...'
    print('{0} {1} (log to {2})'.format(log_type, message, Logger.LOG_FILENAME))
    Logger.logger.debug('{0} {1}'.format(log_type, message))
    
    database_file = Config.SQLALCHEMY_DATABASE_FILENAME
    message = '{0} Working on DB {1}'.format(log_type,  database_file)
    Logger.logger.debug(message)

    if os.path.exists(database_file):
        message = '{0} Removing existing DB {1}'.format(log_type, database_file)
        Logger.logger.debug(message)
        os.remove(database_file)
    message = '{0} Creating app...'.format(log_type)
    Logger.logger.debug(message)
    app = create_app()
    with app.test_request_context():
        app.config.from_object(Config)

        message = '{0} Initializing app...'.format(log_type)
        Logger.logger.debug(message)
        db.init_app(app)
        
        message = '{0} Creating DB {1}'.format(log_type, database_file)
        Logger.logger.debug(message)
        db.create_all()
        
        message = '{0} Populate DB {1}'.format(log_type, database_file)
        Logger.logger.debug(message)
        
        # Users
        message = '{0} Adding admin'.format(log_type)
        Logger.logger.debug(message)
        u = User(username="admin", email="admin@localhost.com", role="ADMIN", enabled=1)
        u.set_password_hash("admin")
        db.session.add(u)

        message = '{0} Adding user'.format(log_type)
        Logger.logger.debug(message)
        u = User(username="user", email="user@localhost.com",  role="USER", enabled=1)
        u.set_password_hash("user")
        db.session.add(u)
        
        # Setup
        s = Setup(camera_ip='', gps_interval=0, gps_store=0, stop_on_lost_connection_interval=6, client_keepalive_interval=3 )
        db.session.add(s)

        # GpsData
        g = GpsData(satellites=0, gps_quality=0, altitude="", latitude="", longitude="")
        db.session.add(g)

        message = '{0} Commit'.format(log_type)
        Logger.logger.debug(message)
        db.session.commit()
        
except Exception as e:
    message = '{0} Process aborted due to unexpected exception {1}'.format(log_type, e)
    Logger.logger.debug(message)
    print(message)
finally:
    message = '{0} Process ended'.format(log_type)
    Logger.logger.debug(message)
    print(message)

exit()
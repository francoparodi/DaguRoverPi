# DaguRoverPi

Java to Python porting of project [RaspDaguRover](https://github.com/francoparodi/RaspiDaguRover) with some important improvements as:
* Users handling (stored in SQLlite DB)
* GPS support and GEO data (stored in SQLlite DB)
* Ultrasonic sensor to avoid collisions (automatically stop)

## Prerequisites
[Motion](https://motion-project.github.io/) software to be able to stream camera content. 

**Quick start** (maybe on Debian-like distro):

installation:
```sh
sudo apt install motion
```

configuration:
```sh
sudo nano /etc/motion/motion.conf
```

start:
```sh
sudo motion
```

logs:
```sh
tail -f /var/log/motion
```

Look for motion_sample.conf in this project.

## Installing

From the project root:
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 init-db.py
```
Init DB process will create two users:

**admin** (pwd: admin role: ADMIN - can handle users)

**user** (pwd: user role: USER - cannot handle users)

## Running

__as app__

```sh
export FLASK_APP=flaskr
flask run
```

__as wsgi server__

```sh
waitress-serve --host localhost --port 8080 --call 'flaskr:create_app'
```
or
```sh
gunicorn --worker-class eventlet -w 1 -b localhost:8080 wsgi
```

## Deployment

As seen above (gunicorn, waitress...)

## Authors 

Franco Parodi <franco.parodi@aol.com>

## License

This project is licensed under the MIT License
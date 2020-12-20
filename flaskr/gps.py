import sys
import serial
import time

class Gps():

    # Hardware module model. 'GPS NEO6M'
    try:
        import RPi.GPIO as GPIO
    except (RuntimeError, ModuleNotFoundError):
        import fake_rpi
        GPIO = fake_rpi.RPi.GPIO
        sys.modules['RPi'] = fake_rpi.RPi
        sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO
        sys.modules['smbus'] = fake_rpi.smbus
        sys.modules['serial'] = fake_rpi.serial
    
    gpsTXD = 15 # GPIO15, pin10 Violet
    gpsRXD = None # Not required
    online = True
    port = "/dev/ttyAMA0"
    baudrate = 9600
    timeout = 0.5
    timestamp = 0
    satellites = 0
    gpsQuality = 0
    altitude = 0
    altitudeUm = ''
    latitude = 0
    longitude = 0
    latitude_dir = 0
    longitude_dir = 0  

    @classmethod
    def gpsData(cls):
        try:
            port = "/dev/ttyAMA0"
            data = serial.Serial(port, baudrate=9600, timeout=0.5)    
        except(serial.SerialException):
            # fake data
            time.sleep(2)
            data = "$GPGGA,181739.065,4535.920,N,00958.319,E,1,12,1.0,0.0,M,0.0,M,,*6B"

        return data

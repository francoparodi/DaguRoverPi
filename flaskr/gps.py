import sys
import serial
import time
import string
import random

class Gps():

    # Hardware module model. 'GPS NEO6M'
    try:
        import RPi.GPIO as GPIO
    except (RuntimeError, ModuleNotFoundError):
        print('error on import RPi.GPIO, use fake_rpi')
        import fake_rpi
        GPIO = fake_rpi.RPi.GPIO
        sys.modules['RPi'] = fake_rpi.RPi
        sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO
        sys.modules['smbus'] = fake_rpi.smbus
        sys.modules['serial'] = fake_rpi.serial
    
    gpsTXD = 15 # GPIO15, pin10, RXD0
    gpsRXD = None # Not required
    online = True
    timestamp = 0
    satellites = 0
    gpsQuality = 0
    altitude = 0
    altitudeUm = ''
    latitude = 0
    longitude = 0
    latitude_dir = 0
    longitude_dir = 0
    fake_GPGGA_data = ("GPGGA,181739.065,4535.920,N,00958.319,E,1,12,1.0,0.0,M,0.0,M,,*6B",
    "GPGGA,172814.0,3723.46587704,N,12202.26957864,W,2,6,1.2,18.893,M,-25.669,M,2.0,0031*4F",
    "GPGGA,001038.00,3334.2313457,N,11211.0576940,W,2,04,5.4,354.682,M,-26.574,M,7.0,0138*79",
    "GPGGA,115739.00,4158.8441367,N,09147.4416929,W,4,13,0.9,255.747,M,-32.00,M,01,0000*6E",
    "GPGGA,181908.00,3404.7041778,N,07044.3966270,W,4,13,1.00,495.144,M,29.200,M,0.10,0000*40")
    serialPort = serial.Serial(port='/dev/ttyAMA0', baudrate=9600, timeout=0.5)

    @classmethod
    def gpsData(cls):
        try:            
            gps_data = serialPort.readline().decode('ascii', errors='replace')
        except Exception as e:
            # fake data
            print('exception  ' + str(e) + ' on reading GPS data, use fake data')
            time.sleep(2)
            index = random.randrange(0, 4, 1)
            gps_data = Gps.fake_GPGGA_data[index]

        return gps_data

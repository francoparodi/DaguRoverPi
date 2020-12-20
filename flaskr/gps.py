class Gps():

    # Hardware module model. 'GPS NEO6M'
    import sys, serial
    try:
        import RPi.GPIO as GPIO
        port = "/dev/ttyAMA0"
        data = serial.Serial(port, baudrate=9600, timeout=0.5)
    except (RuntimeError, ModuleNotFoundError, serial.SerialException):
        import fake_rpi
        GPIO = fake_rpi.RPi.GPIO
        sys.modules['RPi'] = fake_rpi.RPi
        sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO
        sys.modules['smbus'] = fake_rpi.smbus
        sys.modules['serial'] = fake_rpi.serial
        port = None
        data = None
    
    gpsTXD = 15 # GPIO15, pin10 Violet
    gpsRXD = None # Not required
    online = True 
    time = 0
    satellites = 0
    gpsQuality = 0
    altitude = 0
    altitudeUm = ''
    latitude = 0
    longitude = 0
    latitude_dir = 0
    longitude_dir = 0

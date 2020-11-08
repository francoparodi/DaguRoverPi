class Rover():

    import sys
    try:
        import RPi.GPIO as GPIO
    except (RuntimeError, ModuleNotFoundError):
        import fake_rpi
        GPIO = fake_rpi.RPi.GPIO
        sys.modules['RPi'] = fake_rpi.RPi
        sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO
        sys.modules['smbus'] = fake_rpi.smbus

    def __init__(self):
        self.speed = 0
        self.status = 'stop' # values: 'stop', 'forward', 'backward', 'clockwise', 'counter-clockwise'
        self.leftFrontMotor = 23 # GPIO23, pin16
        self.leftBackMotor = 24 # GPIO24, pin18
        self.rightFrontMotor = 17 # GPIO17, pin11
        self.rightBackMotor = 27 # GPIO27, pin13
        self.leftSideMotorsEnabling = 18 # GPIO18, pin12
        self.rightSideMotorsEnabling = 22 # GPIO22, pin15
        self.frequency = 50
        self.leftMotors = None
        self.rightMotors = None
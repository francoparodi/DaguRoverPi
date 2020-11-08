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

    speed = 0
    status = 'stop' # values: 'stop', 'forward', 'backward', 'clockwise', 'counter-clockwise'
    leftFrontMotor = 23 # GPIO23, pin16
    leftBackMotor = 24 # GPIO24, pin18
    rightFrontMotor = 17 # GPIO17, pin11
    rightBackMotor = 27 # GPIO27, pin13
    leftSideMotorsEnabling = 18 # GPIO18, pin12
    rightSideMotorsEnabling = 22 # GPIO22, pin15
    frequency = 50
    leftMotors = None
    rightMotors = None
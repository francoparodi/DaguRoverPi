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

    power = 0
    status = 'STOP' # values: 'STOP', 'FORWARD', 'BACKWARD', 'CLOCKWISE', 'COUNTER-CLOCKWISE'
    leftFrontMotor = 23 # GPIO23, pin16 Blue
    leftBackMotor = 24 # GPIO24, pin18 Green
    rightFrontMotor = 17 # GPIO17, pin11 Brown
    rightBackMotor = 27 # GPIO27, pin13 Violet
    leftSideMotorsEnabling = 18 # GPIO18, pin12 PWM Yellow
    rightSideMotorsEnabling = 12 # GPIO12, pin32 PWM White
    frequency = 50
    leftMotors = None
    rightMotors = None
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
    rightBackMotor = 5 # GPIO5, pin29 Blue (Channel01)
    rightFrontMotor = 6 # GPIO06, pin31 Green (Channel03)
    leftBackMotor = 16 # GPIO16, pin36 Violet (Channel02)
    leftFrontMotor = 17 # GPIO17, pin11 Brown (Channel04)
    rightSideMotorsEnabling = 12 # GPIO12, pin32 PWM White (Channel 01/03)
    leftSideMotorsEnabling = 18 # GPIO18, pin12 PWM Yellow (Channel 02/04)

    frequency = 50
    leftMotors = None
    rightMotors = None
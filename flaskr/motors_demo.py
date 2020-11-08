import time, sys, atexit

try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpi
    GPIO = fake_rpi.RPi.GPIO
    sys.modules['RPi'] = fake_rpi.RPi
    sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO
    sys.modules['smbus'] = fake_rpi.smbus

leftFrontMotor = 23 # GPIO23, pin16
leftBackMotor = 24 # GPIO24, pin18
rightFrontMotor = 17 # GPIO17, pin11
rightBackMotor = 27 # GPIO27, pin13
leftSideMotorsEnabling = 18 # GPIO18, pin12
rightSideMotorsEnabling = 22 # GPIO22, pin15
frequency = 50
leftMotors = None
rightMotors = None
initialSpeed = 10

def gpioSetup():
    GPIO.setmode(GPIO.BCM)

    # Motors
    GPIO.setup(leftFrontMotor, GPIO.OUT)
    GPIO.setup(leftBackMotor, GPIO.OUT)
    GPIO.setup(rightFrontMotor, GPIO.OUT)
    GPIO.setup(rightBackMotor, GPIO.OUT)
    # Motors Directions
    setLeftMotorsDirection('forward')
    setRightMotorsDirection('forward')
    time.sleep(1)

    # Enable left side motors
    GPIO.setup(leftSideMotorsEnabling, GPIO.OUT)
    global leftMotors
    leftMotors = GPIO.PWM(leftSideMotorsEnabling, frequency)
    # Enable right side motors
    GPIO.setup(rightSideMotorsEnabling, GPIO.OUT)
    global rightMotors
    rightMotors = GPIO.PWM(rightSideMotorsEnabling, frequency)

def setLeftMotorsDirection(direction):
    if (direction == 'forward'):
        GPIO.output(leftFrontMotor, GPIO.HIGH)
        GPIO.output(leftBackMotor, GPIO.LOW)
    else:
        GPIO.output(leftFrontMotor, GPIO.LOW)
        GPIO.output(leftBackMotor, GPIO.HIGH)

def setRightMotorsDirection(direction):
    if (direction == 'forward'):
        GPIO.output(rightFrontMotor, GPIO.HIGH)
        GPIO.output(rightBackMotor, GPIO.LOW)
    else:
        GPIO.output(rightFrontMotor, GPIO.LOW)
        GPIO.output(rightBackMotor, GPIO.HIGH)

def stopMotors():
    leftMotors.stop()
    rightMotors.stop()

def startMotors(speed = initialSpeed):
    leftMotors.start(speed)
    rightMotors.start(speed)

def setSpeed(speed):
    leftMotors.ChangeDutyCycle(speed)
    rightMotors.ChangeDutyCycle(speed)

def demo():
    # GPIO Setup
    gpioSetup()
    time.sleep(1)

    # Start motors (power of 10%)
    startMotors(initialSpeed)
    time.sleep(2)

    # Increase speed
    setSpeed(30)
    time.sleep(2)

    # Stop motors
    stopMotors()
    time.sleep(1)

    # Change direction
    setLeftMotorsDirection('backward')
    setRightMotorsDirection('backward')

    # Start motors (power of 10%)
    startMotors(initialSpeed)
    time.sleep(3)

    # increase speed
    setSpeed(30)
    time.sleep(3)

    # stop motors
    stopMotors()
    time.sleep(1)

    GPIO.cleanup()

# Safa terminating
def cleanUp():  
    stopMotors()
    GPIO.cleanup()

atexit.register(cleanUp)

demo()

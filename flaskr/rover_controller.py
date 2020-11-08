import time, atexit
from flaskr.rover import Rover as rover

def gpioSetup():
    rover.GPIO.setmode(rover.GPIO.BCM)

    # Motors
    rover.GPIO.setup(rover.leftFrontMotor, rover.GPIO.OUT)
    rover.GPIO.setup(rover.leftBackMotor, rover.GPIO.OUT)
    rover.GPIO.setup(rover.rightFrontMotor, rover.GPIO.OUT)
    rover.GPIO.setup(rover.rightBackMotor, rover.GPIO.OUT)
    # Motors Directions
    setLeftMotorsDirection('forward')
    setRightMotorsDirection('forward')
    time.sleep(1)

    # Enable left side motors
    rover.GPIO.setup(rover.leftSideMotorsEnabling, rover.GPIO.OUT)
    rover.leftMotors = rover.GPIO.PWM(rover.leftSideMotorsEnabling, rover.frequency)
    # Enable right side motors
    rover.GPIO.setup(rover.rightSideMotorsEnabling, rover.GPIO.OUT)
    rover.rightMotors = rover.GPIO.PWM(rover.rightSideMotorsEnabling, rover.frequency)

def setLeftMotorsDirection(direction):
    if (direction == 'forward'):
        rover.GPIO.output(rover.leftFrontMotor, rover.GPIO.HIGH)
        rover.GPIO.output(rover.leftBackMotor, rover.GPIO.LOW)
    else:
        rover.GPIO.output(rover.leftFrontMotor, rover.GPIO.LOW)
        rover.GPIO.output(rover.leftBackMotor, rover.GPIO.HIGH)

def setRightMotorsDirection(direction):
    if (direction == 'forward'):
        rover.GPIO.output(rover.rightFrontMotor, rover.GPIO.HIGH)
        rover.GPIO.output(rover.rightBackMotor, rover.GPIO.LOW)
    else:
        rover.GPIO.output(rover.rightFrontMotor, rover.GPIO.LOW)
        rover.GPIO.output(rover.rightBackMotor, rover.GPIO.HIGH)

def stopMotors():
    rover.leftMotors.stop()
    rover.rightMotors.stop()

def startMotors(speed):
    rover.leftMotors.start(speed)
    rover.rightMotors.start(speed)

def setSpeed(speed):
    rover.leftMotors.ChangeDutyCycle(speed)
    rover.rightMotors.ChangeDutyCycle(speed)

# Safe terminating
def cleanUp():  
    stopMotors()
    rover.GPIO.cleanup()

atexit.register(cleanUp)

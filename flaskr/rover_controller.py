import time
from flaskr.rover import Rover as rover

def gpioSetup():
    rover.GPIO.setmode(rover.GPIO.BCM)

    # Motors
    rover.GPIO.setup(rover.leftFrontMotor, rover.GPIO.OUT)
    rover.GPIO.setup(rover.leftBackMotor, rover.GPIO.OUT)
    rover.GPIO.setup(rover.rightFrontMotor, rover.GPIO.OUT)
    rover.GPIO.setup(rover.rightBackMotor, rover.GPIO.OUT)
    # Motors Directions
    setLeftMotorsDirection('FORWARD')
    setRightMotorsDirection('FORWARD')
    time.sleep(1)

    # Enable left side motors
    rover.GPIO.setup(rover.leftSideMotorsEnabling, rover.GPIO.OUT)
    rover.leftMotors = rover.GPIO.PWM(rover.leftSideMotorsEnabling, rover.frequency)
    # Enable right side motors
    rover.GPIO.setup(rover.rightSideMotorsEnabling, rover.GPIO.OUT)
    rover.rightMotors = rover.GPIO.PWM(rover.rightSideMotorsEnabling, rover.frequency)

def execute_command(command, value): 
    print('Command:{0} Value:{1}'.format(command, value))
    if (command == 'CHANGE_STATUS'):
        if (value == 'STOP'):
            stopMotors()
            rover.status = value
        elif (value == 'FORWARD'):
            stopMotors()
            setLeftMotorsDirection(value)
            setRightMotorsDirection(value)
            startMotors()
            rover.status = value
        elif (value == 'BACKWARD'):
            stopMotors() 
            setLeftMotorsDirection(value)
            setRightMotorsDirection(value)
            startMotors()
            rover.status = value
        elif (value == 'CLOCKWISE'):
            stopMotors() 
            setLeftMotorsDirection('FORWARD')
            setRightMotorsDirection('BACKWARD')
            startMotors()
            rover.status = value
        elif (value == 'COUNTER-CLOCKWISE'):
            stopMotors()
            setLeftMotorsDirection('BACKWARD')
            setRightMotorsDirection('FORWARD')
            startMotors()
            rover.status = value
    elif (command == 'CHANGE_POWER'):
        setPower(int(value))
    else:
        print('Unknown command')

def setLeftMotorsDirection(direction):
    if (direction == 'FORWARD'):
        rover.GPIO.output(rover.leftFrontMotor, rover.GPIO.HIGH)
        rover.GPIO.output(rover.leftBackMotor, rover.GPIO.LOW)
    else:
        rover.GPIO.output(rover.leftFrontMotor, rover.GPIO.LOW)
        rover.GPIO.output(rover.leftBackMotor, rover.GPIO.HIGH)

def setRightMotorsDirection(direction):
    if (direction == 'FORWARD'):
        rover.GPIO.output(rover.rightFrontMotor, rover.GPIO.HIGH)
        rover.GPIO.output(rover.rightBackMotor, rover.GPIO.LOW)
    else:
        rover.GPIO.output(rover.rightFrontMotor, rover.GPIO.LOW)
        rover.GPIO.output(rover.rightBackMotor, rover.GPIO.HIGH)

def stopMotors():
    rover.leftMotors.stop()
    rover.rightMotors.stop()

def startMotors():
    rover.leftMotors.start(rover.power)
    rover.rightMotors.start(rover.power)

def setPower(power):
    rover.power = power
    rover.leftMotors.ChangeDutyCycle(rover.power)
    rover.rightMotors.ChangeDutyCycle(rover.power)

# Safe terminating
def cleanUp():
    stopMotors()
    setPower(0)
    rover.status = "STOP"
    rover.GPIO.cleanup()

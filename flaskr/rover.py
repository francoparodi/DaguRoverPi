class Rover():

    # speed value from 0 to 100%
    speed = 0
    # status: 'stop', 'forward', 'backward', 'clockwise', 'counter-clockwise' 
    status = 'stop'

    def __init__(self):
        self.speed = 0
        self.move_mode = 'stop'
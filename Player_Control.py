import gpiozero


"""
Each of these will only control one line of players to make differentiating between back, middle, and front easier

Will include functions for moving specific angles in relation to linear distances to avoid all that in the other file

Also will have function that just kick 
"""
class Player_Line:
    def __init__(self,move_pin,kick_pin):
        self.pin1= move_pin
        self.pin2= kick_pin


        #Init both motors as servos
        self.linear_motor = gpiozero.AngularServo(move_pin,max_pulse_width=0.0025,min_pulse_width=0.0005, max_angle=90,min_angle=-90)
        self.rotational_motor = gpiozero.AngularServo(kick_pin, max_pulse_width=0.0025,min_pulse_width=0.0005, max_angle=90,min_angle=-90)
        




    def move(self,pixel):
        pass



    def kick(self):
        pass




import gpiozero


"""
Each of these will only control one line of players to make differentiating between back, middle, and front easier
"""
class Player_Line:
    def __init__(self,move_pin,kick_pin):
        self.pin1= move_pin
        self.pin2= kick_pin


        #Init both motors as servos
        self.linear_motor = gpiozero.AngularServo(move_pin,max_pulse_width=0.0025,min_pulse_width=0.0005, max_angle=180,min_angle=0)
        self.rotational_motor = gpiozero.AngularServo(kick_pin, max_pulse_width=0.0025,min_pulse_width=0.0005, max_angle=180,min_angle=0)


    def move(self,percentage):
        
        #moves the motor to the percentage requested
        self.linear_motor.angle = round(percentage*180)


    def kick(self):
        
        #Kick should be 60 degrees
        #Make it follow through the swing in order to get maximum power
        
        pass

    
    def post_up(self):
        
        self.linear_motor.angle = 90

        #add method to make them stand vertically with rotational motor
        
        pass
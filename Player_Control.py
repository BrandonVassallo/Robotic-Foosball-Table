import gpiozero


"""
Each of these will only control one line of players to make differentiating between back, middle, and front easier

Will include functions for moving specific angles in relation to linear distances to avoid all that in the other file

Also will have functions that just kick or do a wind up kick that don't require any inputs
"""
class Player_Line:
    def __init__(self,move_pin,kick_pin):
        self.pin1= move_pin
        self.pin2= kick_pin




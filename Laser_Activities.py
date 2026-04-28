#This file is intended to be imported into all files where the laser or reciever is used. 
#
#This file contains a single class for a goal which houses both devices and all required functions

from gpiozero import OutputDevice
from gpiozero import DigitalInputDevice 


#overarching class
class Goal:


    def __init__(self,Rpin):
        self.reciever=DigitalInputDevice(Rpin)

        self.goal_notification = False

        self.reciever.when_deactivated = self._goal()


    def _goal(self):
        self.goal_notification = True

    def is_laser_detected(self): 
        return self.reciever.is_active
    #checks if laser is currently detected. This may or may not work depending on our clock cycle
    #Ex: if the ball passes through faster than the clock cycle, a goal will not be detected if we check this
     
#IF GOAL DOUBLE COUNTS/GLITCHES, ADD A WAIT HERE
    def is_goal(self):
        if self.goal_notification == True:
            self.goal_notification = False
            return True
        
        return False

 
          

        

    



    
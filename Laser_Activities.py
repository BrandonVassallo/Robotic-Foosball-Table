#This file is intended to be imported into all files where the laser or reciever is used. 
#
#This file contains a single class for a goal which houses both devices and all required functions

from gpiozero import OutputDevice
from gpiozero import DigitalInputDevice 


#overarching class
class Goal:


    def __init__(self,pinNum1,pinNum2):
        self.reciever=DigitalInputDevice(pinNum1)
        self.laser=OutputDevice(pinNum2)


    def is_laser_detected(self): 
        return self.reciever.is_active
    #checks if laser is currently detected. This may or may not work depending on our clock cycle
    #Ex: if the ball passes through faster than the clock cycle, a goal will not be detected if we check this
     

    def is_goal(self):
        time = self.reciever.inactive_time
        if time>0:
            self.reciever.inactive_time = 0
            return True
    #checks if there has been inactive time, if there has been inactive time, the ball crossed the line-> goal    
    #sets the inactive time to 0 to reset the is_goal check


    def on (self):
        self.laser.on()


    def off (self):
        self.laser.off()

          

        

    



    
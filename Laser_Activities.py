#This file is intended to be imported into all files where the laser reciever or producer is used. 
#It contains two subclasses, one for reciever, one for producer, and will provide all functionality required
#
#
#These subclasses are wrapped into the overarching goal class. This will help avoid confusion with code as
#We only have to use one var per goal. 
# 
# If we want, I can wrap this further so that the entire goal sys is a class but not needed I think
#  

from gpiozero import OutputDevice
from gpiozero import DigitalInputDevice 


#overarching class
class Goal:

    def __init__ (self, pinNum1, pinNum2):
        self.pinNum1 = pinNum1
        self.pinNum2 = pinNum2
        return



#for reciever, only function is: "is_laser_detected"
class LaserReciever(Goal):
    
    def __init__ (self,pinNum1):
        super().__init__(pinNum1)
        self.reciever = DigitalInputDevice(pinNum1)

    def is_laser_detected(self): 
        return self.reciever.is_active
    #checks if laser is currently detected. This may or may not work depending on our clock cycle
    #Ex: if the ball passes through faster than the clock cycle, a goal will not be detected if we check this
    
    def is_goal(self):
        time = self.reciever.inactive_time
        if time>0:
            return True

    

#for shooter, functions are "on" and "off"
class LaserShooter(Goal):

    def __init__(self,pinNum2):
        super().__init__(pinNum2)
        self.shooter = OutputDevice(pinNum2)

    def on (self):
        self.shooter.on()

    def off (self):
        self.shooter.off()

 
        

    



    
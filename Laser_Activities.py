#This file is intended to be imported into all files where the laser reciever or producer is used. 
#It contains two classes, one for reciever, one for producer, and will provide all functionality required

from gpiozero import OutputDevice
from gpiozero import InputDevice 




#for reciever, only function is: "is_laser_detected"
class LaserReciever:
    
    def __init__ (self, pinNum):
        self.reciever = InputDevice(pinNum)

    def is_laser_detected(self):
        
        return self.reciever.is_active
    

#for shooter, functions are "on" and "off"
class LaserShooter:

    def __init__(self, pinNum):
        self.shooter = OutputDevice(pinNum)

    def on (self):
        self.shooter.on()

    def off (self):
        self.shooter.off()

 
        

    



    
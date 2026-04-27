import gpiozero
import time
from gpiozero.pins.pigpio import PiGPIOFactory


"""
Each of these will only control one line of players to make differentiating between back, middle, and front easier
"""
class Player_Line:
    def __init__(self,move_pin,kick_pin):
        self.pin1= move_pin
        self.pin2= kick_pin
        self.kick_bool = False
        self.factory = PiGPIOFactory()
        #Init both motors as servos
        self.linear_motor = gpiozero.AngularServo(move_pin,max_pulse_width=0.0025,min_pulse_width=0.0005, max_angle=180,min_angle=0, pin_factory=self.factory)
        self.rotational_motor = gpiozero.AngularServo(kick_pin, max_pulse_width=0.0025,min_pulse_width=0.0005, max_angle=180,min_angle=0,pin_factory=self.factory)


    def move(self,percentage):
        
        #moves the motor to the percentage requested
        self.linear_motor.angle = round(percentage*180)


    def kick(self):
        
        #Kick should be 60 degrees
        #Make it follow through the swing in order to get maximum power
        self.rotational_motor.angle = 80
        time.sleep(0.2)
        self.rotational_motor.angle = 120
        time.sleep(0.2)
        self.down()
        pass

    
    def up(self):
        
        self.rotational_motor.angle = 30

        #add method to make them stand vertically with rotational motor
        
        pass



    def down(self):
        self.rotational_motor.angle = 100
        pass


    def move_and_kick(self,percentage,kick_bool):
        self.linear_motor.angle = int(round(percentage*180))
        self.kick_bool = kick_bool
        print(percentage)
        print(self.linear_motor.angle)
        print(round(percentage*180))
        if kick_bool:
            self.rotational_motor.angle = 80
            time.sleep(0.2)
            self.rotational_motor.angle = 130
            time.sleep(0.2)
            self.down()
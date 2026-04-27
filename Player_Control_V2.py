import lgpio
import time
#pip install lgpio

class Player_line:
    def __init__(self,move_pin,kick_pin):
        self.move_pin = move_pin
        self.kick_pin = kick_pin

        lgpio.setwarnings(False)
        lgpio.setmode(lgpio.BCM)
        self.gpio_chip = lgpio.gpiochip_open(0)

        lgpio.gpio_claim(self.gpio_chip, self.move_pin)
        lgpio.gpio_claim(self.gpio_chip, self.kick_pin)

    
    def set_position(self,angle,pin):
        
        #convert the angle (0-180) to pwm
        pulse_width = 0.0005 + (angle/180)*(0.0025-0.0005)
        converted_pulse_width = int(pulse_width*1000000)
        #sends the signal
        lgpio.pulsewidth(self.gpio_chip,pin,converted_pulse_width)


    def move(self,percentage):
        real_angle = percentage*180
        self.set_position(real_angle, self.move_pin)

    
    def kick(self):
        self.set_position(80,self.kick_pin)
        time.sleep(0.2)
        self.set_position(130,self.kick_pin)
        time.sleep(0.2)
        self.set_position(100,self.kick_pin)


    def up(self):
        self.set_position(30,self.kick_pin)

    
    def down(self):
        self.set_position(100,self.kick_pin)


    #releases the resources used by lgpio. We may need to use this if we run and stop the program over and over
    def cleanup(self):
        lgpio.gpiochip_close(self.gpio_chip)
import lgpio
import time
#pip install lgpio

class Player_line:

    def __init__(self,move_pin,kick_pin,vertical,middle):
        self.move_pin = move_pin
        self.kick_pin = kick_pin
        self.vertical_pos = vertical
        self.middle_pos = middle

        self.is_kicking = False # Used for .after checking  

        self.gpio_chip = lgpio.gpiochip_open(0)

        lgpio.gpio_claim_output(self.gpio_chip, self.move_pin)
        lgpio.gpio_claim_output(self.gpio_chip, self.kick_pin)



    def set_position(self,angle,pin):
        
        #convert the angle (0-180) to pwm
        pulse_width = 0.0005 + (angle/180)*(0.0025-0.0005)
        converted_pulse_width = int(pulse_width*1000000)
        #sends the signal
        lgpio.tx_servo(self.gpio_chip,pin,converted_pulse_width)




    def smooth_move(self, percentage, current):
        
        if percentage!=None:
            self.target = percentage*180

        if percentage == None:
            return current
        
        elif abs(self.target-current)<=5:
            self.set_position(self.target,self.move_pin)
            return self.target
        elif self.target>current:
            self.set_position((self.target-current)//10 + current,self.move_pin)
            return (self.target-current)//10 + current
        elif current<self.target:
            self.set_position(current - (current-self.target)//10, self.move_pin)
            return current - (current-self.target)//10
        else:
            return self.target
        

    def kick_start(self):
        """Call this to BEGIN a kick. Non-blocking."""
        self.set_position(self.vertical_pos-40, self.kick_pin)

    def kick_followthrough(self):
        """Call this ~200ms after kick_start(). Non-blocking."""
        self.set_position(self.vertical_pos+50, self.kick_pin)

    def kick_reset(self):
        """Call this ~200ms after kick_followthrough(). Non-blocking."""
        self.set_position(self.vertical_pos, self.kick_pin)
        self.is_kicking = False



    def up(self):
        self.set_position(self.vertical_pos-70,self.kick_pin)



    def down(self):
        self.set_position(self.vertical_pos,self.kick_pin)



    #releases the resources used by lgpio. We may need to use this if we run and stop the program over and over
    def cleanup(self):
        lgpio.gpiochip_close(self.gpio_chip)
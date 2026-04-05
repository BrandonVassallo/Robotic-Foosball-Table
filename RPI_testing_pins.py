#This is a test file for controlling pins on the pi

import gpiozero
#gpio pin library for simple tasks


#takes off the training wheels of gpiozero, allows for direct manipulation of pins for laser system


#----------------------BUTTON RELATED CODE---------------------------------------------------------------

reset = gpiozero.Button(2)
#creates a button named reset which uses GPIO2 (this is different from pin 2 and is actually pin 3)
#Refer to this https://pinout-ai.s3.eu-west-2.amazonaws.com/raspberry-pi-5-gpio-pinout-diagram.webp for pins/gpio names


#The following assumes a button that is connected to ground and the pin only



if reset.is_pressed:
    print ("reset pressed")
#checks if reset pressed


start = gpiozero.Button(3)

start.wait_for_press()
#waits until the button is pressed before continue code

def go():
    print ("game start")

start.when_pressed = go
#when the button is pressed, runs go
#when implementing overall code, probably want a large while loop with these statements as interupts




#-------------------SERVO RELATED CODE------------------------------------------------------------------------


#So upon futher examination there are two forms of pwm, hardware and software. This code uses any gpio pin,
#which means it uses software I think. I am not yet sure if changing to a hardware pin will automatically use
#hardware pwm instead of software. We want to use hardware because software uses cpu processing, hurting fps?
#
#
#We also need to figure out what happened when you changed the pin in the kernal, it either set it to software
#or did some gate array stuff to make it hardware pwm. 
# 
# 
# Still working on research for this.


BackLinearMotor_1 = gpiozero.Servo(17)


BackLinearMotor_1.min()
#set to minimum position

BackLinearMotor_1.mid()
#set to middle position

BackLinearMotor_1.max()
#set to maximum position

#^^^^^^^^^^^^^These shortcuts should be very useful for the linear motors but not the kicking ones


BackKickMotor_2 = gpiozero.AngularServo(27, min_angle=-90, max_angle=90)
#Because of the gearbox, we may need to limit the servo from -45 to 45 but I am not certain yet

BackKickMotor_2.angle = -90
BackKickMotor_2.angle = 22

#There are ways to itterate over this but I don't see a point,
#If we just say go to this angle it will go as fast as possible which we want I think


#--------------LASER GOAL DETECTION SYSTEM CODE--------------------------------------------------------------






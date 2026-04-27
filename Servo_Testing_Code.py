import gpiozero

from gpiozero import Servo

import time



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

ZERO = 0
MAX = 1
MID = 2
FULL_RANGE = 3
CUSTOM = 4
cutsom_spin_angle = 100
custom_lin_angle = 90

spin_pin = 12
move_pin = 13

Spin_motor = gpiozero.AngularServo(spin_pin, max_pulse_width=0.0025,min_pulse_width=0.0005, max_angle=180,min_angle=0)
Lin_motor = gpiozero.AngularServo(move_pin, max_pulse_width=0.0025,min_pulse_width=0.0005, max_angle=180,min_angle=0)

mode = CUSTOM

if mode == ZERO:
    Spin_motor.angle = 0
    Lin_motor.angle = 0
    time.sleep(1)

elif mode == MAX:
    Spin_motor.angle = 180
    Lin_motor.angle = 180
    time.sleep(1)

elif mode == MID:
    Spin_motor.angle = 90
    Lin_motor.angle = 90
    time.sleep(1)

elif mode == FULL_RANGE:

    for i in range (3):

        print(i)

        Spin_motor.min()
        Lin_motor.min()
    #set to minimum position
        time.sleep(0.5)

        # BackLinearMotor_1.mid()
    #set to middle position
        # time.sleep(3)

        Spin_motor.max()
        Lin_motor.max()
    #set to maximum position
        time.sleep(0.5)

elif mode == CUSTOM:
    Spin_motor.angle = cutsom_spin_angle
    Lin_motor.angle = custom_lin_angle
    time.sleep(1)









#BackKickMotor_2 = gpiozero.AngularServo(27, min_angle=-90, max_angle=90)
#Because of the gearbox, we may need to limit the servo from -45 to 45 but I am not certain yet

#the above comment is probably false, the small gear goes around the big one 3 full rotations
#I have no idea what this means for the math

#BackKickMotor_2.angle = -90
#BackKickMotor_2.angle = 22

#There are ways to itterate over this but I don't see a point,
#If we just say go to this angle it will go as fast as possible which we want I think
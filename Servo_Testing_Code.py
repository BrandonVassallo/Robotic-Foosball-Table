import gpiozero
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


BackLinearMotor_1 = gpiozero.Servo(12)

for i in range (12):




    BackLinearMotor_1.min()
#set to minimum position
    time.sleep(3)

    BackLinearMotor_1.mid()
#set to middle position
    time.sleep(3)

    BackLinearMotor_1.max()
#set to maximum position
    time.sleep(3)









#BackKickMotor_2 = gpiozero.AngularServo(27, min_angle=-90, max_angle=90)
#Because of the gearbox, we may need to limit the servo from -45 to 45 but I am not certain yet

#the above comment is probably false, the small gear goes around the big one 3 full rotations
#I have no idea what this means for the math

#BackKickMotor_2.angle = -90
#BackKickMotor_2.angle = 22

#There are ways to itterate over this but I don't see a point,
#If we just say go to this angle it will go as fast as possible which we want I think
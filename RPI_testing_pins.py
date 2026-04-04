#This is a test file for controlling pins on the pi

import gpiozero
#gpio pin library


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





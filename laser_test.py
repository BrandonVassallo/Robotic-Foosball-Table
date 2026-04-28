import gpiozero
import Laser_Activities

new = Laser_Activities.Goal(4,26)

new.on()

while new.is_laser_detected:
    print(new.reciever.inactive_time)





print(new.is_goal)
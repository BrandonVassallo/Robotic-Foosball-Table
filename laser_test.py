import Laser_Activities

new = Laser_Activities.Goal(4)

while True:

    if new.is_laser_detected:
        print("Laser detected")
    else:
        print("Nothing")

    if new.is_goal:
        print("Goal Scored")

    
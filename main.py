import ComputerVision as my_cv


import cv2
import sys
import numpy
import time

# ADJUSTABLE PARAMETERS
buffer = 5  # The ammount of additional pixels to add to the ROI to ensure the object is in frame of the tracker

tgt_color = (121, 46, 202) # The objects target color (Blue, Green, Red)
    # Sensitivity and ROI Area bounds can be adjusted within the function

# CROPPING Values are in the pull_frame function

'''
CUSTOMIZE YOUR RENDER SIZE:
    Default is: (640, 360)
'''

x_size = 640
y_size = 360

vid, frame, v_width, v_height = my_cv.initalize_video(buffer, x_size, y_size)
frame, tracker = my_cv.initalize_tracker(vid, frame, x_size, y_size, v_width, v_height, buffer, tgt_color)

count = 0
fps = 0
prev = 0


while True:     # Should break when the goal is triggered or the recalibration button is pressed
    count, tracker, fps, prev, ball_pos = my_cv.tracking_alg(vid, buffer, tracker, x_size, y_size, v_width, v_height, tgt_color, count, prev, fps)
    '''
    count -> Used for ROI resetting
    tracker -> the updated tracker option
    fps -> For FPS usage
    prev -> For FPS usage
    ball_pos -> Current Center of the Ball (x, y)
    '''


    if cv2.waitKey(1) & 0xFF == 27:
        print("ESCAPED IN MAIN")
        break

vid.release()
cv2.destroyAllWindows()
sys.exit()

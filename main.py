import ComputerVision as my_cv

import cv2
import sys
import numpy
import time

# ADJUSTABLE PARAMETERS
buffer = 5  # The ammount of additional pixels to add to the ROI to ensure the object is in frame of the tracker

tgt_color = (70, 70, 80) # The objects target color (Blue, Green, Red)
    # Sensitivity and ROI Area bounds can be adjusted within the function

# CROPPING Values are in the pull_frame function

'''
CUSTOMIZE YOUR RENDER SIZE:
    Default is: (640, 360)
'''

x_size = 640
y_size = 360

while True:     # Should break when the goal is triggered or the recalibration button is pressed

    vid, tracker, vid_width, vid_height = my_cv.initalize_video(buffer, x_size, y_size, tgt_color)

    count = 0

    while cv2.waitKey(1) & 0xFF == 27:
        count, tracker = my_cv.tracking_alg(vid, buffer, tracker, x_size, y_size, vid_width, vid_height, tgt_color, count)
    
    break

vid.release()
cv2.destroyAllWindows()
sys.exit()

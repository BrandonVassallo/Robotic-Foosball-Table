import cv2
import sys
import numpy
import time

import ComputerVision as my_cv

# NOTE: This only works on a white background unfortuanelty

'''
CUSTOMIZE YOUR RENDER SIZE:
    Default is: (640, 360)
'''

x_size = 640
y_size = 360


################################
# INITALIZATION
################################
'''
Notes:

This program will grab the color of the ball or any object not part of the foosball table

'''

vid, frame, v_width, v_height = my_cv.initalize_video(0, x_size, y_size)

for i in range(20): # Pull some frames to let auto exposure do it's thang
    frame = my_cv.pull_frame(vid, x_size, y_size)

cv2.imshow("TITLE: Frame", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

b, g, r = cv2.split(frame)

max_g = 80 # Maximum green value 

min_b = 100
min_r = 100

top_of_object = ()    # The position at the top of the object
bottom_of_object = () # The position at the bottom of the object

frame_blue = numpy.array(b).tolist() # Turn the numpy arrays into iterable python lists
frame_red = numpy.array(r).tolist() 
frame_green = numpy.array(g).tolist()

x_pos = 0   # To record the x position of the pointer
y_pos = 0   # To record the y position of the pointer
found = False   # To help cut off the ROI is nothing is found


################################
# PIXEL ANALYSIS
################################
'''
Notes:

The arrays provided for evaluation (frame_red, frame_green, frame_blue) are in the format below
    * The frame below is obviously not to scale

    x =   0   1   2    3
[   
y = 0    [0, 30, 40, 255],
y = 1    [0,  0, 30,  40],
y = 2    [0,  0,  0,  30],
]

'''

# Find the top point of the object by iterating through the provided frame from top to bottom
# Iterating through each array will first iterate through each value in a y arr before moving to the next y level
for y_pos in range(0, y_size, 1): 
    for x_pos in range(0, x_size, 1):
        # IF the point in the blue array is within the sensitivity bounds
        if frame_blue[y_pos][x_pos] >= (min_b):
            # IF the point in the green array is within the sensitivity bounds
            if frame_green[y_pos][x_pos] <= (max_g):
                # IF the point in the red array is within the sensitivity bounds
                if frame_red[y_pos][x_pos] >= (min_r):
                    top_of_object = (x_pos, y_pos)  # Label this point as the top of the object
                    found = True                    # Tell the program you found a point
                    break
    if found:
        break

# If a point wasn't found, return "Nothing Found" to prompt the ROI to start again
if not found:
    print("Nothing Found")
    sys.exit()

found = False

# Find the bottom point of the object by iterating through the provided frame from bottom to top
# Iterating through each array will first iterate through each value in a y arr before moving to the next y level
for y_pos in range(y_size-1, -1, -1): 
    for x_pos in range(x_size-1, -1, -1):
        # IF the point in the blue array is within the sensitivity bounds
        if frame_blue[y_pos][x_pos] >= (min_b):
            # IF the point in the green array is within the sensitivity bounds
            if frame_green[y_pos][x_pos] <= (max_g):
                # IF the point in the red array is within the sensitivity bounds
                if frame_red[y_pos][x_pos] >= (min_r):
                    bottom_of_object = (x_pos, y_pos)  # Label this point as the top of the object
                    found = True
                    break
    if found:
        break

box_x_radius = abs(bottom_of_object[1]-top_of_object[1])//2
box_y_radius = abs(bottom_of_object[0]-top_of_object[0])//2

frame = cv2.rectangle(frame, top_of_object, (bottom_of_object[0] - box_x_radius, bottom_of_object[1] + box_x_radius), (255, 0, 255), 2)      # Draw out the ROI

bottom_left_pos = (20, 100) 
font = cv2.FONT_HERSHEY_PLAIN
scale = 1

box_center = (top_of_object[1] + box_x_radius, top_of_object[0] + box_y_radius)

tgt_color = (int(b[box_center[0]][box_center[1]]), 
             int(g[box_center[0]][box_center[1]]), 
             int(r[box_center[0]][box_center[1]]))

frame = cv2.putText(frame, "BLUE:   " + str(tgt_color[0]), (20, 20), font, scale, (255, 0, 0), thickness=2, lineType=cv2.LINE_AA)
frame = cv2.putText(frame, "GREEN:  " + str(tgt_color[1]), (20, 40), font, scale, (100, 255, 100), thickness=2, lineType=cv2.LINE_AA)
frame = cv2.putText(frame, "RED:    " + str(tgt_color[2]), (20, 60), font, scale, (0,0,255), thickness=2, lineType=cv2.LINE_AA)

cv2.imshow("TITLE: Located object", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

vid.release()



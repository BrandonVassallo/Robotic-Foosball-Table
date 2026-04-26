import cv2
import ComputerVision as my_cv

"""This will be the file used for recalibration of both the CV and the servos. This is not a class but a process and we
will probably have to import all the gpiozero things for this too. This will not erase the score but we will have conditions
in the main file that can trigger this as well as a button."""

"""I will need you to write CV recalibration code in here if that is a thing we need, I can handle the rest"""

def recalibrate(vid=None, buffer=None, tracker=None, x_size=None, y_size=None, v_width=None, v_height=None, tgt_color=None, count=None, prev=None, fps=None):
    if vid == None:     # If for some reason a video object was not created create one
        vid, frame, v_width, v_height = my_cv.initalize_video(buffer, x_size, y_size)
        frame, tracker = my_cv.initalize_tracker(vid, frame, x_size, y_size, v_width, v_height, buffer, tgt_color)

        count = 0
        fps = 0
        prev = 0

        # Then run tracker at count == 0 as the tracker was already reinitalized
        count, tracker, fps, prev, ball_pos = my_cv.tracking_alg(vid, buffer, tracker, x_size, y_size, v_width, v_height, tgt_color, count, prev, fps)

        return count, tracker, fps, prev, ball_pos
    
    else:
        count = 100     # Forces recalibration at count 100

        count, tracker, fps, prev, ball_pos = my_cv.tracking_alg(vid, buffer, tracker, x_size, y_size, v_width, v_height, tgt_color, count, prev, fps)

        return count, tracker, fps, prev, ball_pos

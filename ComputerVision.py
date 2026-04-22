import os
import sys
import platform
import cv2
import numpy
import time

def initalize_video(buffer: int, x_size: int, y_size: int):
    '''
    docstring for video_tracking_builtin

    INTERUPT: A boolean to stop the tracking if necessary
    '''


    ################################
    # INITALIZATION
    ################################
    '''
    Notes:
    
    '''

    # Opens the DEFAULT webcam with the parameter 0 ( 0 -> Default Webcam )
    vid = cv2.VideoCapture(0)

    # Check if the webcam is detected
    if not vid.isOpened():
        print("No webcam found")
        return
    else:
        print("Openning webcam...")
        
    # Request MJPG (for high FPS)
    # vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    # Request 1080p
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # Request 60 FPS
    vid.set(cv2.CAP_PROP_FPS, 60)

    # Critical stability settings
    vid.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)
    #vid.set(cv2.CAP_PROP_EXPOSURE, -6)
    vid.set(cv2.CAP_PROP_AUTO_WB, 1)
    vid.set(cv2.CAP_PROP_WB_TEMPERATURE, 4500)

    v_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))    # Get the capture width and height
    v_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))


    print("Width :", v_width)
    print("Height:", v_height)
    print("FPS   :", vid.get(cv2.CAP_PROP_FPS))


    frame = pull_frame(vid, x_size, y_size)

    for i in range(10): # Pull some frames to let auto exposure do it's thang
        frame = pull_frame(vid, x_size, y_size)

    return vid, frame, v_width, v_height

    current_center_of_object = None
    past_center_of_object = None

def initalize_tracker(vid, frame, x_size, y_size, v_width, v_height, buffer, tgt_color):
    
    ################################
    # STARTING ROI
    ################################
    '''
    Notes:
        - ROI stands for "Reigon of Interest"
    '''

    # Uncomment if you want to allow the user to select their own ROI (DEBUGGING)
    #bbox = cv2.selectROI("Select Object", frame, False)

    # THIS will do it automatically (Comment the below line when debugging)
    bbox = findingROI(frame, x_size, y_size, buffer, tgt_color)

    #-------------------------------------------------------#
    #return     # Uncomment if you need to debug findingROI()
    #-------------------------------------------------------#

    while bbox == "Nothing Found":                  # While the findingROI function cannot detect the ball
        cv2.putText(frame, "LOST", (10,30), cv2.FONT_HERSHEY_PLAIN, 0.7, (255,0,0), 2)    # Show LOST
        cv2.imshow("Webcam", frame)                 # We'd still like to show the frame
        cv2.waitKey(1)
        
        frame = pull_frame(vid, x_size, y_size)

        bbox = findingROI(frame, x_size, y_size, buffer, tgt_color)

        # If the user presses the ESC key, kill the program
        if cv2.waitKey(1) & 0xFF == 27:  # ESC key
            print("EXITING...")
            sys.exit()
        

    ################################
    # STARTING THE TRACKER
    ################################
    '''
    Notes:
        - The Tracker will not start without an ROI
    '''

    tracker = cv2.legacy.TrackerCSRT.create()       # When a bbox is finally found, start the tracker
    tracker.init(frame, bbox)                       # Initalize the tracker with the bbox on the ball

    return frame, tracker



'''
This function involves running the tracking algorithm.
This function is intended to be called in a loop.
If called in a loop, the below inputs/outputs must be connected in a feedback configuration:
    - tracker
    - count
'''
def tracking_alg(vid: cv2.VideoCapture, 
                 buffer: int, 
                 tracker: cv2.TrackerCSRT, 
                 x_size: int, 
                 y_size: int, 
                 v_width: int, 
                 v_height: int,
                 tgt_color: tuple[int, int, int],
                 count: int,
                 prev: int,
                 fps: int):
    '''
    docstring for tracking_alg:

    vid: The video object for cv2
    buffer: The ammount of additional pixels to add to the ROI to ensure 
        the object is in frame of the tracker
    tracker: The initalized tracker from the previous run
    x_size: The prefered x size of the frame (for either resizing or cropping)
    y_size: The prefered y size of the frame (for either resizing or cropping)
    v_width: The actual width of the raw input frame
    v_heigh: The actual height of the raw input frame
    tgt_color: The color of the object being tracked (blue, green , red)
    count: Used for FPS calculation
    prev: Used for FPS Calculation
    fps: Used for FPS calculation
    '''

    ################################
    # RUNNING THE TRACKER
    ################################
    '''
    Notes:
        - We still need to implement the actual location tracking and velocity
        calculation in this section
            (see the "if not success --> else" branch)
    '''
    curr = time.time()      # For FPS Calculaiton
    
    key = cv2.waitKey(1) & 0xFF

    frame = pull_frame(vid, x_size, y_size)

    # Calculate frames every 0.25 seconds
    if count % 25 == 0:
        fps = 1 / (curr - prev)
        
    if count == 100:   # Reset the tracker every couple frames for accuracy
        bbox = findingROI(frame, x_size, y_size, buffer, tgt_color)    # Reinitalize the tracker for accuracy
        tracker = None
        cv2.waitKey(1)
        if bbox != "Nothing Found":                             # If it doesn't work, keep trying
            tracker = cv2.legacy.TrackerCSRT.create()
            tracker.init(frame, bbox)
            cv2.waitKey(1)
        count = 0       # Reset the timer
    else:
        count += 1

    # If the user presses R, recalibrate the tracker
    if key == ord('r'):
        cv2.putText(frame, "Recalibrating", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)    # Show that it's recalibrating
        tracker = None
        bbox = findingROI(frame, x_size, y_size, buffer, tgt_color)                # Try to reinitalize the bbox
        cv2.waitKey(5)
        if bbox != "Nothing Found":                             # If it doesn't work, keep trying
            tracker = cv2.legacy.TrackerCSRT.create()
            tracker.init(frame, bbox)
            cv2.waitKey(5)

    elif key == 27:
        print("ESCAPED IN CV")
        sys.exit()

    # If the user doesn't press R, track the object
    else:
        if tracker != None:
            success, bbox = tracker.update(frame)       # Update the tracker every frame
        if tracker == None or not success:                             # If the object is LOST
            cv2.putText(frame, "LOST", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)    # Show lost
            bbox = findingROI(frame, x_size, y_size, buffer, tgt_color)                # Try to reinitalize the bbox
            if bbox != "Nothing Found":                             # If it doesn't work, keep trying
                tracker = cv2.legacy.TrackerCSRT.create()
                tracker.init(frame, bbox)

        else:                                       # If the object is FOUND
            x, y, w, h = [int(v) for v in bbox]     # Create a rectangle around it
            current_center_of_object = (x+(w/2), y+(h/2))
            past_center_of_object = current_center_of_object

            # frame, move_vector = movementVector(frame, current_center_of_object, past_center_of_object)

            """ 
            USE THESE "x" and "y" VALUES TO FIND CURRENT POSITION
            """

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)      # Slap the rectangle on the screen
            cv2.putText(frame, "Tracking", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)    # Show that it's tracking
    
    prev = curr         # Used for FPS Tracking

    # Display the FPS
    cv2.putText(frame, f"FPS: {int(fps)}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    # ----------------- UPDATE PLAYER POSITION ------------------- #

    # Show the current frame
    cv2.imshow("Webcam", frame)
    cv2.waitKey(1)

    

    return count, tracker, fps, prev, current_center_of_object



'''
This function involves finding the Reigon of Interest to help restart
the targeted tracking object every time.

NOTE: Sensivity Adjustments can be made here
'''
def findingROI(frame, x_size, y_size, buffer, tgt_color):
    '''
    Docstring for findingROI
    
    frame: The current frame provided by the webcam
    x_size: The x dimension of the provided frame
    y_size: The y dimension of the provided frame
    buffer: The ammount of additional pixels to add to the ROI to ensure 
            the object is in frame of the tracker
    '''

    # ADJUSTABLE PARAMETERS
    
    sensitivity = 30            # ammount of color units of buffer between each tgt color

    area_low_bound = 0       # The lower bounds of the objects area for error checking
    area_high_bound = 10000     # The upper bounds of the objects area for error checking
        # The Box Width/Height for the red testing ball should be around 90/90 (an Area of 8100)
    
    ################################
    # INITALIZATION
    ################################
    '''
    Notes:
    
    '''

    b, g, r = cv2.split(frame)  # Split the frame to extract the color that you need (red)

    top_of_object, bottom_of_object = BoundDetect(b, g, r, tgt_color, sensitivity, x_size, y_size)

    
    ################################
    # CALCULATING ROI
    ################################
    '''
    Notes:
    
    '''

    if top_of_object == "Nothing Found" or bottom_of_object == "Nothing Found":
        return "Nothing Found"

    box_radius = abs(bottom_of_object[1]-top_of_object[1])//2 + buffer

    box_center = top_of_object[0], box_radius//2 + top_of_object[1]

    top_left_of_box_x = box_center[0] - box_radius - buffer
    top_left_of_box_y = top_of_object[1] - buffer
    pt1 = (top_left_of_box_x, top_left_of_box_y)

    bottom_right_of_box_x = box_center[0] + box_radius + buffer
    bottom_right_of_box_y = bottom_of_object[1] + buffer
    pt2 = (bottom_right_of_box_x, bottom_right_of_box_y)

    box_width = abs(pt2[0] - pt1[0])
    box_height = abs(pt2[1] - pt1[1])

    frame = cv2.rectangle(frame, pt1, pt2, (255, 0, 0), 2)      # Draw out the ROI


    """ Debugging """
    # cv2.imshow("ROI", frame)
    # cv2.waitKey()
    # cv2.waitKey(1000)
    # cv2.destroyAllWindows()

    # Clear the CLI depending on the Operating System
    # if platform.system() == "Linux":
    #     os.system('clear')
    # if platform.system() == "Windows":
    #     os.system('cls')

    print(f"WIDTH:  {box_width}\n")
    print(f"HEIGHT: {box_height}\n")
    print(f"AREA:   {box_width*box_height}")

    #cv2.putText(frame_red, "Reinitalizing...", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
    """           """

    ################################
    # ERROR CHECKING AND RETURN
    ################################
    '''
    Notes:
    
    '''
    
    
    # Anything significantly smaller or larger than the provided bounds should be 
    # considered an error and prompt another initalization
    if (box_width * box_height) < area_low_bound or (box_width * box_height) > area_high_bound:
       return "Nothing Found"
    
    if pt1[0] + box_width >= x_size:
        box_width = x_size - pt1[0]
    
    if pt1[1] >= y_size:
        box_height = y_size - pt1[1]

    return (pt1[0], pt1[1], box_width, box_height)




'''
This function focuses on isolating the colors inside each provided blue, green and red
numpy arrays to find the target color for a specific pixel. The pixels returned will 
represent the top and bottom of the object
'''
def BoundDetect(b, g, r, colr, sensitivity, x_size, y_size):
    '''
    Docstring for BoundDetect
    
    b: The blue Numpy Array
    g: The green Numpy Array
    r: The red Numpy Array
    colr: The specified color of the object you want to track a tuple as shown: (b, g, r)
    sensitivity: The pixel color amount of buffer allowed when tracking pixel colors (from 0 - 127)
        0 = exactly the provided colr
        20 = look for colors within 20 color values of colr
    x_size: The x dimension of the provided frame
    y_size: The y dimension of the provided frame
    '''

    ################################
    # INITALIZATION
    ################################
    '''
    Notes:
    
    '''

    tgt_blue = colr[0]  # The target color's blue value
    tgt_green = colr[1] # The target color's green value
    tgt_red = colr[2]   # The target color's red value

    top_of_object = ()    # The point at the top of the ball
    bottom_of_object = () # The point at the bottom of the ball

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
            if frame_blue[y_pos][x_pos] <= (tgt_blue + sensitivity) and frame_blue[y_pos][x_pos] >= (tgt_blue - sensitivity):
                # IF the point in the green array is within the sensitivity bounds
                if frame_green[y_pos][x_pos] <= (tgt_green + sensitivity) and frame_green[y_pos][x_pos] >= (tgt_green - sensitivity):
                    # IF the point in the red array is within the sensitivity bounds
                    if frame_red[y_pos][x_pos] <= (tgt_red + sensitivity) and frame_red[y_pos][x_pos] >= (tgt_red - sensitivity):
                        top_of_object = (x_pos, y_pos)  # Label this point as the top of the object
                        found = True                    # Tell the program you found a point
                        break
        if found:
            break

    # If a point wasn't found, return "Nothing Found" to prompt the ROI to start again
    if not found:
        return "Nothing Found", "Nothing Found"
    
    found = False

    # Find the bottom point of the object by iterating through the provided frame from bottom to top
    # Iterating through each array will first iterate through each value in a y arr before moving to the next y level
    for y_pos in range(y_size-1, -1, -1): 
        for x_pos in range(x_size-1, -1, -1):
            # IF the point in the blue array is within the sensitivity bounds
            if frame_blue[y_pos][x_pos] <= (tgt_blue + sensitivity) and frame_blue[y_pos][x_pos] >= (tgt_blue - sensitivity):
                # IF the point in the green array is within the sensitivity bounds
                if frame_green[y_pos][x_pos] <= (tgt_green + sensitivity) and frame_green[y_pos][x_pos] >= (tgt_green - sensitivity):
                    # IF the point in the red array is within the sensitivity bounds
                    if frame_red[y_pos][x_pos] <= (tgt_red + sensitivity) and frame_red[y_pos][x_pos] >= (tgt_red - sensitivity):
                        bottom_of_object = (x_pos, y_pos)  # Label this point as the top of the object
                        found = True
                        break
        if found:
            break

    return top_of_object, bottom_of_object


"""
This function finds the movement vector of the object and adds a line in the UI
"""
############ UNWORKING ###########
def movementVector(frame, object_center_curr, object_center_prev):
    '''
    docstring for movementVector

    frame: the current frame from the webcam
    object_center_curr: the current center of the tracked object
    object_center_prev: the previous center of the tracked object
    '''

    ##################################################################
    # CHANGE THIS VALUE TO ADJUST THE SIZE OF THE VECTOR IN THE FRAME
    vector_scale = 1
    ##################################################################

    # If either of these points do not exist yet, ignore everything
    if object_center_curr == None or object_center_prev == None:
        return None
    
    # Use the change in the two points to find the total movement over one frame
    x_change = object_center_curr[0] - object_center_prev[0]
    y_change = object_center_curr[1] - object_center_prev[1]
    move_vector = (x_change, y_change)

    # Create the points used for the vector lines
    x_vector = (object_center_curr[0] + x_change)*vector_scale
    y_vector = (object_center_curr[1] + y_change)*vector_scale
    
    # Draw the vector line on the current frame
    frame = cv2.line(frame, object_center_curr, (x_vector, y_vector), (0,0,255), 3)

    return frame, move_vector 


'''
This function will pull a frame from the webcam
'''
def pull_frame(vid: cv2.VideoCapture, x_size: int, y_size: int):
    '''
    docstring for pull_frame

    vid: The webcame variable from OpenCV
    x_size: The prefered x size of the frame (for either resizing or cropping)
    y_size: The prefered y size of the frame (for either resizing or cropping)
    vwidth: The unedited video feed's width
    vheight: The uneditied video feed's height
    '''

    left_crop_x = 95    # Crops the beginning (left <-) of the frame array
    right_crop_x = 88   # Crops the end (right ->) of the frame array

    top_crop_y = 72     # Crops the top of the frame array
    bot_crop_y = 82     # Crops the bottom of the frame array

    ok = False      # Initalize the frame OK variable
    ok_count = 0    # Initalize the OK count

    # If a frame is not found, 
    while not ok:
        ok, frame = vid.read()      # Try and grab another frame

        if not ok or frame.all() == None:                  # If it still is not found, report an error and add 1 to the counr
            print("ERROR: frame not found")
            ok = False
            ok_count += 1

        if ok_count == 5:           # If the count exceeds 5, kill the program
            print("TOO MANY FRAMES DROPPED. EXITING...")
            sys.exit()

    frame = cv2.resize(frame, (x_size, y_size))   # Resize the frame to a specified value        

    # frame = frame[y_size:vheight-y_size, x_size:vwidth-x_size] # Crop the frame INSTEAD of resize for zooming
    frame = frame[top_crop_y:y_size - bot_crop_y, left_crop_x:x_size - right_crop_x] # Crop the frame WITH resize for zooming

    frame = cv2.resize(frame, (x_size, y_size))   # Resize the frame again to ensure standard resolution

    #frame = cv2.convertScaleAbs(frame, 1.0, 1)    # Increase the brigtness (default 1)
    
    # cv2.imshow("1080p60 Test", frame)
    # cv2.waitKey()
    # cv2.waitKey(1000)

    # print(frame.dtype, frame.min(), frame.max())

    return frame


'''
All code for debugging stuff is in here
'''
def debug():
    x_size = 640
    y_size = 360


    ################################
    # INITALIZATION
    ################################
    '''
    Notes:
    
    '''

    # Opens the DEFAULT webcam with the parameter 0 ( 0 -> Default Webcam )
    vid = cv2.VideoCapture(0)

    # Check if the webcam is detected
    if not vid.isOpened():
        print("No webcam found")
        return
    else:
        print("Openning webcam...")
        v_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))    # Get the capture width and height
        v_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Request MJPG (for high FPS)
    vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    # Request 1080p
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # Request 60 FPS
    vid.set(cv2.CAP_PROP_FPS, 60)

    # Critical stability settings
    vid.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    vid.set(cv2.CAP_PROP_EXPOSURE, -6)
    vid.set(cv2.CAP_PROP_AUTO_WB, 0)
    vid.set(cv2.CAP_PROP_WB_TEMPERATURE, 4500)

    vwidth = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    vheight = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print("Width :", vwidth)
    print("Height:", vheight)
    print("FPS   :", vid.get(cv2.CAP_PROP_FPS))

    frame = pull_frame(vid, x_size, y_size)

    cv2.imshow("1080p60 Test", frame)
    cv2.waitKey()
    cv2.waitKey(1000)

    vid.release()
    cv2.destroyAllWindows()

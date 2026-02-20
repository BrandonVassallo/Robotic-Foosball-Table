import cv2
import numpy
import time

def video_tracking_builtin():
    
    # ADJUSTABLE PARAMETERS
    buffer = 5  # The ammount of additional pixels to add to the ROI to ensure the object is in frame of the tracker

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

    ok, frame = vid.read()              # Read the first frame to make sure the camera is working

    if not ok:
        print("ERROR: frame not found")
        return
    
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
    bbox = findingROI(frame, v_width, v_height)

    #-------------------------------------------------------#
    #return     # Uncomment if you need to debug findingROI()
    #-------------------------------------------------------#

    while bbox == "Nothing Found":                  # While the findingROI function cannot detect the ball
        cv2.putText(frame, "LOST", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)    # Show LOST
        cv2.imshow("Webcam", frame)                 # We'd still like to show the frame
        ok, frame = vid.read()                      # Try to read the next frame
        if not ok:                                  # If there is no next frame, throw an error
            print("ERROR: frame not found")
            return  
        bbox = findingROI(frame, v_width, v_height)     # Try findingROI() again
        

    ################################
    # STARTING THE TRACKER
    ################################
    '''
    Notes:
        - The Tracker will not start without an ROI
    '''

    tracker = cv2.legacy.TrackerCSRT.create()       # When a bbox is finally found, start the tracker
    tracker.init(frame, bbox)                       # Initalize the tracker with the bbox on the ball

    prev = 0    # These constants are used for the FPS counter
    count = 0
    fps = 0

    ################################
    # RUNNING THE TRACKER
    ################################
    '''
    Notes:
        - We still need to implement the actual location tracking and velocity
        calculation in this section
            (see the "if not success --> else" branch)
    '''
       
    while True:

        curr = time.time()  

        ok, frame = vid.read()      # Read the current frame

        if not ok:                  # If there is no frame, throw an error
            print("ERROR: frame not found")
            return
        
        '''
        CUSTOMIZE YOUR RENDER SIZE:
            Default is: (640, 480)
        '''

        x_size = 640
        y_size = 480

        frame = cv2.resize(frame, (x_size, y_size))   # Resize the frame to a specified value

        success, bbox = tracker.update(frame)       # Update the tracker every frame
        if not success:                             # If the object is LOST
            cv2.putText(frame, "LOST", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)    # Show lost
            bbox = findingROI(frame, x_size, y_size, buffer)                # Try to reinitalize the bbox
            if bbox != "Nothing Found":                             # If it doesn't work, keep trying
                tracker = cv2.legacy.TrackerCSRT.create()
                tracker.init(frame, bbox)

        else:                                       # If the object is FOUND
            x, y, w, h = [int(v) for v in bbox]     # Create a rectangle around it

            """ 
            USE THESE "x" and "y" VALUES TO FIND CURRENT POSITION
                Also incorperate a previous position to help calculate velo
            """

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)      # Slap the rectangle on the screen
            cv2.putText(frame, "Tracking", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)    # Show that it's tracking
        
        # Calculate frames every 0.25 seconds
        if count % 25 == 0:
            fps = 1 / (curr - prev)
            
        if count == 3000:   # Reset the tracker every 3 seconds for accuracy
            bbox = findingROI(frame, x_size, y_size)    # Reinitalize the tracker for accuracy
            tracker = cv2.legacy.TrackerCSRT.create()
            tracker.init(frame, bbox)
            count = 0       # Reset the timer
        else:
            count += 1
        prev = curr         # Used for FPS Tracking

        # Display the FPS
        cv2.putText(frame, f"FPS: {int(fps)}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        # Show the current frame
        cv2.imshow("Webcam", frame)
        
        # If the user presses the ESC key, kill the program
        if cv2.waitKey(1) & 0xFF == 27:  # ESC key
            break

    vid.release()
    cv2.destroyAllWindows()
    pass

'''
This function involves finding the Reigon of Interest to help restart
the targeted tracking object every time.
'''
def findingROI(frame, x_size, y_size, buffer):
    '''
    Docstring for findingROI
    
    frame: The current frame provided by the webcam
    x_size: The x dimension of the provided frame
    y_size: The y dimension of the provided frame
    buffer: The ammount of additional pixels to add to the ROI to ensure 
            the object is in frame of the tracker
    '''

    # ADJUSTABLE PARAMETERS
    tgt_color = (255, 255, 255) # The objects target color (Blue, Green, Red)
    sensitivity = 10            # ammount of color units of buffer between each tgt color

    area_low_bound = 6000       # The lower bounds of the objects area for error checking
    area_high_bound = 15000     # The upper bounds of the objects area for error checking
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


    box_radius = (bottom_of_object[1]-top_of_object[1])//2 + buffer

    box_center = (top_of_object[0], box_radius//2 + top_of_object[1])

    top_left_of_box_x = box_center[0] - box_radius - buffer
    top_left_of_box_y = top_of_object[1] - buffer
    pt1 = (top_left_of_box_x, top_left_of_box_y)

    bottom_right_of_box_x = box_center[0] + box_radius + buffer
    bottom_right_of_box_y = bottom_of_object[1] + buffer
    pt2 = (bottom_right_of_box_x, bottom_right_of_box_y)

    box_width = pt2[0] - pt1[0]
    box_height = pt2[1] - pt1[1]

    frame_red = cv2.rectangle(r, pt1, pt2, (255, 0, 0), 2)      # Draw out the ROI


    """ Debugging """
    #cv2.imshow("ROI", frame_red)
    #cv2.waitKey()
    #cv2.waitKey(1000)
    #cv2.destroyAllWindows()

    #print(f"WIDTH: {box_width}\n")
    #print(f"HEIGHT: {box_height}\n")

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

    # If a point wasn't found, return "Nothing Found" to prompt the ROI to start again
    if not found:
        return "Nothing Found"
    
    found = False

    # NOTE: If something is found, the below for loop should find the point from above in worst case scenario
    #       This removes the need for a second "found" check

    # Find the bottom point of the object by iterating through the provided frame from bottom to top
    # Iterating through each array will first iterate through each value in a y arr before moving to the next y level
    for y_pos in range(y_size, 0, -1): 
        for x_pos in range(x_size, 0, -1):
            # IF the point in the blue array is within the sensitivity bounds
            if frame_blue[y_pos][x_pos] <= (tgt_blue + sensitivity) and frame_blue[y_pos][x_pos] >= (tgt_blue - sensitivity):
                # IF the point in the green array is within the sensitivity bounds
                if frame_green[y_pos][x_pos] <= (tgt_green + sensitivity) and frame_green[y_pos][x_pos] >= (tgt_green - sensitivity):
                    # IF the point in the red array is within the sensitivity bounds
                    if frame_red[y_pos][x_pos] <= (tgt_red + sensitivity) and frame_red[y_pos][x_pos] >= (tgt_red - sensitivity):
                        bottom_of_object = (x_pos, y_pos)  # Label this point as the top of the object
                        break

    return top_of_object, bottom_of_object



def main():
    video_tracking_builtin()
    pass

main()
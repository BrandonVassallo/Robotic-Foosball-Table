import os
import cv2
import numpy
import matplotlib as plt
import time

from IPython.display import Image

def reading_img():

    # imread(<filename>) MUST be used to process any image
    imag = cv2.imread("Checkerboard_pattern.png") 

    if imag.all() == None:
        print("no image exists from this name")
        return
    
    cv2.imshow("TITLE: Checkerboard", imag)
    cv2.waitKey(0)      # Wait until any keyboard input to move onto the next line
    cv2.destroyAllWindows()

    img = numpy.ones((500,200,1))
    img2 = numpy.ones((500,300,200))

    cv2.imshow("TITLE: Custom Image", img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def crop_resize_image(select: int):
    imag = cv2.imread("Matvei_M.jpg")   # Defaults to read in Color
    
    if imag.all() == None:
            print("no image exists from this name")
            return


    #########################
    # CROPPING
    #########################
    if select == 0 or select == 2:

        cv2.imshow("TITLE: Best Hockey Player", imag)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.waitKey(1000)      # Wait 1 seconds to close the image
        
        cropped_imag = imag[200:800, 1100:1700]

        cv2.imshow("TITLE: Best Hockey Player but better", cropped_imag)
        cv2.waitKey(0)
        cv2.waitKey(1000)      # Wait 1 seconds to close the image
        cv2.destroyAllWindows()

        cropped_imag = imag[500:650, 1300:1500]

        cv2.imshow("TITLE: Best Hockey Player but better", cropped_imag)
        cv2.waitKey(0)
        cv2.waitKey(1000)      # Wait 1 seconds to close the image
        cv2.destroyAllWindows()

    #########################
    # RESIZING
    #########################
    if select == 1 or select == 2:
        

        cv2.imshow("TITLE: Best Hockey Player", imag)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.waitKey(1000)      # Wait 1 seconds to close the image


        # Use a custom Dimension
        new_dim = (1050, 500)
        resized_img = cv2.resize(imag, new_dim)

        cv2.imshow("TITLE: Best Hockey Player but better", resized_img)
        cv2.waitKey(0)
        cv2.waitKey(1000)      # Wait 1 seconds to close the image
        cv2.destroyAllWindows()

        # Use a scaling factor
        resized_img = cv2.resize(imag, None, fx=0.5, fy=0.5)

        cv2.imshow("TITLE: Best Hockey Player but better", resized_img)
        cv2.waitKey(0)
        cv2.waitKey(1000)      # Wait 1 seconds to close the image
        cv2.destroyAllWindows()

def flipping():
    imag = cv2.imread("Arrow.png")   # Defaults to read in Color
    
    if imag.all() == None:
            print("no image exists from this name")
            return

    imag = cv2.resize(imag, None, fx = 0.3, fy = 0.3)

    cv2.imshow("TITLE: Arrow", imag)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1000)      # Wait 1 seconds to close the image


    # FLIP OVER X AXIS

    flipped_imag = cv2.flip(imag, 0)
    """ 
    The second argument is "FlipCode"
        FlipCode == 0: Flip Over X Axis
        FlipCode == 1: Flip Over Y Axis
        FlipCode < 0 : Flip Over Both Axis 
    """

    cv2.imshow("TITLE: Arrow Flipped over X axis", flipped_imag)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1000)      # Wait 1 seconds to close the image


    # FLIP OVER Y AXIS

    flipped_imag = cv2.flip(imag, 1)
    
    cv2.imshow("TITLE: Arrow Flipped over Y axis", flipped_imag)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1000)      # Wait 1 seconds to close the image


    # FLIP OVER BOTH AXIS

    flipped_imag = cv2.flip(imag, -1)
    
    cv2.imshow("TITLE: Arrow Flipped over both axis", flipped_imag)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1000)      # Wait 1 seconds to close the image

def annotation():
    imag = cv2.imread("Jalen-H.jpg") 

    if imag.all() == None:
        print("no image exists from this name")
        return

    cv2.imshow("TITLE: Jay Money", imag)
    cv2.waitKey(0)      # Wait until any keyboard input to move onto the next line
    cv2.destroyAllWindows()
    cv2.waitKey(1000)

    ##################
    # Drawing a line
    ##################
    pt1 = (100,100)
    pt2 = (350, 320)
    color = (0, 0, 255) # Color is in BGR format

    annotated_img = cv2.line(imag, pt1, pt2, color, thickness=5, lineType=cv2.LINE_AA)
    # cv2.LINE_AA is a smoother line type

    ################################
    # Turn the line into an the arrow
    ################################
    arrow_up_pt = (pt2[0],pt2[1]-30)
    arrow_side_pt = (pt2[0]-30, pt2[1])


    annotated_img = cv2.line(annotated_img, pt2, arrow_up_pt, color, thickness=5, lineType=cv2.LINE_AA)
    annotated_img = cv2.line(annotated_img, pt2, arrow_side_pt, color, thickness=5, lineType=cv2.LINE_AA)
    

    cv2.imshow("TITLE: Jay Money with arrow", annotated_img)
    cv2.waitKey(0)      # Wait until any keyboard input to move onto the next line
    cv2.destroyAllWindows()
    cv2.waitKey(1000)

    ###############
    # Add a Circle
    ###############
    center_pt = (400, 430)
    radius = 100
    annotated_img = cv2.circle(annotated_img, center_pt, radius, color, thickness=5, lineType=cv2.LINE_AA)

    cv2.imshow("TITLE: Jay Money with circle", annotated_img)
    cv2.waitKey(0)      # Wait until any keyboard input to move onto the next line
    cv2.destroyAllWindows()
    cv2.waitKey(1000)

    ##############
    # Adding Text 
    ##############

    text = "The Undisputed Goat"
    bottom_left_pos = (20, 100) 
    font = cv2.FONT_HERSHEY_PLAIN
    scale = 4
    color = (0, 255, 0) # Green

    text2 = "Literally Him"
    bottom_left_pos2 = (20, 150)
    font2 = cv2.FONT_HERSHEY_DUPLEX
    scale2 = 2
    
    annotated_img = cv2.putText(annotated_img, text, bottom_left_pos, font, scale, color, thickness=5, lineType=cv2.LINE_AA)
    annotated_img = cv2.putText(annotated_img, text2, bottom_left_pos2, font2, scale2, color, thickness=3, lineType=cv2.LINE_AA)

    cv2.imshow("TITLE: The Truth", annotated_img)
    cv2.waitKey(0)      # Wait until any keyboard input to move onto the next line
    cv2.destroyAllWindows()
    cv2.waitKey(1000)

def masking():
    imag = cv2.imread("Yellow_Fish.jpg") 

    if imag.all() == None:
        print("no image exists from this name")
        return

    cv2.imshow("TITLE: What do you call a fish with no eye?", imag)
    cv2.waitKey(0)      # Wait until any keyboard input to move onto the next line
    cv2.destroyAllWindows()
    cv2.waitKey(1000)


    ############################
    # Adjusting the brightness
    ############################

    # Create a matrix the exact size of the image with each pixel as a constant of 100
    #   Remember: Grayscale constants go from 0 (white) to 255 (black) per pixel
    gray_scale_const_matrix = numpy.ones(imag.shape, dtype="uint8") * 150

    darker_img = cv2.add(imag, gray_scale_const_matrix)
    lighter_img = cv2.subtract(imag, gray_scale_const_matrix)

    cv2.imshow("TITLE: An overused joke that you're definitelty too old to laugh at", darker_img)
    cv2.waitKey(0)      # Wait until any keyboard input to move onto the next line
    cv2.destroyAllWindows()
    cv2.waitKey(1000)

    cv2.imshow("TITLE: A FSHHHHHHHHHHHHH !!!", lighter_img)
    cv2.waitKey(0)      # Wait until any keyboard input to move onto the next line
    cv2.destroyAllWindows()
    cv2.waitKey(1000)

    ###########################
    # Adjusting the contrast
    ###########################

    low_contrast_matrix = numpy.ones(imag.shape) * 0.8
    high_contrast_matrix = numpy.ones(imag.shape) * 1.2

    low_cont_img = numpy.uint8(cv2.multiply(numpy.float64(imag), low_contrast_matrix))
    high_cont_img = numpy.uint8(cv2.multiply(numpy.float64(imag), high_contrast_matrix))

    cv2.imshow("TITLE: Something you can't find in the dictionary", low_cont_img)
    cv2.waitKey(0)      # Wait until any keyboard input to move onto the next line
    cv2.destroyAllWindows()
    cv2.waitKey(1000)

    cv2.imshow("TITLE: Laughter", high_cont_img)
    cv2.waitKey(0)      # Wait until any keyboard input to move onto the next line
    cv2.destroyAllWindows()
    cv2.waitKey(1000)

    """
    The above image will have some sharp colors that are a result of some pixels going over 255, the bounds of openCV.
    The below command fixes that using numpy.clip() to keep the pixel values between 0 and 255
    """

    fixed_high_cont_img = numpy.uint8(
        numpy.clip(
            cv2.multiply(numpy.float64(imag), high_contrast_matrix), 
            0,      # Keep the included matrix values above 0
            255))   # Keep the included matrix values below 255

    cv2.imshow("TITLE: Laughter, but better", fixed_high_cont_img)
    cv2.waitKey(0)      # Wait until any keyboard input to move onto the next line
    cv2.destroyAllWindows()
    cv2.waitKey(1000)

def video_tracking_builtin():
    
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
            bbox = findingROI(frame, x_size, y_size)                # Try to reinitalize the bbox
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

def findingROI(frame, x_size, y_size):
    ################################
    # INITALIZATION
    ################################
    '''
    Notes:
    
    '''
    
    b, g, r = cv2.split(frame)  # Split the frame to extract the color that you need (red)
    frame_red = r               # Isolate the red matrix

    """ Debugging """
    #cv2.imshow("TITLE: RED MASK", frame_red)
    #cv2.waitKey(0)      # Wait until any keyboard input to move onto the next line
    #cv2.destroyAllWindows()
    #cv2.waitKey(1000)

    #numpy.savetxt("redballpic.csv", frame_red, '%d', ",")   # For debuging
    """           """


    top_of_ball = ()    # The point at the top of the ball
    bottom_of_ball = () # The point at the bottom of the ball

    frame_red = numpy.array(frame_red).tolist() # Turn the numpy array into an iterable python list
    x_pos = 0   # To record the x position of the pointer
    y_pos = 0   # To record the y position of the pointer
    found = False   # To help cut off the ROI is nothing is found


    ################################
    # PIXEL ANALYSIS
    ################################
    '''
    Notes:
    
    '''
    
    for y_arr in frame_red:                     # This will iterate through the y arrays first
        for x_arr in y_arr:                     # Then iterate through each y level to find the x coordinate of the top of the ball
            if frame_red[y_pos][x_pos] > 100:   # If the selected coordinate is within the correct range of color,
                top_of_ball = (x_pos, y_pos)    # record the point
                found = True                    # say you found something
                break                           # Stop iterating
            x_pos += 1
        if found:   # This will break out of the nested loop if a point is found
            break
        x_pos = 0   
        y_pos += 1

    if not found:   # If no point was found, the ball isn't in view
        return "Nothing Found"

    found = False

    for y in range(top_of_ball[1], y_size, 1):         # Iterate Straight down to try and find the last point that conforms to the correct color
        if frame_red[y][top_of_ball[0]] < 100:      # the x value (top_of_ball[0]) will stay the same to go straight down
            bottom_of_ball = (top_of_ball[0], y)    # If the current coordinate is not the color of the ball, record it as the bottom of the ball
            found = True                            # say you found the end
            break                                   # Stop iterating

    if not found:   # If no end was found, its a glitch and try again
        return "Nothing Found"

    """ Debugging """
    #print(f"top = {top_of_ball}\n\n")
    #print(f"bottom = {bottom_of_ball}\n\n")
    """           """

    ################################
    # CALCULATING ROI
    ################################
    '''
    Notes:
    
    '''
    
    buffer = 5  # Specify the amount of buffer pixels you want around the object


    box_radius = (bottom_of_ball[1]-top_of_ball[1])//2 + buffer

    box_center = (top_of_ball[0], box_radius//2 + top_of_ball[1])

    top_left_of_box_x = box_center[0] - box_radius - buffer
    top_left_of_box_y = top_of_ball[1] - buffer
    pt1 = (top_left_of_box_x, top_left_of_box_y)

    bottom_right_of_box_x = box_center[0] + box_radius + buffer
    bottom_right_of_box_y = bottom_of_ball[1] + buffer
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
    
    # The Box Width/Height for the red testing ball should be around 90/90 (an Area of 8100)
    # Anything significantly smaller or larger than that should be considered an error and prompt another initalization
    if box_width * box_height < 6000 or box_width * box_height > 15000:
        return "Nothing Found"
    
    return (pt1[0], pt1[1], box_width, box_height)


'''
Anything below this is useless and for experimentation only

'''


def drawRectangle(frame, bbox):
    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)


def displayRectangle(frame, bbox):
    plt.figure(figsize=(20, 10))
    frameCopy = frame.copy()
    drawRectangle(frameCopy, bbox)
    frameCopy = cv2.cvtColor(frameCopy, cv2.COLOR_RGB2BGR)
    plt.imshow(frameCopy)
    plt.axis("off")


def drawText(frame, txt, location, color=(50, 170, 50)):
    cv2.putText(frame, txt, location, cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

def main():
    #reading_img()
    #crop_resize_image(1) # Select = 0 is ONLY Cropping, Select = 1 is ONLY resizing, Select = 2 is both
    #flipping()
    #annotation()
    #video_tracking_builtin()
    #findingROI()
    pass

main()

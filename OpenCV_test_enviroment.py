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

def video_tracking():
    
    # Opens the DEFAULT webcame with the parameter 0
    vid = cv2.VideoCapture(0)

    if not vid.isOpened():
        print("No webcam found")
        return
    else:
        print("Openning webcam...")
        v_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        v_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the bounding box
    bbox = (300, 400, 200, 100)

    # Define your tracking types for ease of use

    tracker_types = [
    "BOOSTING",
    "MIL",
    "KCF",
    "CSRT",
    "TLD",
    "MEDIANFLOW",
    "GOTURN",
    "MOSSE",
]

    # Change the index to change the tracker type
    tracker_type = tracker_types[3]

    if tracker_type == 'BOOSTING':
        tracker = cv2.legacy.TrackerBoosting_create()
    elif tracker_type == 'MIL':
        tracker = cv2.TrackerMIL_create()
    elif tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
    elif tracker_type == 'TLD':
        tracker = cv2.legacy.TrackerTLD_create()
    elif tracker_type == 'MEDIANFLOW':
        tracker = cv2.legacy.TrackerMedianFlow_create()
    elif tracker_type == 'GOTURN':
        tracker = cv2.TrackerGOTURN_create()
    elif tracker_type == "CSRT":
        tracker = cv2.TrackerCSRT_create()
    elif tracker_type == "MOSSE":
        tracker = cv2.legacy.TrackerMOSSE_create()
    else:
        tracker = None

    # read frame
    frame = vid.read()

    # Initalize tracker
    ok = tracker.__init__(frame, bbox)
    
    while True:
        ok, frame = vid.read()

        if not ok:
            break

        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = tracker.update(frame)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        # Draw bounding box
        if ok:
            drawRectangle(frame, bbox)
        else:
            drawText(frame, "Tracking failure detected", (80, 140), (0, 0, 255))

        # Display Info
        drawText(frame, tracker_type + " Tracker", (80, 60))
        drawText(frame, "FPS : " + str(int(fps)), (80, 100))

        cv2.imshow('Webcam', frame)



    """
    Below is my half witted attempt at an fps counter for the video
    
    """

    # fps = 0.0
    # fps_diff = 0
    # spf_strt = 0.0
    # spf_end = 0.0
    # count = 0
    # fps_scale = 20

    # Gives a live feed of the camera capture

    # while True:
    #     ok, frame = vid.read()

        

        # text = str(fps)
        # bottom_left_pos = (20, 20) 
        # font = cv2.FONT_HERSHEY_PLAIN
        # scale = 1
        # color = (0, 200, 100) # Around Green

        # # Display Frames Per Second
        # frame = cv2.putText(frame, text, bottom_left_pos, font, scale, color, thickness=2, lineType=cv2.LINE_AA)

        # # Display the starting time of frame
        # bottom_left_pos = (20, 50) 
        # frame = cv2.putText(frame, str(spf_strt), bottom_left_pos, font, scale, color, thickness=2, lineType=cv2.LINE_AA)
        
        # # Display the ending amount of frame
        # bottom_left_pos = (20, 60) 
        # frame = cv2.putText(frame, str(spf_end), bottom_left_pos, font, scale, color, thickness=2, lineType=cv2.LINE_AA)        

        # if not ok:
        #     print("No Frame")
        #     break


        # # Calculating the actual FPS of the system

        # if count == 0:
        #     spf_strt = round(time.time_ns()/1_000_000)
        #     count += 1
        # elif count == fps_scale:
        #     spf_end = round(time.time_ns()/1_000_000)
        #     if spf_end-spf_strt != 0:
        #         fps_diff = (abs(spf_end-spf_strt)*10^-3)^-1
        #         fps = fps_diff*fps_scale
        #     else:
        #         fps = "TOO BIG"
        #     count = 0
        # else:
        #     count += 1
        
        # cv2.imshow('Webcam', frame)
        
        


        # if cv2.waitKey(1) and 0xFF == ord("q"):
        #     break

    vid.release()
    cv2.destroyAllWindows()
    

    pass

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
    video_tracking()
    pass

main()

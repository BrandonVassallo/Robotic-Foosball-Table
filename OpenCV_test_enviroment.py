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
    
    # Opens the DEFAULT webcame with the parameter 0
    vid = cv2.VideoCapture(0)

    # Check if the webcam is detected
    if not vid.isOpened():
        print("No webcam found")
        return
    else:
        print("Openning webcam...")
        v_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        v_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Initalize tracker
    tracker = cv2.legacy.TrackerMOSSE.create()

    ok, frame = vid.read()

    if not ok:
        print("ERROR: frame not found")
        return
    
    frame = cv2.resize(frame, (1280, 720))
    
    bbox = cv2.selectROI("Select Object", frame, False)

    tracker.init(frame, bbox)

    prev = 0
    count = 0
    fps = 0
    
    while True:

        curr = time.time()

        # Read the current frame
        ok, frame = vid.read()

        if not ok:
            print("ERROR: frame not found")
            return
        
        frame = cv2.resize(frame, (1280, 720))

        # Use the tracker
        success, bbox = tracker.update(frame)
        if not success:
            cv2.putText(frame, "LOST", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
        else:
            x, y, w, h = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(frame, "Tracking", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        
        # Calculate frames every 0.25 seconds
        if count == 25:
            fps = 1 / (curr - prev)
            count = 0
        else:
            count += 1
        prev = curr

        cv2.putText(frame, f"FPS: {int(fps)}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        
        cv2.imshow("Webcam", frame)

        
        
        

        if cv2.waitKey(1) & 0xFF == 27:  # ESC key
            break

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
    video_tracking_builtin()
    pass

main()

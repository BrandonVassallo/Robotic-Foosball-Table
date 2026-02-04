import os
import cv2
import numpy
import matplotlib as plt

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

def main():
    #reading_img()
    #crop_resize_image(1) # Select = 0 is ONLY Cropping, Select = 1 is ONLY resizing, Select = 2 is both
    #flipping()
    annotation()

main()

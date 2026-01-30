import os
import cv2
import numpy
import matplotlib as plt

from IPython.display import Image

img = numpy.ones((10,10,1))

print()
print(img)
print()


print(img.shape)
print()

def main():
    imag = cv2.imread("Checkerboard_pattern.png")
    if imag.all() == None:
        print("no image exists from this name")
        return
    
    cv2.imshow("TITLE: Checkerboard", imag)
    cv2.waitKey(0)      # Wait until any keyboard input to move onto the next line
    cv2.destroyAllWindows()

main()

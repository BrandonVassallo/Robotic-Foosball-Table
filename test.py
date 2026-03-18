import cv2
import numpy

# On Windows, DirectShow is the most reliable backend
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Request MJPG (critical for high FPS)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

# Request 1080p
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Request 60 FPS
cap.set(cv2.CAP_PROP_FPS, 60)

# Critical stability settings
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
cap.set(cv2.CAP_PROP_EXPOSURE, -6)
cap.set(cv2.CAP_PROP_AUTO_WB, 0)
cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 4500)

vwidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
vheight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("Width :", vwidth)
print("Height:", vheight)
print("FPS   :", cap.get(cv2.CAP_PROP_FPS))


ret, frame = cap.read()

if ret:

    #frame = cv2.resize(frame, (640, 420))

    x_size = 640
    y_size = 360

    # frame = frame[y_size:vheight-y_size, x_size:vwidth-x_size] # Crop the frame instead of resize

    frame = cv2.resize(frame, (x_size, y_size))

    cv2.imshow("1080p60 Test", frame)
    cv2.waitKey()
    cv2.waitKey(1000)

    frame = cv2.convertScaleAbs(frame, 1.0, 2)

    

    b, g, r = cv2.split(frame)
    
    numpy.savetxt("./.debugfolder/REDmarkerpic.csv", b, '%d', ",")
    numpy.savetxt("./.debugfolder/GREENmarkerpic.csv", g, '%d', ",")
    numpy.savetxt("./.debugfolder/BLUEmarkerpic.csv", r, '%d', ",")

    cv2.imshow("1080p60 Test", frame)
    cv2.waitKey()
    cv2.waitKey(1000)

cap.release()
cv2.destroyAllWindows()
import cv2
import numpy
import ComputerVision as my_cv

x_size = 640
y_size = 360

vid, frame, v_width, v_height = my_cv.initalize_video(0, x_size, y_size)

# frame = frame[y_size:vheight-y_size, x_size:vwidth-x_size] # Crop the frame instead of resize

for i in range(20): # Pull some frames to let auto exposure do it's thang
    frame = my_cv.pull_frame(vid, x_size, y_size)

b, g, r = cv2.split(frame)  # Split the frame

# Save the frames individual color arrays
numpy.savetxt("./.debugfolder/RED.csv", r, '%d', ",")
numpy.savetxt("./.debugfolder/GREEN.csv", g, '%d', ",")
numpy.savetxt("./.debugfolder/BLUE.csv", b, '%d', ",")

cv2.imshow("1080p60 Test", frame)
cv2.waitKey()
cv2.waitKey(1)

vid.release()
cv2.destroyAllWindows()
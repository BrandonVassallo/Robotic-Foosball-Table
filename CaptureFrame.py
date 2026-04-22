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

# ACCURATE PLAYER POSITIOING BELOW

player_circle_rad = 3
player_circle_col = (255,0,0)
player_circle_thick = -1    # FILLED

servo_percent = 0.5

y_p1 = int(servo_percent*109 + 17)
y_p2 = int(servo_percent*109 + 126)
y_p3 = int(servo_percent*109 + 235)

x_pos = 35    # GOAL ROD
cv2.circle(frame, (x_pos, y_p1), player_circle_rad, player_circle_col, player_circle_thick)
cv2.circle(frame, (x_pos, y_p2), player_circle_rad, player_circle_col, player_circle_thick)
cv2.circle(frame, (x_pos, y_p3), player_circle_rad, player_circle_col, player_circle_thick)

x_pos = 265    # DEF ROD
cv2.circle(frame, (x_pos, y_p1), player_circle_rad, player_circle_col, player_circle_thick)
cv2.circle(frame, (x_pos, y_p2), player_circle_rad, player_circle_col, player_circle_thick)
cv2.circle(frame, (x_pos, y_p3), player_circle_rad, player_circle_col, player_circle_thick)

x_pos = 495    # OFF ROD
cv2.circle(frame, (x_pos, y_p1), player_circle_rad, player_circle_col, player_circle_thick)
cv2.circle(frame, (x_pos, y_p2), player_circle_rad, player_circle_col, player_circle_thick)
cv2.circle(frame, (x_pos, y_p3), player_circle_rad, player_circle_col, player_circle_thick)

cv2.imshow("1080p60 Test", frame)
cv2.waitKey()
cv2.waitKey(1)

vid.release()
cv2.destroyAllWindows()
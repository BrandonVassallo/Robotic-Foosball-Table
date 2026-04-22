import cv2


def update_player_pos(frame, ball_pos):
    '''
    - Use the ball_pos's x-value to figure out where the servos should move to
        - Make sure to have sections for each player
    - If the ball_pos's y-value is close enough to the foot of the player, hit the ball
    - If the ball_pos's y-value is behind the current rod, ignore it
    
    '''

    # FROM PLAYER'S PERSPECTIVE (x = 0)
        # Player 1 is responsible for 136 > x > 0
        # Player 2 is responsible for 223 > x > 137 
        # Player 3 is responsible for 359 > x > 224

    # Player 1 x pos = Servo % * 136
    # Player 2 x pos = Servo % * 86 + 136
    # Player 3 x pos = Servo % * 136 + 223

    
    pass
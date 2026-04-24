import cv2
import Player_Control


def update_player_pos(frame, ball_pos):
    '''
    - Use the ball_pos's x-value to figure out where the servos should move to
        - Make sure to have sections for each player
    - If the ball_pos's y-value is close enough to the foot of the player, hit the ball
    - If the ball_pos's y-value is behind the current rod, ignore it

    - IF ball_pos == None, DO NOT Move the servos
    
    '''

    # FROM PLAYER'S PERSPECTIVE (y = 0)
        # Player 1 is responsible for 136 > y > 0      (Player from wall)
        # Player 2 is responsible for 223 > y > 137 
        # Player 3 is responsible for 359 > y > 224

    # 17 pixels from wall to center of player when on wall
    # Player 1 y pos = Servo % * 119 + 17
    # Player 2 y pos = Servo % * 86 + 119 + 17
    # Player 3 y pos = Servo % * (136 - 17) + 223

    # FOR WHITE FOOSBALL MEN (x)
        # GOAL PLAYER:
            # Rod is at 50
            # Hits when 100 > x > 0
            # Moves when 216 > x > 0

        # DEFENSE PLAYER:
            # Rod is at 226
            # Hits when 316 > x > 216
            # Moves when 428 > x > 216

        # OFFENSE PLAYERS:
            # Rod is at 478
            # Hits when 528 > x > 428
            # Moves when 639 > x > 428
    
    pass





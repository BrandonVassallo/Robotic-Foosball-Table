import cv2
import Player_Control as pc
import sys

def update_player_pos(ball_pos, goalie: pc.Player_Line, defense: pc.Player_Line, offense: pc.Player_Line):
    '''
    - Use the ball_pos's x-value to figure out where the servos should move to
        - Make sure to have sections for each player
    - If the ball_pos's y-value is close enough to the foot of the player, hit the ball
    - If the ball_pos's y-value is behind the current rod, ignore it

    - IF ball_pos == None, DO NOT Move the servos
    
    '''
    
    # 17 pixels from wall to center of player when on wall
    RUBBER_BARRIER = 17

    MAX_ROD_MOVEMENT_PIXELS = 136
    PLAYER_2_RANGE = 88

    MAX_PLAYER_1_PIXEL = MAX_ROD_MOVEMENT_PIXELS
    MAX_PLAYER_2_PIXEL = MAX_ROD_MOVEMENT_PIXELS + PLAYER_2_RANGE
    MAX_PLAYER_3_PIXEL = MAX_ROD_MOVEMENT_PIXELS*2 + PLAYER_2_RANGE

    if (ball_pos == None):
        print("NO BALL POSITION INPUTTED")
        return None     # DO NOT MOVE THE SERVOS

    active_player = goalie      # Initalize the active player as the goalie for now
    kick_bool = False           # Assume no kicking is needed yet

    # y = 0: FROM PLAYER'S PERSPECTIVE 
        # Player 1 is responsible for 136 > y > 0       (Closest to Player)
        # Player 2 is responsible for 223 > y > 137 
        # Player 3 is responsible for 359 > y > 224     (Closest to Servos)



    ##### WHAT ROD IS RESPONSIBLE? #####

    # NOTE: This is FOR WHITE FOOSBALL MEN (x)
    
    # GOAL PLAYER:
        # Rod is at 50
        # Hits when 100 > x > 0
        # Moves when 216 > x > 0

    if ball_pos[0] < 216:
        active_player = goalie
        # ADD CHECK TO KICK
        if ball_pos[0] < 100:
            kick_bool = True


    # DEFENSE PLAYER:
        # Rod is at 226
        # Hits when 316 > x > 216
        # Moves when 428 > x > 216

    elif ball_pos[0] < 428:
        active_player = defense
        # ADD CHECK TO KICK
        if ball_pos[0] < 316:
            kick_bool = True


    # OFFENSE PLAYERS:
        # Rod is at 478
        # Hits when 528 > x > 428
        # Moves when 639 > x > 428

    elif ball_pos[0] < 639:
        active_player = offense
        # ADD CHECK TO KICK
        if ball_pos[0] < 528:
            kick_bool = True


    # Ball position is out of range

    else:
        print("BALL POSITION INVALID!\n")
        print(f"ball_pos was: {ball_pos}")
        return None         # DO NOT MOVE THE SERVOS


    ##### WHAT PLAYER ON THE ROD IS RESPONSIBLE? #####

    # Player 1 (Closest to Player)
    if ball_pos[1] < MAX_PLAYER_1_PIXEL:
        if ball_pos[1] < RUBBER_BARRIER:
            move_to = 0     # If the ball is past the rubber barrier, move the servo to 0%
        else:
            move_to = int((ball_pos[1]-RUBBER_BARRIER)/MAX_ROD_MOVEMENT_PIXELS)
        active_player.move(move_to)

    # Player 2 (Center)
    elif ball_pos[1] < MAX_PLAYER_2_PIXEL:
        # Player 2's percentage must be calculated between the PLAYER_2_RANGE rather than the standard
        move_to = int((ball_pos[1]-MAX_PLAYER_1_PIXEL)/PLAYER_2_RANGE)
        # Player 2 also does not need to worry about the 17 pixel rubber barrier
        active_player.move(move_to)

    # Player 3 (Closest to Servos)
    elif ball_pos[1] < MAX_PLAYER_3_PIXEL:
        if ball_pos[1] > (360 - RUBBER_BARRIER):
            move_to = 1     # If the ball is past the rubber barier, move the servo to 100%
        else:
            move_to = int((ball_pos[1]-MAX_PLAYER_2_PIXEL)/MAX_ROD_MOVEMENT_PIXELS)
        active_player.move(move_to)
        
    # Ball position was invalid
    else:
        print("BALL POSITION INVALID!\n")
        print(f"ball_pos was: {ball_pos}")
        return None         # DO NOT MOVE THE SERVOS

    # Do we need to kick?
    if kick_bool:
        active_player.kick()




    ####################### Notes #######################

    # Player 1 y pos = Servo % * 119 + 17
        # Player 1 handles 36.5% of the field

    # Player 2 y pos = Servo % * 86 + 119 + 17
        # Player 2 handles 27% of the field

    # Player 3 y pos = Servo % * (136 - 17) + 223
        # Player 3 handles 36.5% of the field





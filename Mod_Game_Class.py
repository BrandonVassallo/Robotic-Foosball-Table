import tkinter as tk
import gpiozero
import New_cv_code as my_cv
import cv2
import PlayerPositions as pps
from enum import Enum

import Player_Control_V2 as pc
import os

 
 #Need to make recalibrate class in seperate file

#TODO
"""
-player position update
-vectors if time
"""


#To whom it may concern:

"""

I have made this entire UI scalable to the best of my ability. We will need to get better measurements
of the screen in order to have it fit correctly. The only values you *should* need to change are:
    
    self.window_size
    self.width
    self.height
    
All of these values are at the top of the init class. The main functions will be init,
goal, ball_lost, press_start, and reset/recalibration
      
"""
#______________________________Code Below______________________________________________________________________________________

#Adds the enumerated types that we will need later
class Game_States(Enum):

    IDLE = 1
    WAITING = 2
    PLAYING = 3


class Game:

    def __init__(self):
    #-------------Setting up values needed later------------------------------------------------------------------------

        #These values will need to be tweaked in the future!!!!!!!  Changes all window sizes -> and shapes
        self.window_size = "1024x600"
        self.width = 1024
        self.height = 600


        #scores will be 0-0 in initialization, used to track score of the game
        self.human_score = 0
        self.robot_score = 0


        #time in seconds
        self.timer = 0 


        self.ball_x = 0
        self.ball_y = 0


        self.current_angle_goalie = 0
        self.current_angle_offense = 0
        self.current_angle_defense = 0


        #****************************WE MAY NEED TO PICK A DIFFERENT PIN HERE*********************************************
        #makes the start button GPIO pin 
        self.start_button = gpiozero.Button(23)
        self.reset_button = gpiozero.Button(24)

        self.start_button.when_activated = self.start_pressed
        self.reset_button.when_activated = self.reset_pressed

        self.robot = gpiozero.Button(17)
        self.human = gpiozero.Button(27)

        self.human.when_activated = self.human_goal
        self.robot.when_activated = self.robot_goal

        

        #*****************************PLAYER DECLERATIONS******************************************
        self.goalie_move_pin = 26
        self.goalie_kick_pin = 19
        self.goalie = pc.Player_line(self.goalie_move_pin, self.goalie_kick_pin)

        self.def_move_pin = 6
        self.def_kick_pin = 13
        self.defense = pc.Player_line(self.def_move_pin, self.def_kick_pin)
        
        self.off_move_pin = 20
        self.off_kick_pin = 21
        self.offense = pc.Player_line(self.off_move_pin, self.off_kick_pin)


        #init the game state using enum types
        self.game_state = Game_States.IDLE

    #--------------------------------------------------------------------------------------------------------------------


    #____________________________BRANDON PARAMETERS FOR CV  (copied from main.py, not sure if needed)______________________________________________________
        
        # ADJUSTABLE PARAMETERS
        self.buffer = 5  # The ammount of additional pixels to add to the ROI to ensure the object is in frame of the tracker

        self.tgt_color = (100, 35, 100)     # The objects target color (Blue, Green, Red)
            # Sensitivity and ROI Area bounds can be adjusted within the function

        # CROPPING Values are in the pull_frame function

        '''
        CUSTOMIZE YOUR RENDER SIZE:
            Default is: (640, 360)
        '''

        self.x_size = 640
        self.y_size = 360

        self.vid = None

        self.lost_counter = 0

        self.ball_pos = None
        self.fps = 0
    #________________________________________________________________________________________________________________________


    #----------------------------------Initializing display, adding visual features----------------------------------------------------------------------

        #Create the main window
        self.screen = tk.Tk()

        # IF THE SECOND LARGER SCREEN IS CONNECTED
        self.screen.geometry("1024x600+0+0")
       
        # Force the screen to full screen
        #self.screen.attributes("-fullscreen", True)

        #Name the window
        self.screen.title("Jumbotron")

        #Set window size
        self.screen.geometry(self.window_size)

        #Set green background
        self.screen.configure(bg="green")

        #Create a canvas so I can add a rectangle for scoreboard, pack lets the screen expand with the board centered
        self.canvas = tk.Canvas(self.screen, width = self.width, height = self.height, bg = "green")
        self.canvas.pack(expand=True)


        self.top_of_field = int(0.3*self.height)
        #The rectangle is 30% of the field---> change the value right above this (0.3) to adjust
        #Create a giant black rectangle to make scoreboard on
        self.scoreboard_bg = self.canvas.create_rectangle(0,0,self.width,self.top_of_field, fill = "black" )


        #Creates 2 goals on either side of the field that take up 1/3 of the width
        self.goal_1_bg = self.canvas.create_rectangle(0,(((self.height-self.top_of_field)//3)+self.top_of_field), int(self.width*0.02), (((self.height-self.top_of_field)//3)*2+self.top_of_field), fill = "black")
        self.goal_2_bg = self.canvas.create_rectangle(self.width,(((self.height-self.top_of_field)//3)+self.top_of_field), int(self.width*0.98), (((self.height-self.top_of_field)//3)*2+self.top_of_field), fill = "black")
        

        #Creates an outline of the field and green field.
        self.field_outline = self.canvas.create_rectangle(self.width*0.02,self.top_of_field, self.width*0.98,self.height, outline = "white", fill="green")

        #Creates text for the top of the scoreboard for the robot and human labels
        self.scoreboard_text= self.canvas.create_text(self.width*0.25,self.top_of_field//2,text="human", fill="white", font=("Impact",40)) 
        self.scoreboard_text= self.canvas.create_text(self.width*0.75,self.top_of_field//2,text="robot", fill="white", font=("Impact",40)) 


        #displays current score on scoreboard
        self.human_scoreboard_text = self.canvas.create_text(self.width*0.1, self.top_of_field//2, text= self.human_score, fill = "white", font = ("Impact",55))
        self.robot_scoreboard_text = self.canvas.create_text(self.width*0.9, self.top_of_field//2, text= self.robot_score, fill = "white", font = ("Impact",55))
        

        #initialize the timer on the scoreboard
        self.timer_text = self.canvas.create_text(self.width*0.5, self.top_of_field//2, text= "0:00",fill="blue",font=("Impact",50) )

        self.color = "red"
        self.ball = self.canvas.create_oval(self.ball_x-15,self.ball_y-15,self.ball_x+15,self.ball_y+15, fill="magenta", state="normal")
        self.waiting_screen = self.canvas.create_rectangle(0,self.top_of_field,self.width,self.height, fill="red", state="hidden")
        self.waiting_text = self.canvas.create_text (self.width//2,self.height//2,text="Place the ball in the enclosure,\n then press the start button.", fill="black",font=("Impact",40),state="hidden")
        self.game_over_screen = self.canvas.create_rectangle(0,self.top_of_field,self.width,self.height, fill=self.color, state="hidden")
        self.game_over_text = self.canvas.create_text (self.width//2,self.height//2,text=" wins!\nTo play again, press the start button.", fill="black",font=("Impact",40),state="hidden")
        self.fps_text = self.canvas.create_text(self.width//2, self.height//2,text="", font=("impact",80))




        self.screen.after(50,self.active_state)

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------




    #used to convert timer into text format
    def format_time(self, seconds):
        mins = seconds//60
        secs = seconds % 60
        return f"{mins}:{secs:02d}"


    def clear_screen_events(self):
        
        #gets rid of waiting screen and text
        self.canvas.itemconfig(self.waiting_screen, state="hidden")
        self.canvas.itemconfig(self.waiting_text, state="hidden")
        #gets rid of game over screen
        self.canvas.itemconfig(self.game_over_screen, state="hidden")
        self.canvas.itemconfig(self.game_over_text, state="hidden")



    def update_timer(self):

        #basic timer ticking down
        print("UPDATE TIMER CALLED\n")
        print(f"TIME = {self.timer}")
        if self.timer > 0 and self.game_state == Game_States.PLAYING:
            self.timer -= 1


            #updates display
            self.canvas.itemconfig(self.timer_text,text=self.format_time(self.timer))


            #call this function again after second
            self.screen.after(1000, self.update_timer)



    #Writes the scoreboard with current vals because im tired of typing this
    def update_scores(self):
        self.canvas.itemconfig(self.robot_scoreboard_text,text=self.robot_score)
        self.canvas.itemconfig(self.human_scoreboard_text, text=self.human_score)



    #Used to after IDLE is exited to setup a new game
    def start_game(self):


        #make timer display 5mins
        self.timer = 60
        self.canvas.itemconfig(self.timer_text, text=self.format_time(self.timer))
        
        self.update_timer()

        #reset scores
        self.human_score = 0
        self.robot_score = 0
        self.update_scores()


        """MOVE TO WAITING STATE"""
        self.game_state = Game_States.WAITING
        
        self.enter_WAITING()

    # Resets all of the computer vision variables (RUN WHEN RESET IS PRESSED)
    def restart_cv(self):
        self.lost_counter = 0
        if self.vid != None:
            self.vid.release()

        self.vid, self.frame, self.v_width, self.v_height = my_cv.initalize_video(self.buffer, self.x_size, self.y_size)
        self.frame, self.tracker = my_cv.initalize_tracker(self.vid, self.frame, self.x_size, self.y_size, self.v_width, self.v_height, self.buffer, self.tgt_color)

        self.count = 0
        self.fps = 0
        self.prev = 0
        self.lost_counter = 0



    #run after any update function calls reset
    def reset(self):
        #reset basic vars
        self.timer = 0
        self.robot_score=0
        self.human_score=0
        self.update_scores()
        self.canvas.itemconfig(self.timer_text,text=self.format_time(self.timer))
        self.clear_screen_events()


        # Move all three player rods up
        self.goalie.up()
        self.defense.up()
        self.offense.up()

        # Reset Computer Vision Objects
        if hasattr(self, "vid"):
            self.vid.release()
        cv2.destroyAllWindows()

        """MOVE TO IDLE STATE"""
        self.game_state = Game_States.IDLE
    
    
    
    def goal(self,whom):
    #whom is a boolean which dicatates who scored,   TRUE FOR robot (ROBOT), FALSE FOR human (HUMAN)
        
        if whom == False:
            self.human_score+=1
            self.canvas.itemconfig(self.human_scoreboard_text, text=self.human_score)
        else:
            self.robot_score+=1
            self.canvas.itemconfig(self.robot_scoreboard_text, text=self.robot_score)


        """MOVE TO WAITING STATE"""
        self.enter_WAITING()
        self.game_state = Game_States.WAITING




    def ui_ball_pos(self, ball_pos):


        if ball_pos != None:
            
        #cord is a tuple containing the x,y cordinate of the ball.
        #Brandon code uses 0,0 as top left and 640,360 as bottom right

        #We want the y position of the ball to be the value to be below the scoreboard and provide a margin for the ball size
        #Convert Brandon coordinates tuple (x, y) to UI coordinates
            self.ball_x = self.width*0.02 + ball_pos[0] * ((self.width*0.98 - self.width*0.02)/640)
            self.ball_y = self.top_of_field + ball_pos[1] * ((self.height - self.top_of_field)/360)
            self.canvas.coords(self.ball,self.ball_x-15,self.ball_y-15,self.ball_x+15,self.ball_y+15 )
            self.canvas.itemconfig(self.ball, state="normal")

   

    def enter_WAITING(self):
        self.clear_screen_events()

        # Move all three player rods down, to begin playing
        self.goalie.down()
        self.defense.down()
        self.offense.down()


        #Move all Lines to center position and update current angles
        self.current_angle_goalie = 90
        self.current_angle_defense = 90
        self.current_angle_offense = 90

        self.offense.set_position(90,self.off_move_pin)
        self.defense.set_position(90,self.def_move_pin)
        self.goalie.set_position(90,self.goalie_move_pin)



        if self.ball != None:
            self.canvas.itemconfig(self.ball, state="hidden")

        #creates a waiting screen with instructions
        self.canvas.itemconfig(self.waiting_screen, state="normal")
        self.canvas.itemconfig(self.waiting_text,state="normal")

        self.canvas.update_idletasks()
        self.canvas.update()

        # Start the video object for openCV and get the ball's position
        self.restart_cv()
        self.count, self.tracker, self.fps, self.prev, self.ball_pos, self.lost_counter = my_cv.tracking_alg(
            self.vid, self.buffer, self.tracker,
            self.x_size, self.y_size, self.v_width, self.v_height,
            self.tgt_color, self.count, self.prev, self.fps, self.lost_counter)
        print(f"self.ball_pos = {self.ball_pos}")



    def game_over(self):
        self.clear_screen_events()


        if self.ball != None:
            self.canvas.itemconfig(self.ball, state="hidden")

        #determines winner
        if self.robot_score > self.human_score:
            self.winner = "Robot"
            self.color = "red"
        elif self.robot_score < self.human_score:
            self.winner = "Human"
            self.color = "green"
        else:
            self.winner = "Tie"
            self.color = "blue"

        #displays winner, also leaves scoreboard up
        self.canvas.itemconfig(self.game_over_screen, state="normal")
        self.canvas.itemconfig(self.game_over_text, state="normal",text=self.winner+" wins!\nTo play again, press the start button.")
        
        """MOVES TO IDLE"""
        print("Game Over")
        print("MODE CHANGED TO IDLE")
        self.game_state = Game_States.IDLE



    def start_pressed(self):
        self.screen.after(0, self._start_pressed_ui)


    def _start_pressed_ui(self):
        if self.game_state == Game_States.IDLE:
            print("Starting Game...")
            self.start_game()

        elif self.game_state == Game_States.WAITING:
            # If the ball is found, continue
            if self.ball_pos != None:
                self.clear_screen_events()
                print("MODE CHANGED TO PLAYING")
                self.game_state = Game_States.PLAYING
                self.update_timer()
            else:
                print("Ball not found?")
            # If the ball is not found, do not switch to playing

        elif self.game_state == Game_States.PLAYING:
            self.enter_WAITING()
            print("MODE CHANGED TO WAITING")
            self.game_state = Game_States.WAITING


    def reset_pressed(self):
        self.screen.after(0,self._reset_pressed_ui)
        

    def _reset_pressed_ui(self):
        if self.game_state == Game_States.PLAYING:
            self.reset()
            print("MODE CHANGED TO IDLE")
            self.game_state = Game_States.IDLE

        elif self.game_state == Game_States.WAITING:
            self.reset()
            print("MODE CHANGED TO IDLE")
            self.game_state = Game_States.IDLE


    def human_goal(self):
        self.screen.after(0,self._human_goal_ui)

    def _human_goal_ui(self):
        if self.game_state == Game_States.PLAYING:
            self.goal(False)
    
    def robot_goal(self):
        self.screen.after(0,self._robot_goal_ui)

    def _robot_goal_ui(self):
        if self.game_state == Game_States.PLAYING:
            self.goal(True)
    

    def kick_helper(self, player_line: pc.Player_line):
        if not player_line.is_kicking:
            player_line.is_kicking = True   # Prevent's multiple kick attempts during the kick
            player_line.kick_start()
            # These commands tell tkinter to run the referenced functions after x amount of miliseconds
            self.screen.after(200, player_line.kick_followthrough)
            self.screen.after(400, player_line.kick_reset)
            
        

    def update_IDLE(self):
        pass



    def update_WAITING(self):
        # Check interupts
        pass



    def update_PLAYING(self):
        # Step 1: Track the ball
        self.count, self.tracker, self.fps, self.prev, self.ball_pos, self.lost_counter = my_cv.tracking_alg(
            self.vid, self.buffer, self.tracker,
            self.x_size, self.y_size, self.v_width, self.v_height,
            self.tgt_color, self.count, self.prev, self.fps, self.lost_counter)

        print(f"\nCurrent Ball Pos: {self.ball_pos}\n")

        # Step 2: Use the new position to move the Players
        if self.ball_pos != None:
            cmd_array = pps.update_player_pos(self.ball_pos)

            #Linear motion of the lines
            self.current_angle_goalie = self.goalie.smooth_move(cmd_array[0][0],self.current_angle_goalie)
            print(f"goalie move {self.current_angle_goalie}")
            self.current_angle_offense = self.offense.smooth_move(cmd_array[2][0],self.current_angle_offense)
            print(f"offense move {self.current_angle_goalie}")
            self.current_angle_defense = self.defense.smooth_move(cmd_array[1][0],self.current_angle_defense)
            print(f"defense move {self.current_angle_goalie}")

            #kicking function of the lines
            if cmd_array[0][1] == True:
                self.kick_helper(self.goalie)
                print("goalie kick")
            if cmd_array[1][1] == True:
                self.kick_helper(self.defense)
                print("defense kick")
            if cmd_array[2][1] == True:
                self.kick_helper(self.offense)
                print("offense kick")
                    
                

        # Step 2.5: Update the ball on the ui
        self.ui_ball_pos(self.ball_pos)


        # Step 3: Check for interupts
        if self.timer <= 0:         # Has a timer run out?
            self.game_over()



    #Calls itself constantly to run whatever services are needed for each state
    def active_state(self):
        if self.game_state == Game_States.IDLE:
            self.update_IDLE()
            print("IDLE UPDATED")
        elif self.game_state == Game_States.PLAYING:
            print("PLAYING UPDATED")
            self.update_PLAYING()
        else:
            print("WAITING UPDATED")
            self.update_WAITING()

        self.canvas.itemconfig(self.fps_text, text=round(self.fps))

        
        #THIS VARIABLE IS THE SPEED AT WHICH THE GAME WILL RUN, CURRENTLY 50ms PER LOOP
        self.screen.after(25,self.active_state)

    


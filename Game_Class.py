import tkinter as tk
import gpiozero
import ComputerVision as my_cv
import cv2
import PlayerPositions as pps
from enum import Enum
import Laser_Activities as pew
import Player_Control as pc

 
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
        self.home_score = 0
        self.away_score = 0


        #time in seconds
        self.timer = 0 
        self.timer_running = False


        #****************************WE MAY NEED TO PICK A DIFFERENT PIN HERE*********************************************
        #makes the start button GPIO pin 3, reset gpio 2 
        self.start_button = gpiozero.Button(5)
        self.reset_button = gpiozero.Button(6)

        self.start_button.when_activated = self.start_pressed
        self.reset_button.when_activated = self.reset_pressed



        #*****************************THESE PINS MAY ALSO NEED TO BE CHANGED******************************************
        #creates the two laser systems for the goals according to the laser activities class structure
        #pin one is reciever, pin two is laser
        home_goal_recv_pin = 4
        home_goal_lazer_pin = 23
        self.home_goal = pew.Goal(home_goal_recv_pin,home_goal_lazer_pin)

        away_goal_recv_pin = 25
        away_goal_lazer_pin = 24
        self.away_goal = pew.Goal(away_goal_recv_pin,away_goal_lazer_pin)
        
        #*****************************PLAYER DECLERATIONS******************************************
        goalie_move_pin = 13
        goalie_kick_pin = 19
        self.goalie = pc.Player_Line(goalie_move_pin, goalie_kick_pin)

        def_move_pin = 18
        def_kick_pin = 12
        self.defense = pc.Player_Line(def_move_pin, def_kick_pin)
        
        off_move_pin = 21
        off_kick_pin = 20
        self.offense = pc.Player_Line(off_move_pin, off_kick_pin)


        #init the game state using enum types
        self.game_state = Game_States.IDLE

    #--------------------------------------------------------------------------------------------------------------------


    #____________________________BRANDON PARAMETERS FOR CV  (copied from main.py, not sure if needed)______________________________________________________
        
        # ADJUSTABLE PARAMETERS
        self.buffer = 5  # The ammount of additional pixels to add to the ROI to ensure the object is in frame of the tracker

        self.tgt_color = (121, 46, 130)     # The objects target color (Blue, Green, Red)
            # Sensitivity and ROI Area bounds can be adjusted within the function

        # CROPPING Values are in the pull_frame function

        '''
        CUSTOMIZE YOUR RENDER SIZE:
            Default is: (640, 360)
        '''

        self.x_size = 640
        self.y_size = 360


    #________________________________________________________________________________________________________________________


    #----------------------------------Initializing display, adding visual features----------------------------------------------------------------------

        #Create the main window
        self.screen = tk.Tk()
       
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

        #Creates text for the top of the scoreboard for the away and home labels
        self.scoreboard_text= self.canvas.create_text(self.width*0.25,self.top_of_field//2,text="HOME", fill="white", font=("Impact",40)) 
        self.scoreboard_text= self.canvas.create_text(self.width*0.75,self.top_of_field//2,text="AWAY", fill="white", font=("Impact",40)) 


        #displays current score on scoreboard
        self.home_scoreboard_text = self.canvas.create_text(self.width*0.1, self.top_of_field//2, text= self.home_score, fill = "white", font = ("Impact",55))
        self.away_scoreboard_text = self.canvas.create_text(self.width*0.9, self.top_of_field//2, text= self.away_score, fill = "white", font = ("Impact",55))
        

        #initialize the timer on the scoreboard
        self.timer_text = self.canvas.create_text(self.width*0.5, self.top_of_field//2, text= "0:00",fill="blue",font=("Impact",50) )

        self.color = "red"
        self.ball = self.canvas.create_oval(self.ball_x-15,self.ball_y-15,self.ball_x+15,self.ball_y+15, fill="magenta", state="hidden")
        self.waiting_screen = self.canvas.create_rectangle(0,self.top_of_field,self.width,self.height, fill="red", state="hidden")
        self.waiting_text = self.canvas.create_text (self.width//2,self.height//2,text="Place the ball in the enclosure,\n then press the start button.", fill="black",font=("Impact",40),state="hidden")
        self.game_over_screen = self.canvas.create_rectangle(0,self.top_of_field,self.width,self.height, fill=self.color, state="hidden")
        self.game_over_text = self.canvas.create_text (self.width//2,self.height//2,text=" wins!\nTo play again, press the start button.", fill="black",font=("Impact",40),state="hidden")

        self.screen.after(50,self.active_state)
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        #runs the loop
        #CHAT SAID TO COMMENT THIS AS IT doesnt work
        #self.screen.mainloop()



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
        self.canvas.itemconfig(self.away_scoreboard_text,text=self.away_score)
        self.canvas.itemconfig(self.home_scoreboard_text, text=self.home_score)



    #Used to after IDLE is exited to setup a new game
    def start_game(self):


        # Start the video object for openCV
        self.restart_cv()

        #make timer display 5mins
        self.timer = 300
        self.canvas.itemconfig(self.timer_text, text=self.format_time(self.timer))
        
        self.update_timer()

        #reset scores
        self.home_score = 0
        self.away_score = 0
        self.update_scores()

        self.away_goal.on()
        self.home_goal.on()

        # Move all three player rods down, to begin playing
        self.goalie.down()
        self.defense.down()
        self.offense.down()

        """MOVE TO WAITING STATE"""
        self.enter_WAITING()
        self.game_state = Game_States.WAITING

    # Resets all of the computer vision variables (RUN WHEN RESET IS PRESSED)
    def restart_cv(self):
        self.vid, self.frame, self.v_width, self.v_height = my_cv.initalize_video(self.buffer, self.x_size, self.y_size)
        self.frame, self.tracker = my_cv.initalize_tracker(self.vid, self.frame, self.x_size, self.y_size, self.v_width, self.v_height, self.buffer, self.tgt_color)

        self.count = 0
        self.fps = 0
        self.prev = 0



    #run after any update function calls reset
    def reset(self):
        #reset basic vars
        self.timer = 0
        self.away_score=0
        self.home_score=0
        self.update_scores()
        self.canvas.itemconfig(self.timer_text,text=self.format_time(self.timer))
        self.away_goal.on()
        self.home_goal.on()
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
    #whom is a boolean which dicatates who scored,   TRUE FOR AWAY (ROBOT), FALSE FOR HOME (HUMAN)
        
        if whom == False:
            self.home_score+=1
            self.canvas.itemconfig(self.home_scoreboard_text, text=self.home_score)
        else:
            self.away_score+=1
            self.canvas.itemconfig(self.away_scoreboard_text, text=self.away_score)

        #turn goals off after goal is scored
        self.away_goal.off()
        self.home_goal.off()


        """MOVE TO WAITING STATE"""
        self.enter_WAITING()
        self.game_state = Game_States.WAITING



    #if goal is scored, calls goal, with correct team   -> TRUE FOR AWAY, FALSE FOR HOME
    def was_goal_scored(self):
        if self.away_goal.is_goal():
            self.goal(True)
        elif self.home_goal.is_goal():
            self.goal(False)



    def ui_ball_pos(self, ball_pos):


        if ball_pos != None:
            
            self.canvas.delete(self.ball)
        #cord is a tuple containing the x,y cordinate of the ball.
        #Brandon code uses 0,0 as top left and 640,360 as bottom right

        #We want the y position of the ball to be the value to be below the scoreboard and provide a margin for the ball size
        #Convert Brandon coordinates tuple (x, y) to UI coordinates
            self.ball_x = self.width*0.02 + ball_pos[0] * ((self.width*0.98 - self.width*0.02)/640)
            self.ball_y = self.top_of_field + ball_pos[1] * ((self.height - self.top_of_field)/360)

            self.ball=self.canvas.create_oval(self.ball_x-15,self.ball_y-15,self.ball_x+15,self.ball_y+15, fill="magenta", state="normal")

   

    def enter_WAITING(self):
        self.clear_screen_events()
        #creates a waiting screen with instructions
        self.canvas.itemconfig(self.waiting_screen, state="normal")
        self.canvas.itemconfig(self.waiting_text,state="normal")



    def game_over(self):
        self.clear_screen_events()


        #determines winner
        if self.away_score > self.home_score:
            self.winner = "Robot"
            self.color = "red"
        elif self.away_score < self.home_score:
            self.winner = "Human"
            self.color = "green"
        else:
            self.winner = "Tie"
            self.color = "blue"

        #displays winner, also leaves scoreboard up
        self.canvas.itemconfig(self.game_over_screen, state="normal")
        self.canvas.itemconfig(self.game_over_text, state="normal")
        
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
            self.clear_screen_events()
            print("MODE CHANGED TO PLAYING")
            self.game_state = Game_States.PLAYING
            self.update_timer()

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

        

    def update_IDLE(self):
        pass



    def update_WAITING(self):
        # Check interupts
        pass



    def update_PLAYING(self):
        # Step 1: Track the ball
        self.count, self.tracker, self.fps, self.prev, self.ball_pos = my_cv.tracking_alg(
            self.vid, self.buffer, self.tracker, 
            self.x_size, self.y_size, self.v_width, self.v_height, 
            self.tgt_color, self.count, self.prev, self.fps)
        
        print(f"\nCurrent Ball Pos: {self.ball_pos}\n")

        # Step 2: Use the new position to move the Players
        pps.update_player_pos(self.ball_pos, self.goalie, self.defense, self.offense)


        # Step 2.5: Update the ball on the ui
        self.ui_ball_pos(self.ball_pos)


        # Step 3: Check for interupts
        self.was_goal_scored()      # Was a goal scored?
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

        #THIS VARIABLE IS THE SPEED AT WHICH THE GAME WILL RUN, CURRENTLY 50ms PER LOOP
        self.screen.after(50,self.active_state)

    


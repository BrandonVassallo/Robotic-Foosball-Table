import tkinter as tk
import gpiozero
import ComputerVision as my_cv
import PlayerPositions
from enum import Enum

#import Recalibration
 
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


class Background:

    def __init__(self):
    #-------------Setting up values needed later------------------------------------------------------------------------

        #These values will need to be tweaked in the future!!!!!!!  Changes all window sizes -> and shapes
        self.window_size = "800x400"
        self.width = 800
        self.height = 400


        #scores will be 0-0 in initialization, used to track score of the game
        self.home_score = 0
        self.away_score = 0


        #time in seconds
        self.timer = 0 
        self.timer_running = False


        #****************************WE MAY NEED TO PICK A DIFFERENT PIN HERE*********************************************
        #makes the start button GPIO pin 3, reset gpio 2 
        self.start_button = gpiozero.Button(3)
        self.reset_button = gpiozero.Button(2)


        #init the game state using enum types
        self.game_state = Game_States.IDLE

    #--------------------------------------------------------------------------------------------------------------------


    #____________________________BRANDON PARAMETERS FOR CV  (copied from main.py, not sure if needed)______________________________________________________
        
        # ADJUSTABLE PARAMETERS
        self.buffer = 5  # The ammount of additional pixels to add to the ROI to ensure the object is in frame of the tracker

        self.tgt_color = (121, 46, 202) # The objects target color (Blue, Green, Red)
            # Sensitivity and ROI Area bounds can be adjusted within the function

        # CROPPING Values are in the pull_frame function

        '''
        CUSTOMIZE YOUR RENDER SIZE:
            Default is: (640, 360)
        '''

        self.x_size = 640
        self.y_size = 360

        self.vid, self.frame, self.v_width, self.v_height = my_cv.initalize_video(self.buffer, self.x_size, self.y_size)
        self.frame, self.tracker = my_cv.initalize_tracker(self.vid, self.frame, self.x_size, self.y_size, self.v_width, self.v_height, self.buffer, self.tgt_color)

        self.count = 0
        self.fps = 0
        self.prev = 0

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

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        #runs the loop
        self.screen.mainloop()



    #used to convert timer into text format
    def format_time(self, seconds):
        mins = seconds//60
        secs = seconds % 60
        return f"{mins}:{secs:02d}"



    def update_timer(self):

        #basic timer ticking down
        if self.timer > 0 and self.game_state == Game_States.PLAYING:
            self.timer -= 1


            #updates display
            self.canvas.itemconfig(self.timer_text,text=self.format_time(self.timer))


            #call this function again after second
            self.screen.after(1000, self.update_timer)
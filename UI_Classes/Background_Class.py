import tkinter as tk

#To whom it may concern:

"""

I have made this entire UI scalable to the best of my ability. We will need to get better measurements
of the screen in order to have it fit correctly. The only values you *should* need to change are:
    
    self.window_size
    self.width
    self.height
    
All of these values are at the top of the init class. The main functions will be init,
away_goal, home_goal, ball_lost, press_start, and reset/recalibration
      
"""

class Background:

    def __init__(self):

        #These values will need to be tweaked in the future!!!!!!!  Changes all window sizes -> and shapes
        self.window_size = "800x400"
        self.width = 800
        self.height = 400

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
        

        #Creates an outline of the field
        self.field_outline = self.canvas.create_rectangle(self.width*0.02,self.top_of_field, self.width*0.98,self.height, outline = "white")

        #Creates text for the top of the scoreboard for the away and home labels
        self.scoreboard_text= self.canvas.create_text(self.width*0.25,self.top_of_field//2,text="HOME", fill="white", font=("Impact",40)) 
        self.scoreboard_text= self.canvas.create_text(self.width*0.75,self.top_of_field//2,text="AWAY", fill="white", font=("Impact",40)) 



        #scores will be 0-0 in initialization, used to track score of the game
        self.home_score = 0
        self.away_score = 0

        #displays current score on scoreboard
        self.scoreboard_text = self.canvas.create_text(self.width*0.1, self.top_of_field//2, text= self.home_score, fill = "white", font = ("Impact",55))
        self.scoreboard_text = self.canvas.create_text(self.width*0.9, self.top_of_field//2, text= self.away_score, fill = "white", font = ("Impact",55))
        



        self.screen.mainloop()












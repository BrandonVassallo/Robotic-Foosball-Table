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
        screen = tk.Tk()
       
        #Name the window
        screen.title("Jumbotron")

        #Set window size
        screen.geometry(self.window_size)

        #Set green background
        screen.configure(bg="green")

        #Create a canvas so I can add a rectangle for scoreboard, don't know why I need pack
        canvas = tk.Canvas(screen, self.width, self.height)
        canvas.pack()

        #Create a giant black rectangle to make scoreboard on
        scoreboard_bg = canvas.create_rectangle(0,0,self.width,int(0.3*self.height), fill = "black" )

        










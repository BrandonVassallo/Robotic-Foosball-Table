import tkinter as tk
import gpiozero


#TODO
"""
-Goal scored function
-ball_lost screen
-reset fxn
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

class Background:

    def __init__(self):

        #These values will need to be tweaked in the future!!!!!!!  Changes all window sizes -> and shapes
        self.window_size = "800x400"
        self.width = 800
        self.height = 400


        self.start_button = gpiozero.button(3)

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


        #scores will be 0-0 in initialization, used to track score of the game
        self.home_score = 0
        self.away_score = 0

        #displays current score on scoreboard
        self.home_scoreboard_text = self.canvas.create_text(self.width*0.1, self.top_of_field//2, text= self.home_score, fill = "white", font = ("Impact",55))
        self.away_scoreboard_text = self.canvas.create_text(self.width*0.9, self.top_of_field//2, text= self.away_score, fill = "white", font = ("Impact",55))
        
        #time in seconds
        self.timer = 0 

        #initialize the timer on the scoreboard
        self.timer_text = self.canvas.create_text(self.width*0.5, self.top_of_field//2, text= "0:00",fill="blue",font=("Impact",50) )


        self.screen.mainloop()



    #used to convert timer into text format
    def format_time(self, seconds):
        mins = seconds//60
        secs = seconds % 60
        return f"{mins}:{secs:02d}"



    def update_timer(self):
        if self.timer > 0:
            self.timer -= 1

            #updates display
            self.canvas.itemconfig(self.timer_text,text=self.format_time(self.timer))

            #call this function again after second
            self.screen.after(1000, self.update_timer)



    def wait_for_ball(self):
        
        #creates a waiting screen with instructions
        self.waiting_screen = self.canvas.create_rectangle(0,0,self.width,self.height, fill="red")
        self.waiting_text = self.canvas.create_text (text="Place the ball in the enclosure, then press the ball button.", fill="black",font=("Impact",80))

        #Halts code until the button is pressed. You must press this button AFTER the ball is in the field.
        self.start_button.wait_for_press()

        #gets rid of waiting screen and text
        self.canvas.delete(self.waiting_screen)
        self.canvas.delete(self.waiting_text)


    
    def start_game(self):

        #make timer display 5mins but do not begin updating yet, I think that function will call itself a ton
        self.timer = 300
        self.canvas.itemconfig(self.timer_text, text=self.format_time(self.timer))

        self.wait_for_ball()

        self.update_timer()









    






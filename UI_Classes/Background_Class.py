import tkinter as tk
import gpiozero
#import Recalibration
 
 #Need to make recalibrate class in seperate file

#TODO
"""
-ball position update
-player position update
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

        #makes the start button GPIO pin 3 -----> this button is used to move the game out of the waiting for ball state 
        self.start_button = gpiozero.Button(3)

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
        self.timer_running = False

        #initialize the timer on the scoreboard
        self.timer_text = self.canvas.create_text(self.width*0.5, self.top_of_field//2, text= "0:00",fill="blue",font=("Impact",50) )

        #init ball, will make visible later in code when it is needed
        self.ball = self.canvas.create_oval(self.width//2,self.height//2,self.width//2+30,self.height//2+30, fill = "magenta", state="hidden")

        self.screen.mainloop()



    #used to convert timer into text format
    def format_time(self, seconds):
        mins = seconds//60
        secs = seconds % 60
        return f"{mins}:{secs:02d}"



    def update_timer(self):

        #basic timer ticking down
        if self.timer > 0 and self.timer_running==True:
            self.timer -= 1

            #updates display
            self.canvas.itemconfig(self.timer_text,text=self.format_time(self.timer))

            #call this function again after second
            self.screen.after(1000, self.update_timer)

        #If time is up, call game over fxn
        if self.timer <= 0:
            self.canvas.itemconfig(self.timer_text,text=self.format_time(self.timer))
            self.timer_running=False
            #game_over(self)



    #run when we need to wait for human to put ball in arena ----> can also call when the CV seriously loses ball
    def wait_for_ball(self):

        #stop the timer
        self.timer_running = False
        
        #creates a waiting screen with instructions
        self.waiting_screen = self.canvas.create_rectangle(0,0,self.width,self.height, fill="red")
        self.waiting_text = self.canvas.create_text (text="Place the ball in the enclosure, then press the ball button.", fill="black",font=("Impact",80))

        #Halts code until the button is pressed. You must press this button AFTER the ball is in the field.
        self.start_button.wait_for_press()

        #gets rid of waiting screen and text
        self.canvas.delete(self.waiting_screen)
        self.canvas.delete(self.waiting_text)

        #start the timer again
        self.timer_running = True



    def start_game(self):

        #recalibrate()

        #make timer display 5mins
        self.timer = 300
        self.canvas.itemconfig(self.timer_text, text=self.format_time(self.timer))
        self.timer_running = False

        self.wait_for_ball()

        self.update_timer()

    

    def reset(self):
        #reset basic vars
        self.timer_running = False
        self.timer = 0
        self.away_score=0
        self.home_score=0
        self.canvas.itemconfig(self.timer_text,text=self.format_time(self.timer))

        #start new game
        self.start_game()



    def goal(self,whom):
    #whom is a boolean which dicatates who scored,   TRUE FOR HOME (ROBOT), FALSE FOR AWAY (HUMAN)
        
        self.timer_running = False

        if whom == True:
            self.home_score+=1
            self.canvas.itemconfig(self.home_scoreboard_text, text=self.home_score)
        else:
            self.away_score+=1
            self.canvas.itemconfig(self.away_scoreboard_text, text=self.away_score)

        self.wait_for_ball()

    
    
    def ball_pos(self, cord):
        #cord is a tuple containing the x,y cordinate of the ball.
        #Brandon code uses 0,0 as top left and 640,360 as bottom right

        #We want the y position of the ball to be the value to be below the scoreboard and provide a margin for the ball size
        self.ball_y = int(cord[1])+self.top_of_field+15
    #TODO - Finish this
        


    def game_over(self):
        
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
        self.game_over_screen = self.canvas.create_rectangle(0,self.top_of_field,self.width,self.height, fill=self.color)
        self.game_over_text = self.canvas.create_text (text=self.winner+" wins!\nTo play again, press the start button.", fill="black",font=("Impact",80))

        #wait for them to hit start
        self.start_button.wait_for_press()

        #gets rid of waiting screen and text
        self.canvas.delete(self.game_over_screen)
        self.canvas.delete(self.game_over_text)

        self.start_game()









    






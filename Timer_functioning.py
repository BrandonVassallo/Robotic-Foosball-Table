import tkinter as tk
import time

# Create the main window
root = tk.Tk()
root.title("Display")

# Set window size
root.geometry("800x400")

# Set green background
root.configure(bg="green")

# Label to display the timer
label = tk.Label(root, text="", font=("Ariel", 60), bg="green", fg="white")
label.pack(expand=True)


start_time = 300 #currently 5 mins for a game, we can alter by inputing number of seconds

def update_timer():
    global start_time

    if start_time>=0:

        minutes = start_time// 60
        seconds = start_time % 60
        label.config(text=f"{minutes:02}:{seconds:02}")
        start_time -= 1    #reduces start time
        root.after(1000, update_timer)  # update every second

    if start_time<0:
        label.config(text=f"Game Over")


# Start the timer
update_timer()

# Run the window
root.mainloop()
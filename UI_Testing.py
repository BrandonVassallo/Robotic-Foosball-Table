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
label = tk.Label(root, text="", font=("Wingdings", 60), bg="green", fg="white")
label.pack(expand=True)


start_time = 60

#start time and elapsed time currently not interacting!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def update_timer():

    if(elapsed_time>0):
        elapsed_time = int(elapsed_time - 1)
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    label.config(text=f"{minutes:02}:{seconds:02}")
    root.after(1000, update_timer)  # update every second

# Start the timer
update_timer()

# Run the window
root.mainloop()
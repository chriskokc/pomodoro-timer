from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- # 


def reset_timer():
    """
    this function resets the timer as users click the reset button
    """
    # cancel the timer to avoid it keep running in the background
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer")
    # reset check_marks
    check_mark_label.config(text="")
    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- # 


def start_timer():
    """
    this function starts counting time as users click the start button
    """
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # figure out which Pomodoro session we are currently at
    # and then we decide the appropriate text (i.e work or break) to show,
    # and input the correct counting time into the count_down method
    # if it's the 8th rep:
    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="Break", fg=RED)
    # if it's 2nd/4th/6th rep:
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="Break", fg=PINK)
    # if it's the 1st/3rd/5th/7th rep:
    else:
        count_down(work_sec)
        title_label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    """
    this function takes an integer, which is the time to count in seconds,
    and keeps refreshing the UI element (i.e canvas text) to display the counting time
    """
    count_min = math.floor(count / 60)
    count_sec = count % 60

    # display 00:00, 00:01, 00:02 etc. in the timer
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    # modify the canvas text for showing time
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    # if it is counting time
    if count > 0:
        global timer
        # a method that execute a command after a time delay (i.e 1000 ms)
        # it calls itself (i.e count_down method) again so that the canvas text can keep refreshing
        timer = window.after(1000, count_down, count - 1)
    # if the count is over
    else:
        # we switch to the next Pomodoro session and starts counting again
        start_timer()
        marks = ""
        # e.g when reps is 4, we have: work, break, work, break, i.e 2 work sessions
        work_session = math.floor(reps/2)
        # display a mark to remind users how many work sessions have been completed
        for _ in range(work_session):
            marks += "✔️"
        check_mark_label.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

# Canvas widget
# create a canvas, size in pixels
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)

# load the .gif image file
tomato_img = PhotoImage(file="tomato.png")

# put gif image on canvas
canvas.create_image(100, 112, image=tomato_img)

# put a text on canvas
# assign the canvas text to a variable
timer_text = canvas.create_text(103, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))

canvas.grid(column=1, row=1)

# Timer label
title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 45, "bold"))
title_label.grid(column=1, row=0)

# Check mark label
check_mark_label = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 25, "bold"))
check_mark_label.grid(column=1, row=3)

# Start button
start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

# Reset button
reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

window.mainloop()
from tkinter import *
from random import choice
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# ---------- Functions ----------

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(to_learn)
    canvas.itemconfig(canvas_image, image=front_card_img)
    canvas.itemconfig(canvas_title, text="French", fill="black")
    canvas.itemconfig(canvas_word, text=current_card["French"], fill="black")

    flip_timer = window.after(3000, back_card)


def back_card():
    canvas.itemconfig(canvas_image, image=back_card_img)
    canvas.itemconfig(canvas_title, text="English", fill="white")
    canvas.itemconfig(canvas_word, text=current_card["English"], fill="white")


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("./data/words_to_learn.csv", index=False)

    next_card()


# ---------- UI ----------

window = Tk()
window.title("Flashy")
window.config(padx= 50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, back_card)

canvas = Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0)
back_card_img = PhotoImage(file="./images/card_back.png")
front_card_img = PhotoImage(file="./images/card_front.png")
canvas_image = canvas.create_image(400, 263, image=front_card_img)
canvas_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, 'italic'))
canvas_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, 'bold'))
canvas.grid(column=0, row=0, columnspan=2)

cross_image = PhotoImage(file='./images/wrong.png')
cross_button = Button(image=cross_image, highlightthickness=0, command=next_card)
cross_button.grid(column=0, row=1)

check_image = PhotoImage(file="./images/right.png")
check_button = Button(image=check_image, highlightthickness=0, command=is_known)
check_button.grid(column=1, row=1)

next_card()

window.mainloop()

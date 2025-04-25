from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"


french_words = pandas.read_csv("data/french_words.csv")
french_to_english_dict = {row.French: row.English for (index,row) in french_words.iterrows()}
random_french_word = None
known_french_words = {}
french_words_still_to_learn = french_to_english_dict

def pick_random_french_word():
    global random_french_word, flip_timer
    window.after_cancel(flip_timer)

    random_french_word = random.choice(list(french_to_english_dict.keys()))
    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=f"{random_french_word}", fill="black")

    flip_timer = window.after(3000, func=swap_cards)

def pick_random_french_word_right():
    with open(file="words_to_learn.csv", mode="w") as words_to_learn:
        words_to_learn.write("")
    global random_french_word, flip_timer
    window.after_cancel(flip_timer)
    known_french_words[random_french_word] = french_to_english_dict[random_french_word]
    for key, value in known_french_words.items():
        if key in french_to_english_dict.keys():
            del french_words_still_to_learn[key]
    if len(french_words_still_to_learn) > 0:
        random_french_word = random.choice(list(french_words_still_to_learn.keys()))
    else:
        random_french_word = random.choice(list(known_french_words.keys()))
    for key,value in french_words_still_to_learn.items():
        with open(file="words_to_learn.csv", mode="a") as words_to_learn:
            words_to_learn.write(f"{key}, {value}\n")

    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=f"{random_french_word}", fill="black")

    flip_timer = window.after(3000, func=swap_cards)

def swap_cards():
    global random_french_word
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=f"{french_to_english_dict[random_french_word]}", fill="white")






window = Tk()
window.title("Flashy")
window.config(padx=75, pady=75, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=swap_cards)

canvas = Canvas(width=820,height=550,highlightthickness=0, bg=BACKGROUND_COLOR)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(410,275,image=card_front)
title_text = canvas.create_text(410, 150, text="", font=("Arial", 30, "italic"))
word_text = canvas.create_text(410,275,text="", font=("Arial", 50, "bold"))
canvas.grid(column=0,row=0,columnspan=2)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=pick_random_french_word)
wrong_button.grid(column=0,row=1)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=pick_random_french_word_right)
right_button.grid(column=1,row=1)

pick_random_french_word()
window.mainloop()

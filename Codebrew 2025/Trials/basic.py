from tkinter import *
import pandas as pd
import random

# Constants
BACKGROUND_COLOR = "#B1DDC6"
FONT_TITLE = ("Arial", 30, "italic")
FONT_WORD = ("Arial", 50, "bold")

# Load Data
french_words = pd.read_csv("data/french_words.csv")
french_to_english_dict = {row.French: row.English for _, row in french_words.iterrows()}
known_french_words = {}
french_words_still_to_learn = french_to_english_dict.copy()

# Global Variables
random_french_word = None
showing_french = True  # Tracks current card state

# Initialize Tkinter Window
window = Tk()
window.title("Flashy")
window.config(padx=75, pady=75, bg=BACKGROUND_COLOR)

# UI Setup
canvas = Canvas(width=820, height=550, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(410, 275, image=card_front)
title_text = canvas.create_text(410, 150, text="", font=FONT_TITLE)
word_text = canvas.create_text(410, 275, text="", font=FONT_WORD)
canvas.grid(column=0, row=0, columnspan=2)

# Functions
def pick_random_french_word():
    """Pick a new random word and reset card to French side."""
    global random_french_word, showing_french

    if french_words_still_to_learn:
        random_french_word = random.choice(list(french_words_still_to_learn.keys()))
    else:
        random_french_word = random.choice(list(known_french_words.keys()))

    # Reset to French side
    showing_french = True
    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=random_french_word, fill="black")

def mark_word_as_known():
    """Mark the current word as known and remove it from the learning list."""
    global random_french_word

    if random_french_word in french_words_still_to_learn:
        known_french_words[random_french_word] = french_to_english_dict[random_french_word]
        del french_words_still_to_learn[random_french_word]

    with open("words_to_learn.csv", "w") as file:
        for key, value in french_words_still_to_learn.items():
            file.write(f"{key}, {value}\n")

    pick_random_french_word()

def flip_card(event):
    """Toggle between French and English when the card is clicked."""
    global showing_french
    showing_french = not showing_french  # Switch state

    if showing_french:
        canvas.itemconfig(canvas_image, image=card_front)
        canvas.itemconfig(title_text, text="French", fill="black")
        canvas.itemconfig(word_text, text=random_french_word, fill="black")
    else:
        canvas.itemconfig(canvas_image, image=card_back)
        canvas.itemconfig(title_text, text="English", fill="white")
        canvas.itemconfig(word_text, text=french_to_english_dict[random_french_word], fill="white")

# Bind click event to canvas
canvas.bind("<Button-1>", flip_card)  # Left-click on card to flip

# Buttons
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=pick_random_french_word)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=mark_word_as_known)
right_button.grid(column=1, row=1)

# Start the App
pick_random_french_word()
window.mainloop()
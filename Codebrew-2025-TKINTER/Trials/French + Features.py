from tkinter import *
import pandas as pd
import random

# Constants
BACKGROUND_COLOR = "#B1DDC6"
FONT_TITLE = ("Arial", 30, "italic")
FONT_WORD = ("Arial", 50, "bold")
FONT_COUNTER = ("Arial", 20, "bold")
FONT_END_SCREEN = ("Arial", 14, "bold")

# Load Data
french_words = pd.read_csv("data/french_words.csv")
french_to_english_dict = {row.French: row.English for _, row in french_words.iterrows()}
remaining_words = list(french_to_english_dict.keys())

# Global Variables
session_words = []
random_french_word = None
showing_french = True
session_counter = 0
SESSION_SIZE = 20
known_french_words = {}
unknown_french_words = {}

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
counter_text = canvas.create_text(410, 450, text="Words reviewed: 0/20", font=FONT_COUNTER)
canvas.grid(column=0, row=0, columnspan=2)

# Functions
def update_counter():
    """Update the counter display for the current session."""
    canvas.itemconfig(counter_text, text=f"Words reviewed: {session_counter}/{SESSION_SIZE}")

def reset_game():
    """Fully reset all data and restart the first session."""
    global remaining_words, known_french_words, unknown_french_words
    remaining_words = list(french_to_english_dict.keys())
    known_french_words.clear()
    unknown_french_words.clear()
    start_new_session()

def start_new_session():
    """Start the next batch of 20 words."""
    global session_words, session_counter

    if remaining_words:
        session_words = random.sample(remaining_words, min(SESSION_SIZE, len(remaining_words)))
        for word in session_words:
            remaining_words.remove(word)
        session_counter = 0
        pick_random_french_word()
    else:
        display_end_screen()

def pick_random_french_word():
    """Pick a new random word from the session batch."""
    global random_french_word, showing_french, session_counter

    if session_words:
        random_french_word = session_words.pop(0)
    else:
        display_session_review()
        return

    session_counter += 1
    update_counter()
    showing_french = True
    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=random_french_word, fill="black")

def mark_word(correct):
    """Mark words as known or unknown."""
    global random_french_word
    if correct:
        known_french_words[random_french_word] = french_to_english_dict[random_french_word]
    else:
        unknown_french_words[random_french_word] = french_to_english_dict[random_french_word]
    pick_random_french_word()

def flip_card(event):
    """Toggle between French and English when clicking the flashcard."""
    global showing_french
    showing_french = not showing_french

    if showing_french:
        canvas.itemconfig(canvas_image, image=card_front)
        canvas.itemconfig(title_text, text="French", fill="black")
        canvas.itemconfig(word_text, text=random_french_word, fill="black")
    else:
        canvas.itemconfig(canvas_image, image=card_back)
        canvas.itemconfig(title_text, text="English", fill="white")
        canvas.itemconfig(word_text, text=french_to_english_dict[random_french_word], fill="white")

def display_session_review():
    """Show a summary of the current session before loading the next batch."""
    review_window = Toplevel(window)
    review_window.title("Session Review")
    review_window.config(bg=BACKGROUND_COLOR)

    frame = Frame(review_window)
    frame.pack(fill=BOTH, expand=True)

    canvas_review = Canvas(frame, bg=BACKGROUND_COLOR)
    scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas_review.yview)
    scroll_frame = Frame(canvas_review, bg=BACKGROUND_COLOR)

    scroll_frame.bind("<Configure>", lambda e: canvas_review.configure(scrollregion=canvas_review.bbox("all")))
    canvas_review.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas_review.configure(yscrollcommand=scrollbar.set)

    canvas_review.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    Label(scroll_frame, text="Session Complete!", font=("Arial", 25, "bold"), bg=BACKGROUND_COLOR).pack(pady=10)
    Label(scroll_frame, text="Words You Knew (✓):", font=("Arial", 18), bg=BACKGROUND_COLOR).pack(pady=5)

    for french, english in known_french_words.items():
        Label(scroll_frame, text=f"✔ {french} → {english}", font=FONT_END_SCREEN, bg=BACKGROUND_COLOR).pack()

    Label(scroll_frame, text="Words You Missed (✗):", font=("Arial", 18), bg=BACKGROUND_COLOR).pack(pady=5)

    for french, english in unknown_french_words.items():
        Label(scroll_frame, text=f"✖ {french} → {english}", font=FONT_END_SCREEN, bg=BACKGROUND_COLOR).pack()

    Button(scroll_frame, text="Next Session", font=("Arial", 18), command=lambda: [review_window.destroy(), start_new_session()]).pack(pady=20)

def display_end_screen():
    """Show a final congratulatory message when all sessions are completed."""
    canvas.delete("all")
    canvas.create_text(410, 200, text="🎉 Congratulations! 🎉", font=("Arial", 40, "bold"), fill="green")
    canvas.create_text(410, 260, text="You've completed all words!", font=("Arial", 25), fill="black")

    Button(window, text="Restart", font=("Arial", 18), command=reset_game).place(x=360, y=500)

# Buttons
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=lambda: mark_word(False))
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=lambda: mark_word(True))
right_button.grid(column=1, row=1)

canvas.bind("<Button-1>", flip_card)

# Start the First Session
start_new_session()
window.mainloop()
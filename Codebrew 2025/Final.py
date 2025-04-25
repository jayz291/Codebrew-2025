from tkinter import *
import pandas as pd
import random
import pygame
pygame.mixer.init()

# Constants
BACKGROUND_COLOR = "#B1DDC6"
FONT_TITLE = ("Arial", 30, "italic")
FONT_WORD = ("Arial", 50, "bold")
FONT_COUNTER = ("Arial", 20, "bold")
FONT_END_SCREEN = ("Arial", 14, "bold")

# Language File Mapping
LANGUAGE_FILES = {
    "French": "French_words_to_learn.csv",
    "Latin": "Latin_words_to_learn.csv",
    "Chinese": "Chinese_words_to_learn.csv",
}

# Globals
session_words = []
word_dict = {}
remaining_words = []
random_word = None
showing_front = True
session_counter = 0
SESSION_SIZE = 20
known_words = {}
unknown_words = {}
selected_language = None

# GUI Elements to hold references
canvas = None
canvas_image = None
title_text = None
word_text = None
counter_text = None
wrong_button = None
right_button = None
restart_button = None
card_front_img = None
card_back_img = None
wrong_img = None
right_img = None

# Initialize Tkinter Window
window = Tk()
window.title("Flashy")
window.config(padx=75, pady=75, bg=BACKGROUND_COLOR)

# Load sound files
correct_sound = pygame.mixer.Sound("sounds/correct.mp3")
wrong_sound = pygame.mixer.Sound("sounds/wrong.mp3")
flip_sound = pygame.mixer.Sound("sounds/flip.mp3")
review_sound = pygame.mixer.Sound("sounds/review.mp3")

def load_words(language):
    global word_dict, remaining_words, selected_language, session_counter
    selected_language = language
    session_counter = 0

    file_path = LANGUAGE_FILES.get(language)
    try:
        words = pd.read_csv(file_path, encoding="utf-8")
        word_dict.clear()
        word_dict.update({str(row.iloc[0]): str(row.iloc[1]) for _, row in words.iterrows()})
        remaining_words.clear()
        remaining_words.extend(list(word_dict.keys()))
        setup_main_ui()
        start_new_session()
    except FileNotFoundError:
        print(f"Error: CSV file for {language} not found.")


def start_page():
    for widget in window.winfo_children():
        widget.destroy()
    Label(window, text="Choose a Language", font=("Arial", 25, "bold"), bg=BACKGROUND_COLOR).pack(pady=20)
    for language in LANGUAGE_FILES:
        Button(window, text=language, font=("Arial", 18), command=lambda lang=language: load_words(lang)).pack(pady=10)


def setup_main_ui():
    global canvas, canvas_image, title_text, word_text, counter_text
    global card_front_img, card_back_img, wrong_img, right_img, wrong_button, right_button, restart_button

    for widget in window.winfo_children():
        widget.destroy()

    card_front_img = PhotoImage(file="images/card_front.png")
    card_back_img = PhotoImage(file="images/card_back.png")
    wrong_img = PhotoImage(file="images/wrong.png")
    right_img = PhotoImage(file="images/right.png")

    canvas = Canvas(window, width=820, height=550, highlightthickness=0, bg=BACKGROUND_COLOR)
    canvas_image = canvas.create_image(410, 275, image=card_front_img)
    title_text = canvas.create_text(410, 150, text=selected_language, font=FONT_TITLE)
    word_text = canvas.create_text(410, 275, text="", font=FONT_WORD)
    counter_text = canvas.create_text(410, 450, text="Words reviewed: 0/20", font=FONT_COUNTER)
    canvas.grid(column=0, row=0, columnspan=2)

    canvas.bind("<Button-1>", flip_card)

    wrong_button = Button(window, image=wrong_img, highlightthickness=0, command=lambda: mark_word(False))
    wrong_button.grid(column=0, row=1)

    right_button = Button(window, image=right_img, highlightthickness=0, command=lambda: mark_word(True))
    right_button.grid(column=1, row=1)

    restart_button = Button(window, text="Back to Start", font=("Arial", 18), command=reset_game)
    restart_button.grid(column=0, row=2, columnspan=2, pady=20)


def update_counter():
    canvas.itemconfig(counter_text, text=f"Words reviewed: {session_counter}/{SESSION_SIZE}")


def reset_game():
    global known_words, unknown_words
    known_words.clear()
    unknown_words.clear()
    start_page()


def start_new_session():
    global session_words, session_counter
    known_words.clear()         # Reset known words for the new batch
    unknown_words.clear()       # Reset unknown words for the new batch

    if remaining_words:
        session_words = random.sample(remaining_words, min(SESSION_SIZE, len(remaining_words)))
        for word in session_words:
            remaining_words.remove(word)
        session_counter = 0
        pick_random_word()
    else:
        display_end_screen()



def pick_random_word():
    global random_word, showing_front, session_counter

    if session_words:
        random_word = session_words.pop(0)
    else:
        display_session_review()
        return

    session_counter += 1
    update_counter()
    showing_front = True
    canvas.itemconfig(canvas_image, image=card_front_img)
    canvas.itemconfig(title_text, text=selected_language, fill="black")
    canvas.itemconfig(word_text, text=random_word, fill="black")


def mark_word(correct):
    global random_word
    if correct:
        correct_sound.play()
        known_words[random_word] = word_dict[random_word]
    else:
        wrong_sound.play()
        unknown_words[random_word] = word_dict[random_word]
    pick_random_word()


def flip_card(event):
    global showing_front
    showing_front = not showing_front
    flip_sound.play()

    if showing_front:
        canvas.itemconfig(word_text, text=random_word, fill="black")
    else:
        canvas.itemconfig(word_text, text=word_dict[random_word], fill="white")

    if showing_front:
        canvas.itemconfig(canvas_image, image=card_front_img)
        canvas.itemconfig(title_text, text=selected_language, fill="black")
        canvas.itemconfig(word_text, text=random_word, fill="black")
    else:
        canvas.itemconfig(canvas_image, image=card_back_img)
        canvas.itemconfig(title_text, text="Translation", fill="white")
        canvas.itemconfig(word_text, text=word_dict[random_word], fill="white")


def display_session_review():
    review_sound.play()
    review_window = Toplevel(window)
    review_window.title("Session Review")
    review_window.config(bg=BACKGROUND_COLOR)

    Label(review_window, text="Session Complete!", font=("Arial", 25, "bold"), bg=BACKGROUND_COLOR).pack(pady=10)

    Label(review_window, text="Words You Knew (✓):", font=("Arial", 18), bg=BACKGROUND_COLOR).pack(pady=5)
    for front, back in known_words.items():
        Label(review_window, text=f"✔ {front} → {back}", font=FONT_END_SCREEN, bg=BACKGROUND_COLOR).pack()

    Label(review_window, text="Words You Missed (✗):", font=("Arial", 18), bg=BACKGROUND_COLOR).pack(pady=5)
    for front, back in unknown_words.items():
        Label(review_window, text=f"✖ {front} → {back}", font=FONT_END_SCREEN, bg=BACKGROUND_COLOR).pack()

    Button(review_window, text="Next Session", font=("Arial", 18),
           command=lambda: [review_window.destroy(), start_new_session()]).pack(pady=20)


completion_sound = pygame.mixer.Sound("sounds/completion.mp3")

def display_end_screen():
    completion_sound.play()
    for widget in window.winfo_children():
        widget.destroy()

    Label(window, text="🎉 Congratulations! 🎉", font=("Arial", 40, "bold"), bg=BACKGROUND_COLOR).pack(pady=20)
    Label(window, text="You've completed all words!", font=("Arial", 25), bg=BACKGROUND_COLOR).pack(pady=10)
    Button(window, text="Back to Start", font=("Arial", 18), command=reset_game).pack(pady=20)


# Start the program
start_page()
window.mainloop()

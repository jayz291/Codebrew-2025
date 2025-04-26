from tkinter import Tk, Label, Button, PhotoImage, Toplevel, Canvas
import pandas as pd
import random
import pygame

pygame.mixer.init()
window = Tk()
window.title("Flashy")
# default view is fullscreen, press 'ESC' to escape
window.attributes("-fullscreen", True)
window.bind("<Escape>", lambda e: window.attributes("-fullscreen", False))
LIGHT_GREEN_BACKGROUND_COLOUR = "#B1DDC6"
GREEN_COLOUR = "#88B04B"
DARK_GREEN_COLOUR = "#005a00"
YELLOW_COLOUR = "#FFFF00"
window.config(padx=75, pady=75, bg=LIGHT_GREEN_BACKGROUND_COLOUR)
SCREEN_WIDTH = window.winfo_screenwidth()
SCREEN_HEIGHT = window.winfo_screenheight()


def start_menu():
    # Clear any existing widgets and create a fresh menu
    for widget in window.winfo_children():
        widget.destroy()

    Label(
        window, text="Choose a Language!", font=("Arial", 50, "bold"), fg=DARK_GREEN_COLOUR, bg=LIGHT_GREEN_BACKGROUND_COLOUR
    ).pack(pady=20)

    for language in ["French", "Latin", "Chinese"]:
        Button(
            window,
            text=language,
            font=("Arial", 18),
            command=lambda lang=language: load_vocabulary(lang),
            fg=YELLOW_COLOUR,
            bg=DARK_GREEN_COLOUR,
        ).pack(pady=10)


def load_vocabulary(language):
    language_files = {
        "French": "French_words_to_learn.csv",
        "Latin": "Latin_words_to_learn.csv",
        "Chinese": "Chinese_words_to_learn.csv",
    }

    file_path = language_files.get(language)
    words = pd.read_csv(file_path, encoding="utf-8")

    word_dict = {row.iloc[0]: row.iloc[1] for _, row in words.iterrows()}
    remaining_words = list(word_dict.keys())

    # Move to main flashcard screen
    setup_flashcard_ui(language, word_dict, remaining_words)


def setup_flashcard_ui(language, word_dict, remaining_words):
    for widget in window.winfo_children():
        widget.destroy()

    # Create a state dictionary to track the app state
    state = {
        "showing_front": True,
        "random_word": None,
        "session_counter": 0,
        "answering": False,
    }

    card_front_img = PhotoImage(file="images/card_front.png")
    card_back_img = PhotoImage(file="images/card_back.png")
    wrong_img = PhotoImage(file="images/wrong.png")
    right_img = PhotoImage(file="images/right.png")


    canvas_height = SCREEN_HEIGHT - 500
    canvas_width = SCREEN_WIDTH - 400
    optimal_centering_width = canvas_width / 2

    canvas = Canvas(window, width=canvas_width, height=canvas_height, highlightthickness=0, bg=LIGHT_GREEN_BACKGROUND_COLOUR)
    canvas_image = canvas.create_image(optimal_centering_width, canvas_height / 2, image=card_front_img)
    title_text = canvas.create_text(
        optimal_centering_width, 150, text=language, font=("Arial", 30, "italic"), fill=DARK_GREEN_COLOUR,
    )
    reminder_text_label = Label(
        window, text="Left-click on the flashcard to show translation!", font=("Arial", 50, "bold"), fg=DARK_GREEN_COLOUR, bg=LIGHT_GREEN_BACKGROUND_COLOUR
    )
    reminder_text_label.grid(row=0, column=1)

    word_text = canvas.create_text(optimal_centering_width, 275, text="", font=("Arial", 50, "bold"), fill=DARK_GREEN_COLOUR)
    counter_text = canvas.create_text(
        optimal_centering_width, 450, text="Words reviewed: 0/20", font=("Arial", 20, "bold"), fill=DARK_GREEN_COLOUR,
    )
    canvas.grid(column=1, row=1, columnspan=1, pady=20)

    wrong_button = Button(window, image=wrong_img, highlightthickness=0)
    wrong_button.grid(column=0, row=2)
    right_button = Button(window, image=right_img, highlightthickness=0)
    right_button.grid(column=2, row=2)
    restart_button = Button(
        window, text="Back to Start", font=("Arial", 18), fg=YELLOW_COLOUR, bg=DARK_GREEN_COLOUR, command=start_menu
    )
    restart_button.grid(column=1, row=2, pady=30)
    escape_label = Label(window, text="Press 'ESC' on keyboard to toggle out of full-screen mode", font=("Arial", 30), fg=GREEN_COLOUR, bg=LIGHT_GREEN_BACKGROUND_COLOUR)
    escape_label.grid(column=1, row=3, pady=70)

    canvas.card_front_img = card_front_img
    canvas.card_back_img = card_back_img
    wrong_button.image = wrong_img
    right_button.image = right_img

    new_session(
        language,
        word_dict,
        remaining_words,
        canvas,
        canvas_image,
        title_text,
        word_text,
        counter_text,
        wrong_button,
        right_button,
        state,
    )


def new_session(
    language,
    word_dict,
    remaining_words,
    canvas,
    canvas_image,
    title_text,
    word_text,
    counter_text,
    wrong_button,
    right_button,
    state,
):
    session_size = 20
    known_words = {}
    unknown_words = {}
    session_words = []

    state["session_counter"] = 0

    # Get batch of words for this session
    if remaining_words:
        session_words = random.sample(
            remaining_words, min(session_size, len(remaining_words))
        )
        for word in session_words:
            remaining_words.remove(word)

        def update_counter():
            canvas.itemconfig(
                counter_text,
                text=f"Words reviewed: {state['session_counter']}/{session_size}",
            )

        def pick_random_word():
            if session_words:
                state["random_word"] = session_words.pop(0)
                state["session_counter"] += 1
                state["showing_front"] = True
                update_counter()

                canvas.itemconfig(canvas_image, image=canvas.card_front_img)
                canvas.itemconfig(title_text, text=language, fill=GREEN_COLOUR)
                canvas.itemconfig(word_text, text=state["random_word"], fill=GREEN_COLOUR)

                return True
            else:
                display_session_review(
                    known_words,
                    unknown_words,
                    language,
                    word_dict,
                    remaining_words,
                    canvas,
                    canvas_image,
                    title_text,
                    word_text,
                    counter_text,
                    wrong_button,
                    right_button,
                    state,
                )
                return False

        def mark_word(correct):
            if correct:
                pygame.mixer.Sound("sounds/correct.mp3").play()
                known_words[state["random_word"]] = word_dict[state["random_word"]]
            else:
                pygame.mixer.Sound("sounds/wrong.mp3").play()
                unknown_words[state["random_word"]] = word_dict[state["random_word"]]

            pick_random_word()

        def flip_card(event):
            state["showing_front"] = not state["showing_front"]
            pygame.mixer.Sound("sounds/flip.mp3").play()

            if state["showing_front"]:
                canvas.itemconfig(canvas_image, image=canvas.card_front_img)
                canvas.itemconfig(title_text, text=language, fill=GREEN_COLOUR)
                canvas.itemconfig(word_text, text=state["random_word"], fill=GREEN_COLOUR)
            else:
                canvas.itemconfig(canvas_image, image=canvas.card_back_img)
                canvas.itemconfig(title_text, text="Translation:", fill=YELLOW_COLOUR)
                canvas.itemconfig(
                    word_text, text=word_dict[state["random_word"]], fill=YELLOW_COLOUR
                )

        canvas.bind("<Button-1>", flip_card)
        wrong_button.config(command=lambda: mark_word(False))
        right_button.config(command=lambda: mark_word(True))

        pick_random_word()
    else:
        ending_screen()


def display_session_review(
    known_words,
    unknown_words,
    language,
    word_dict,
    remaining_words,
    canvas,
    canvas_image,
    title_text,
    word_text,
    counter_text,
    wrong_button,
    right_button,
    state,
):
    pygame.mixer.Sound("sounds/review.mp3").play()

    # Create review window
    review_window = Toplevel(window)
    review_window.title("Session Review")
    review_window.config(bg=GREEN_COLOUR)

    Label(
        review_window,
        text="Session Complete!",
        font=("Arial", 25, "bold"),
        bg=GREEN_COLOUR,
    ).pack(pady=10)

    Label(
        review_window, text="Words You Knew (✓):", font=("Arial", 18), bg=GREEN_COLOUR
    ).pack(pady=5)
    for front, back in known_words.items():
        Label(
            review_window,
            text=f"✔ {front} → {back}",
            font=("Arial", 14, "bold"),
            bg=GREEN_COLOUR,
        ).pack()

    Label(
        review_window, text="Words You Missed (✗):", font=("Arial", 18), bg=GREEN_COLOUR
    ).pack(pady=5)
    for front, back in unknown_words.items():
        Label(
            review_window,
            text=f"✖ {front} → {back}",
            font=("Arial", 14, "bold"),
            bg=GREEN_COLOUR,
        ).pack()

    Button(
        review_window,
        text="Next Session",
        font=("Arial", 18),
        command=lambda: [
            review_window.destroy(),
            new_session(
                language,
                word_dict,
                remaining_words,
                canvas,
                canvas_image,
                title_text,
                word_text,
                counter_text,
                wrong_button,
                right_button,
                state,
            ),
        ],
    ).pack(pady=20)


def ending_screen():
    pygame.mixer.Sound("sounds/completion.mp3").play()

    for widget in window.winfo_children():
        widget.destroy()

    Label(
        window, text="🎉 Congratulations! 🎉", font=("Arial", 40, "bold"), bg=GREEN_COLOUR
    ).pack(pady=20)
    Label(
        window, text="You've completed all words!", font=("Arial", 25), bg=GREEN_COLOUR
    ).pack(pady=10)
    Button(window, text="Back to Start", font=("Arial", 18), command=start_menu).pack(
        pady=20
    )


start_menu()
window.mainloop()

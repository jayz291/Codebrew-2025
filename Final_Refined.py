from tkinter import Tk, Label, Button, PhotoImage, Toplevel, Canvas
import pandas as pd
import random
import pygame

pygame.mixer.init()
window = Tk()
window.title("Flashy")
window.config(padx=75, pady=75, bg="#B1DDC6")


def start_menu():
    # Clear any existing widgets and create a fresh menu
    for widget in window.winfo_children():
        widget.destroy()

    Label(
        window, text="Choose a Language", font=("Arial", 25, "bold"), bg="#B1DDC6"
    ).pack(pady=20)

    for language in ["French", "Latin", "Chinese"]:
        Button(
            window,
            text=language,
            font=("Arial", 18),
            command=lambda lang=language: load_vocabulary(lang),
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

    canvas = Canvas(window, width=820, height=550, highlightthickness=0, bg="#B1DDC6")
    canvas_image = canvas.create_image(410, 275, image=card_front_img)
    title_text = canvas.create_text(
        410, 150, text=language, font=("Arial", 30, "italic")
    )
    word_text = canvas.create_text(410, 275, text="", font=("Arial", 50, "bold"))
    counter_text = canvas.create_text(
        410, 450, text="Words reviewed: 0/20", font=("Arial", 20, "bold")
    )
    canvas.grid(column=0, row=0, columnspan=2)

    wrong_button = Button(window, image=wrong_img, highlightthickness=0)
    wrong_button.grid(column=0, row=1)
    right_button = Button(window, image=right_img, highlightthickness=0)
    right_button.grid(column=1, row=1)
    restart_button = Button(
        window, text="Back to Start", font=("Arial", 18), command=start_menu
    )
    restart_button.grid(column=0, row=2, columnspan=2, pady=20)

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
                canvas.itemconfig(title_text, text=language, fill="black")
                canvas.itemconfig(word_text, text=state["random_word"], fill="black")

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
                canvas.itemconfig(title_text, text=language, fill="black")
                canvas.itemconfig(word_text, text=state["random_word"], fill="black")
            else:
                canvas.itemconfig(canvas_image, image=canvas.card_back_img)
                canvas.itemconfig(title_text, text="Translation", fill="white")
                canvas.itemconfig(
                    word_text, text=word_dict[state["random_word"]], fill="white"
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
    review_window.config(bg="#B1DDC6")

    Label(
        review_window,
        text="Session Complete!",
        font=("Arial", 25, "bold"),
        bg="#B1DDC6",
    ).pack(pady=10)

    Label(
        review_window, text="Words You Knew (✓):", font=("Arial", 18), bg="#B1DDC6"
    ).pack(pady=5)
    for front, back in known_words.items():
        Label(
            review_window,
            text=f"✔ {front} → {back}",
            font=("Arial", 14, "bold"),
            bg="#B1DDC6",
        ).pack()

    Label(
        review_window, text="Words You Missed (✗):", font=("Arial", 18), bg="#B1DDC6"
    ).pack(pady=5)
    for front, back in unknown_words.items():
        Label(
            review_window,
            text=f"✖ {front} → {back}",
            font=("Arial", 14, "bold"),
            bg="#B1DDC6",
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
        window, text="🎉 Congratulations! 🎉", font=("Arial", 40, "bold"), bg="#B1DDC6"
    ).pack(pady=20)
    Label(
        window, text="You've completed all words!", font=("Arial", 25), bg="#B1DDC6"
    ).pack(pady=10)
    Button(window, text="Back to Start", font=("Arial", 18), command=start_menu).pack(
        pady=20
    )


start_menu()
window.mainloop()

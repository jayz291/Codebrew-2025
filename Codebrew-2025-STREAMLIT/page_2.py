import streamlit as st
import pandas as pd
import time
from random import randint
from PIL import Image

main = st.Page("main.py", title="French", icon="🇫🇷")
page_2 = st.Page("page_2.py", title="Latin", icon="🇻🇦")
page_3 = st.Page("page_3.py", title="Chinese", icon="🇨🇳")

pg = st.navigation([main, page_2, page_3])
if pg == page_2:
    page_2.run()
    # Load data
    latin_words = pd.read_csv("Latin_words_to_learn.csv")
    latin_to_english_dict = {row.Latin: row.English for (index,row) in latin_words.iterrows()}
    image = Image.open("images/card_front.png")

    # Header
    st.markdown("""
        <div style='background-color: DodgerBlue; text-align: center; padding: 10px;'>
            <h1 style='color: Tomato; margin: 0;'>Test your Latin!</h1>
        </div>""", unsafe_allow_html=True)

    # Create layout with columns
    left, middle, right = st.columns(3)

    # Add buttons for user interaction
    left_button = left.button("I don't know this word... :sunglasses:", type="primary")
    right_button = right.button('I know this word!', type="primary")

    # Add image
    middle.image(image, caption="Latin Flashcards", use_container_width=True)

    for i in range(len(latin_to_english_dict)):
        random_latin_word = list(latin_to_english_dict.keys())[randint(0, len(latin_to_english_dict))]
        middle.write(random_latin_word)
        time.sleep(1)
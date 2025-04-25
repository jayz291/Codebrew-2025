import streamlit as st
import pandas as pd
import time
from random import randint
from PIL import Image

# Load data
french_words = pd.read_csv("french_words.csv")
french_to_english_dict = {row.French: row.English for (index,row) in french_words.iterrows()}
image = Image.open("images/card_front.png")

# Header
st.markdown("""
    <div style='background-color: DodgerBlue; text-align: center; padding: 10px;'>
        <h1 style='color: Tomato; margin: 0;'>Test your French!</h1>
    </div>""", unsafe_allow_html=True)

# Create layout with columns
left, middle, right = st.columns(3)

# Add buttons for user interaction
left_button = left.button("I don't know this word... :sunglasses:", type="primary")
right_button = right.button('I know this word!', type="primary")

# Add image
middle.image(image, caption="French Flashcards", use_container_width=True)

for i in range(len(french_to_english_dict)):
    random_french_word = list(french_to_english_dict.keys())[randint(0, len(french_to_english_dict))]
    middle.write(random_french_word)
    time.sleep(1)





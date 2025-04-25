import streamlit as st
import pandas as pd
from PIL import Image

french_words = pd.read_csv("french_words.csv")
french_to_english_dict = {row.French: row.English for (index,row) in french_words.iterrows()}
print(french_to_english_dict)
image = Image.open("/images/card_front.png")

#st.write("Hello World!")
st.image(image, caption="Starting")
import streamlit as st
import pandas as pd

french_words = pd.read_csv("french_words.csv")
french_to_english_dict = {row.French: row.English for (index,row) in french_words.iterrows()}
print(french_to_english_dict)

#st.write("Hello World!")
st.file_uploader()
import streamlit as st
import pandas as pd
import time
import os
from random import randint
from PIL import Image


main = st.Page("main.py", title="French", icon="🇫🇷")
page_2 = st.Page("page_2.py", title="Latin", icon="🇻🇦")
page_3 = st.Page("page_3.py", title="Chinese", icon="🇨🇳")

pg = st.navigation([main, page_2, page_3])

if pg == main:
    import streamlit as st
    import pandas as pd
    from random import randint
    from PIL import Image, ImageDraw, ImageFont

    # Load data
    french_words = pd.read_csv("french_words.csv")
    french_to_english_dict = {row.French: row.English for (index,row) in french_words.iterrows()}

    # Select a random French word
    random_french_word = list(french_to_english_dict.keys())[randint(0, len(french_to_english_dict))]
    english_translation = french_to_english_dict[random_french_word]

    # Using PILLOW to inscribe text onto the image
    image = Image.open("images/card_front.png")
    draw = ImageDraw.Draw(image)
    arial_font = ImageFont.truetype("Arial.ttf", size=100)

    # Get the size of the image and the text
    (image_width, image_height) = image.size
    box_of_text_in_pixels = draw.textbbox(xy=(0, 0), text=random_french_word, font=arial_font)
    text_width = box_of_text_in_pixels[2] - box_of_text_in_pixels[0]
    text_height = box_of_text_in_pixels[3] - box_of_text_in_pixels[1]

    # darwing text
    draw.text(xy=((image_width - text_width)/2,(image_height - text_height)/2), text=random_french_word, align="left", fill="black", font=arial_font)

    st.markdown("""
        <div style='background-color: DodgerBlue; text-align: center; padding: 10px;'>
            <h1 style='color: Tomato; margin: 0;'>Test your French!</h1>
        </div>""", unsafe_allow_html=True)

    image_displayed = st.image(image, caption="French Flashcards", use_container_width=True)

    # Create layout with columns
    left, middle, right = st.columns(3)

    left_button = left.button("I don't know this word... :sunglasses:", type="primary")
    right_button = right.button('I know this word!', type="primary")

    if left_button:
        # Draw English translation
        draw.text(
            xy=((image_width - text_width) / 2, (image_height - text_height) / 2 + 120),
            text=french_to_english_dict[random_french_word],
            fill="blue",
            font=arial_font
        )
        image_displayed = st.image(image, caption="Translation shown!", use_column_width=True)

    elif right_button:
        st.success("Nice job!")
    
    


elif pg == page_2:
    import streamlit as st
    import pandas as pd
    from random import randint
    from PIL import Image, ImageDraw, ImageFont

    # Load data
    latin_words = pd.read_csv("Latin_words_to_learn.csv")
    latin_to_english_dict = {row.Latin: row.English for (index,row) in latin_words.iterrows()}

    # Select a random Latin word
    random_latin_word = list(latin_to_english_dict.keys())[randint(0, len(latin_to_english_dict))]
    english_translation = latin_to_english_dict[random_latin_word]

    # Using PILLOW to inscribe text onto the image
    image = Image.open("images/card_front.png")
    draw = ImageDraw.Draw(image)
    arial_font = ImageFont.truetype("Arial.ttf", size=100)

    # Get the size of the image and the text
    (image_width, image_height) = image.size
    box_of_text_in_pixels = draw.textbbox(xy=(0, 0), text=random_latin_word, font=arial_font)
    text_width = box_of_text_in_pixels[2] - box_of_text_in_pixels[0]
    text_height = box_of_text_in_pixels[3] - box_of_text_in_pixels[1]

    # darwing text
    draw.text(xy=((image_width - text_width)/2,(image_height - text_height)/2), text=random_latin_word, align="left", fill="black", font=arial_font)

    st.markdown("""
        <div style='background-color: DodgerBlue; text-align: center; padding: 10px;'>
            <h1 style='color: Tomato; margin: 0;'>Test your Latin!</h1>
        </div>""", unsafe_allow_html=True)

    image_displayed = st.image(image, caption="Latin Flashcards", use_container_width=True)

    # Create layout with columns
    left, middle, right = st.columns(3)

    left_button = left.button("I don't know this word... :sunglasses:", type="primary")
    right_button = right.button('I know this word!', type="primary")

    if left_button:
        # Draw English translation
        draw.text(
            xy=((image_width - text_width) / 2, (image_height - text_height) / 2 + 120),
            text=latin_to_english_dict[random_latin_word],
            fill="blue",
            font=arial_font
        )
        image_displayed = st.image(image, caption="Translation shown!", use_column_width=True)

    elif right_button:
        st.success("Nice job!")

elif pg == page_3:
    import streamlit as st
    import pandas as pd
    from random import randint
    from PIL import Image, ImageDraw, ImageFont

    # Load data
    chinese_words = pd.read_csv("Chinese_words_to_learn.csv")
    chinese_to_english_dict = {row.Chinese: row.English for (index,row) in chinese_words.iterrows()}

    # Select a random Chinese word
    random_chinese_word = list(chinese_to_english_dict.keys())[randint(0, len(chinese_to_english_dict))]
    english_translation = chinese_to_english_dict[random_chinese_word]

    # Using PILLOW to inscribe text onto the image
    image = Image.open("images/card_front.png")
    draw = ImageDraw.Draw(image)
    arial_font = ImageFont.truetype("Arial.ttf", size=100)

    # Get the size of the image and the text
    (image_width, image_height) = image.size
    box_of_text_in_pixels = draw.textbbox(xy=(0, 0), text=random_chinese_word, font=arial_font)
    text_width = box_of_text_in_pixels[2] - box_of_text_in_pixels[0]
    text_height = box_of_text_in_pixels[3] - box_of_text_in_pixels[1]

    # darwing text
    draw.text(xy=((image_width - text_width)/2,(image_height - text_height)/2), text=random_chinese_word, align="left", fill="black", font=arial_font)

    st.markdown("""
        <div style='background-color: DodgerBlue; text-align: center; padding: 10px;'>
            <h1 style='color: Tomato; margin: 0;'>Test your Chinese!</h1>
        </div>""", unsafe_allow_html=True)

    image_displayed = st.image(image, caption="Chinese Flashcards", use_container_width=True)

    # Create layout with columns
    left, middle, right = st.columns(3)

    left_button = left.button("I don't know this word... :sunglasses:", type="primary")
    right_button = right.button('I know this word!', type="primary")

    if left_button:
        # Draw English translation
        draw.text(
            xy=((image_width - text_width) / 2, (image_height - text_height) / 2 + 120),
            text=chinese_to_english_dict[random_chinese_word],
            fill="blue",
            font=arial_font
        )
        image_displayed = st.image(image, caption="Translation shown!", use_column_width=True)

    elif right_button:
        st.success("Nice job!")





import streamlit as st
from numpy import load
from numpy import expand_dims
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
import requests
import io

#st.header("Generate facades images using cGAN")
st.markdown(
    "<h1 style='text-align: center; color: blue;'>Generate facades images using cGAN</h1>",
    unsafe_allow_html=True)
#st.write("Choose any paint image and get the corresponding facade :")
st.markdown(
    "<h3 style='text-align: center; color: ivory;'>Choose any paint image and get the corresponding facade :</h3>",
    unsafe_allow_html=True)
st.balloons()

st.set_option("deprecation.showfileUploaderEncoding", False)
uploaded_file = st.file_uploader("Choose an image", type="png")

if uploaded_file is not None:

    # uploaded_file.__dict__
    # uploaded_file

    image = Image.open(uploaded_file)
    #st.image(image, caption="Uploaded image", use_column_width=True)
    col1, col2 = st.columns(2)
    col1.header("Input Image")
    col1.image(image, use_column_width=True)
    col2.header("Output Image")
    col2.image(image, use_column_width=True)



    # convert image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    # with open("image.jpg", "wb") as f:
    #     f.write(img_byte_arr)

    # api call
    url = "https://pix2pix-dttdfzxwga-ew.a.run.app/predict"
    files = {"file": img_byte_arr}

    response = requests.post(url, files=files)

    print(response)

    response

    if response.status_code == 200:
        resp = response.content

        with open("sample_image.png", "wb") as file:
            file.write(response.content)

        image = Image.open(io.BytesIO(response.content))
        st.image(image, caption='prediction', use_column_width=False)

    else:
        "😬 api error 🤖"
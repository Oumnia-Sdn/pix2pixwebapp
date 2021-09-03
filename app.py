import streamlit as st
from numpy import load
from numpy import expand_dims
from PIL import Image, ImageDraw, ImageFont
from streamlit_drawable_canvas import st_canvas
import numpy as np
import os
import requests
import io

# first option: upload a paint file:
st.markdown("<h1 style='text-align: center; color: black;'>🏠 🏠 🏠</h1>",
            unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: black;'>Generate facades images using cGAN</h1>",
            unsafe_allow_html=True)

# navigation
st.sidebar.write("# Navigation")
nav = st.sidebar.radio("Go to:", ["file", "drawing"])

if nav == "file":

    st.markdown(
        "<h3 style='text-align: center; color:black;'>Choose any paint image and get the corresponding facade :</h3>",
        unsafe_allow_html=True)

    st.set_option("deprecation.showfileUploaderEncoding", False)
    uploaded_file = st.file_uploader("Choose an image", type=["png","jpeg", "jpg"])

    col1, col2 = st.columns(2)

    if uploaded_file is not None:

        # uploaded_file.__dict__
        # uploaded_file

        in_image = Image.open(uploaded_file)
        #st.image(image, caption="Uploaded image", use_column_width=True)

        col1.header("Input Image")
        col1.image(in_image, use_column_width=True)

        # convert image to bytes
        img_byte_arr = io.BytesIO()
        in_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # with open("image.jpg", "wb") as f:
        #     f.write(img_byte_arr)

        # api call
        if st.button('generate'):
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
                col2.header("Generated Image")
                #st.image(image, caption='prediction', use_column_width=False)
                col2.image(image,use_column_width=True)

            else:
                "😬 api error 🤖"

elif nav == "drawing":

    #second option: draw a paint
    st.markdown(
        "<h3 style='text-align: center; color:black;'>Draw an awesome one yourself and generate its facade :</h3>",
        unsafe_allow_html=True)

    element = st.sidebar.radio("Select facade element :", [
    "Background",
    "Wall",
    "Door",
    "Window",
    "Window still",
    "Window head",
    "Shutter",
    "Balcony",
    "Trim",
    "Cornice",
    "Column",
    "Entrance"])

    element_color = {
        "Background": "rgba(1, 6, 216, 1)",
        "Wall": "rgba(13, 61, 250, 1)",
        "Door": "rgba(165, 4, 3, 1)",
        "Window": "rgba(4, 117, 254, 1)",
        "Window still": "rgba(104, 248, 152, 1)",
        "Window head": "rgba(26, 253, 221, 1)",
        "Shutter": "rgba(238, 237, 40, 1)",
        "Balcony": "rgba(184, 253, 56, 1)",
        "Trim": "rgba(254, 146, 5, 1)",
        "Cornice": "rgba(253, 68, 3, 1)",
        "Column": "rgba(246, 2, 4, 1)",
        "Entrance": "rgba(11, 201, 253, 1)"
    }

    color = element_color.get(element)


    tool = st.sidebar.selectbox("Drawing tool:",
                                ("rect", "line", "circle", "freedraw",
                                 "transform"))


    # realtime_update = st.sidebar.checkbox("Update in realtime", True)
    canvas_result = st_canvas(
        fill_color=color,
        stroke_width=1,
        stroke_color=color,
        background_color="rgba(0, 0, 0, 0)",
        background_image=None,
        update_streamlit=True,  # realtime_update
        width=512,
        height=512,
        drawing_mode=tool,
        key="canvas")

    col1, col2 = st.columns(2)

    def save_image():

        dr_img = Image.fromarray(canvas_result.image_data.astype("uint8"), 'RGBA')
        # dr_img.save("drawing.png")
        st.session_state.dr_image = dr_img

        col1.header("Input Image")
        col1.image(dr_img, use_column_width=True)

    if st.button("save"):

        save_image()

    # api call
    def call_api():

        url = "https://pix2pix-dttdfzxwga-ew.a.run.app/predict"

        dr_img = st.session_state.dr_image
        img_byte_arr = io.BytesIO()
        dr_img.save(img_byte_arr, format='PNG')
        the_bytes = img_byte_arr.getvalue()

        response = requests.post(url, files= {"file": the_bytes})

        print(response)

        response

        if response.status_code == 200:
            resp = response.content

            #with open("sample_image.png", "wb") as file:
            #file.write(response.content)

            gen_img = Image.open(io.BytesIO(response.content))
            col2.header("Generated Image")
            #st.image(image, caption='prediction', use_column_width=False)
            col2.image(gen_img, use_column_width=True)

        else:
            "😬 api error 🤖"

    if st.button('generate'):
        save_image()
        call_api()

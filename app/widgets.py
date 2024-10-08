from PIL import Image
import pandas as pd
import streamlit as st
import time
import os

# local imports
from callbacks import next_img, prev_img
from file_io import inspect_results
from globals import update_globals


def show_download(name_zip="ant-detective.zip"):
    if st.session_state['loaded'] and os.path.exists(name_zip):
        with open(name_zip, 'rb') as f:
            bytes = f.read()
        st.download_button("Download the Detection Results", 
                            data=bytes, 
                            type="primary",
                            file_name=name_zip, )    

    

def show_navigator():
    cur_i = st.session_state.cur_i
    n_imgs = st.session_state.n_imgs

    if n_imgs == 0 or n_imgs == 1:
        st.empty()
    else:
        col_b1, col_b2 = st.columns([3, 1])
        col_b1.button(
            "⬅︎ Previous Image",
            on_click=prev_img,
        )
        col_b2.button(
            "Next Image ➡︎",
            on_click=next_img,
        )
        # st.success("Drag the slider to navigate between images")
        st.slider(
            "File Index",
            min_value=0,
            max_value=n_imgs - 1,
            value=cur_i,
            on_change=slide_i,
            key="slider_index",
            label_visibility="collapsed",
        )



def image_uploader():
    file_ram = st.file_uploader(
        "Upload Image",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        key="image_uploader",
        label_visibility="collapsed",
    )
    is_change = file_ram != st.session_state.file_ram
    st.session_state.file_ram = file_ram
    if st.session_state.init is not None and is_change:
        print("new update!")
        update_globals()
        st.session_state.detect_count = inspect_results()

    #to avoid file_uplaoder to trigger update_globals the first time 
    st.session_state.init = True
    

def slide_i():
    cur_i = st.session_state.cur_i
    slider_value = st.session_state.slider_index
    print("callback: slide_i (%d, %d)" % (slider_value, st.session_state.cur_i))
    if slider_value != st.session_state.cur_i:
        print("change index!")
        st.session_state.cur_i = slider_value
        print("after changed:", slider_value)



# class Timer:
#     def __init__(self, message="Page loaded"):
#         self.message = message

#     def __enter__(self):
#         self.start = time.time()
#         return self

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         end = time.time()
#         st.info(f"{self.message}: {end - self.start:.2f} seconds")



# def show_ui():
#     st.divider()
#     tg1, tg2 = st.columns(2)
#     with tg1:
#         tog_edit = st.toggle("Transform the bounding boxes", False, key="toggle_edit")
#     with tg2:
#         tog_auto = st.toggle("Render on-the-fly (slower)", True, key="toggle_auto")

#     if st.session_state.toggle_edit:
#         st.success("Drag the corners to transform the bounding boxes")
#     else:
#         st.success("Draw a rectangle on the canvas to create a new bounding box")
#     if not st.session_state.toggle_auto:
#         st.success("Right-click on the canvas to render the annotations")

#     return tog_auto, tog_edit
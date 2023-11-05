import streamlit as st
from PIL import Image
import base64
from htbuilder import HtmlElement, div, hr, p, styles
from htbuilder.units import percent, px
import os
import pathlib
from mantis_vision.statefulness import *

# from frontend.streamlit_state_handling import *


# --------------------------------------------------------------------
# Streamlit Functions Module
# --------------------------------------------------------------------


def local_css(file_name):
    with open(file_name) as f:
        st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)


def add_bg_from_local(background_image):
    with open(background_image, "rb") as background_image:
        encoded_string = base64.b64encode(background_image.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(119,119,119,.6), rgba(119,119,119,1)), url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


def add_image_and_title(logo_image):
    col1, col2, col3, col4 = st.columns([0.1, 1, 0.3, 0.1])
    image = Image.open(logo_image)
    with col1:
        st.write("")
    with col2:
        st.title("Mantis Vision")
    with col3:
        st.image(image, width=200)
    with col4:
        st.write("")
    st.markdown(
        f"A tool for rock physics analysis and forward modelling developed by ***mantis geophysics***, a University of Edinburgh spinout."
    )


def footer_layout(*args):
    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 40px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="white",
        background_color="#005E00",
        text_align="center",
        text_weight="bold",
        height="40px",
        opacity=1,
    )

    style_hr = styles(
        display="block",
        background_color="#000000",
        # margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(0.5),
    )

    body = p()
    # foot = div(style=style_div)(hr(style=style_hr), body)
    foot = div(style=style_div)(body)

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def call_footer():
    myargs = ["developed by Giorgos Papageorgiou: gpap@mantis-geophysics.com"]
    footer_layout(*myargs)


def initialize_app_states():
    """
    Initialize session states
    """

    state = st.session_state
    state = set_all_states(state)

    return state


def initializing_sidebar_for_status_info():
    """
    Initializing sidebar for streamlit app page
    """

    image_path = os.path.join(
        str(pathlib.Path(__file__).parent.resolve()),
        "../images",
        "pwi_logo_no_text.png",
    )

    image = Image.open(image_path)
    with st.sidebar:
        # col1, col2, col3 = st.columns([1, 6, 1])
        # with col1:
        #     st.title("  ")
        # with col2:
        #     st.image(image)
        # with col3:
        #     st.write("")
        # st.write("")
        status = st.empty()

    return status


def st_layout_pipeline(background_image, logo_image, style_css):
    """
    Pipeline for definition of the streamlit app layout
    """

    # st.set_page_config(layout="wide")
    local_css(style_css)
    add_bg_from_local(background_image)
    add_image_and_title(logo_image)
    state = initialize_app_states()
    status = initializing_sidebar_for_status_info()

    call_footer()

    return state, status

import subprocess
import sys
import os
import time
import streamlit as st


try:
    # replace "yourpackage" with the package you want to import
    import mantis

# This block executes only on the first run when your package isn't installed
except ModuleNotFoundError as e:
    sleep_time = 45
    dependency_warning = st.warning(
        f"Installing dependencies, this takes {sleep_time} seconds."
    )
    subprocess.Popen(
        [
            f"{sys.executable} -m pip install git+https://gpap-gpap:{st.secrets['git_token']}@github.com/gpap-gpap/anisotroPY.git@dev-fAVO"
        ],
        shell=True,
    )
    # wait for subprocess to install package before running your actual code below
    time.sleep(sleep_time)
    dependency_warning.empty()
import mantis_vision.look_and_feel as lf
import mantis.rock_physics as manRP

from mantis_vision.showcase_loading import *
from mantis_vision.send_email import *
import mantis_vision.simple_workflow as sw

# st.set_page_config(layout="wide")


def main():
    # st.write("Hello World!")
    state, status = lf.st_layout_pipeline(
        background_image="images/phasor_logo.png",
        logo_image="images/phasor_logo.png",
        style_css="style/style.css",
    )

    # image = Image.open("images/advance.png")
    # st.image(image, width=100, caption="")
    # state.process_select, status = process_type_selection(status)

    # st.write("")

    # state, status = structured_pipeline(state, status)

    # state.process_select_confirmed = st.button("Start Process")

    # if state.process_select_confirmed is True:
    #     status.info("Process selected!")
    #     state.begin_process = True

    # if state.begin_process:
    #     if state.process_select == "Structured Data (Single)":
    #         state, status = structured_pipeline(state, status)
    #     elif state.process_select == "Unstructured Data (Single)":
    #         state, status = unstructured_pipeline_single(state, status)
    #     elif state.process_select == "Unstructured Data (Bulk)":
    #         state, status = unstructured_pipeline(state, status)

    if "stage" not in st.session_state:
        st.session_state.stage = 0

    def set_state(i):
        st.session_state.stage = i

    def advance_state():
        st.session_state.stage += 1

    def reset_callback():
        st.session_state.stage = 0
        reset_state(st.session_state)

    def email_callback(email: str):
        send_email(email)
        reset_callback()

    if st.session_state.stage == 0:
        sw.load_1d_model()
        if st.session_state.input_file is not None:
            st.button("Continue", on_click=set_state, args=[1])
    if st.session_state.input_file is not None:
        sw.plot_1d_model_to_sidebar(st.session_state.input_file)
    if st.session_state.stage >= 1:
        sw.select_earth_layer()
    if st.session_state.stage == 1:
        st.button("Chose model", on_click=set_state, args=[2])
        # name = st.text_input("Name", on_change=set_state, args=[2])

    if st.session_state.stage >= 2:
        sw.choose_rock_physics_models()
    if st.session_state.stage == 2:
        st.button("Plot model", on_click=set_state, args=[3])
    if st.session_state.stage >= 3:
        sw.plot_rock_physics_models()
    if st.session_state.stage == 3:
        st.button("Do some AVO", on_click=set_state, args=[4])
    if st.session_state.stage >= 4 and st.session_state.stage < 5:
        email_sender = st.text_input(
            "Enter your email address to receive a small report"
        )
        feedback = st.text_input("Please leave some feedback:")
        # email_receiver = st.text_input("To")
        if st.button("Send Email"):
            send_email(email_sender)
            st.write("Email sent")
            reset_callback()
        # form = st.form(key="email-test")
        # email = form.text_input("Enter your email")
        # name = form.text_input("Enter your name")
        # submit = form.form_submit_button("Submit", on_click=set_state, args=[5])
        # if submit:
        #     # st.write(f"hello {name}")
        #     send_email(email)
    if st.session_state.stage == 5:
        st.button("Reset", on_click=reset_callback)


if __name__ == "__main__":
    main()
    # st.write("wee baws")

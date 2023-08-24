import subprocess
import sys
import os
import time

try:
    # replace "yourpackage" with the package you want to import
    import mantis

# This block executes only on the first run when your package isn't installed
except ModuleNotFoundError as e:
    st.write(f"worked to module not found {os.environ['git_token']}")
    subprocess.Popen(
        [
            f"{sys.executable} -m pip install git+https://${os.environ['git_token']}@github.com/gpap-gpap/anisotroPY.git@dev-fAVO"
        ],
        shell=True,
    )
    # wait for subprocess to install package before running your actual code below
    time.sleep(90)
from mantis_vision.look_and_feel import *
from mantis_vision.showcase_loading import *


def main():
    state, status = st_layout_pipeline(
        background_image="images/phasor_logo.png",
        logo_image="images/phasor_logo.png",
        style_css=".streamlit/style.css",
    )
    # image = Image.open("images/advance.png")
    # st.image(image, width=100, caption="")
    # state.process_select, status = process_type_selection(status)

    # st.write("")

    state, status = structured_pipeline(state, status)

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


if __name__ == "__main__":
    main()

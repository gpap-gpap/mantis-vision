import streamlit as st
import pandas as pd
import requests
import mantis.rock_physics as manRP
import mantis.rock_physics.fluid as manFL
from mantis_vision.statefulness import *
import mantis_vision.base_functions as bf
from PIL import Image


def hline():
    col1, col2, col3 = st.columns([0.4, 1, 0.4])
    with col1:
        st.write(" ")
    with col2:
        st.markdown(
            """<hr style="height:9px;border:4px solid black;
  border-radius: 5px;color:#FF8000;background-color:#FF8000;" /> """,
            unsafe_allow_html=True,
        )
    with col3:
        st.write(" ")


def v_spacer(height, sb=False) -> None:
    for _ in range(height):
        st.write("\n")


def advance():
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(" ")

    with col2:
        try:
            image = Image.open("images/down_arrow.png")

            st.image(image, width=150, caption="")
            v_spacer(height=15)
        except FileNotFoundError:
            st.write("File not found")
    with col3:
        st.write(" ")


def add_title_step_1():
    """
    Adding title for step 1 - specifying file type
    """
    # st.write(
    #     "------------------------------------\n------------------------------------"
    # )
    hline()
    st.markdown(
        f"### Start here. Upload a CSV or XLS file with four columns: Depth, Vp, Vs, Rho"
    )
    # st.markdown("##### Please upload file to be processed.")


def excel_csv_loading(state):
    """
    Uploading and processing jpg/png/tif file
    """

    # file is uploaded
    uploaded_file = st.file_uploader(label="", type=["xlsx", "csv"])

    if uploaded_file is None:
        state.input_file = None
        # state = state_upload_file_none(state)

    else:
        # file converted to numpy array for later processing

        state.input_file = uploaded_file
        state.file_path = state.input_file.name
        # state.current_earth_model = state.file_path
    return state


def convert_file_to_df(state, status):
    status.info("First load an earth model")

    if state.input_file is not None:
        if state.input_file.name.endswith(".csv"):
            state.current_earth_model = pd.read_csv(state.input_file)

        elif state.file.name.endswith(".xlsx"):
            state.current_earth_model = pd.read_excel(state.input_file)
        state.file_uploaded = True
    return state, status


def plot_earth_model(state, status):
    if state.file_uploaded:
        status.info("plotting earth model...")
        with st.sidebar:
            fig = bf.plot_1d_model(state.current_earth_model)
            st.write("")
            # st.write(state.current_earth_model)
            st.write(fig)

    return status


def add_title_step_2(state):
    """
    Adding title for step 2 - begin chatting
    """

    if state.file_uploaded:
        advance()
        st.info(
            "You have succesfully uploaded a 1D Earth model, great stuff! Now, let's move on and do some rock physics",
            icon="ℹ️",
        )
        advance()
        hline()
        st.markdown(
            f"### Choose a layer that you want to change rock physics properties for"
        )
        state.current_layer = st.slider(
            label="layer number",
            min_value=0,
            max_value=len(state.current_earth_model) - 2,
            step=1,
        )
        display = state.current_earth_model.iloc[state.current_layer]
        display["thickness"] = round(
            -display["Depth(m)"]
            + state.current_earth_model.iloc[state.current_layer + 1]["Depth(m)"],
            1,
        )
        st.write(display)


def add_title_step_3(state):
    if state.file_uploaded:
        # advance()
        # hline()
        st.markdown(
            f"### Now choose the fluid that will displace water and a rock physics model"
        )
        col1, col2, col3 = st.columns([0.3, 0.3, 1])
        with col1:
            fluid = st.radio(
                label="Fluid",
                options=["CarbonDioxide", "Hydrogen", "Methane"],
            )
            with st.expander("Advanced"):
                st.write(bf.fluid_data[fluid])
            # pres_range = fluid_data["Pres-MPa"].unique())
            # st.slider(
            #     "Pressure (MPa)",
            #     min_value=int(pres_range.min()),
            #     max_value=int(pres_range.max()),
            #     step=5,
            #     key="pres",
            # )
            # temp_range = np.array(fluids["Temp-degC"].unique())
            # st.slider(
            #     "Temperature (deg C)",
            #     min_value=float(temp_range.min()),
            #     max_value=float(temp_range.max()),
            #     step=3.5,
            #     key="temp",
            # )
            # st.slider(
            #     "Patchiness (small is patchy)",
            #     min_value=0.0,
            #     max_value=1.0,
            #     value=1.0,
            #     step=0.1,
            #     key="patch",
            # )
        with col2:
            state.current_model = st.radio(
                label="Rock Physics Model",
                options=[
                    "Hudson",
                    "Gassmann",
                    "SLS",
                    "Chapman",
                    "White",
                    "Continuous Random Medium",
                ],
            )
        with col3:
            st.write(
                f"{state.current_fluid} displacing water using {state.current_model} model"
            )

        fluid1 = manFL.Fluid.from_presets(name="Water", temperature=23, pressure=16.0)
        # state.current_fluid = manFL.Fluid.from_presets(
        #     name=state.current_fluid, temperature=52.0, pressure=16.0
        # )

        if (
            st.button("I have forward modelled my layer, let's do some AVO!")
            and state.file_uploaded
        ):
            state.layer_modelled = True
            advance()


def add_title_step_4(state):
    if state.layer_modelled:
        advance()
        hline()
        st.markdown(f"### Now choose the parameters for the rock physics model")
        state.current_parameters = st.slider(
            label="parameters",
            min_value=0,
            max_value=len(state.current_earth_model),
            step=1,
        )


def add_title_step_5(state):
    if state.layer_modelled:
        advance()
        hline()
        st.markdown(
            f"### Now choose an interface to see the AVO, fAVO, and AVA response"
        )
        if st.button("How about wavefield modelling?"):
            state.complete_simulation = True


def conclude(state):
    if state.complete_simulation:
        hline()
        st.write("### Thank you for using the app!")
        with st.form(key="my_form", clear_on_submit=True):
            st.write(
                """Please enter your email so that we send you a one-page report of your session. 
                Feel free (bot not obliged) to include any feedback you may have. We will only contact you 
                if you ask us to."""
            )
            feedback = st.text_input(label="Feedback")
            email = st.text_input(label="Email")
            submit_button = st.form_submit_button(label="Submit (resets the session)")
        if submit_button:
            set_all_states(state)
            st.toast("Thank you for your feedback!")


def input_query_text_area(state, status):
    if state.file is not None:
        status.info("Please enter your query...")
        col1, _ = st.columns([0.7, 0.3])

        with col1:
            state.query_method_one = st.text_area(
                "Please enter your query regarding uploaded file:"
            )

        if st.button("Save query"):
            state.save_query = True

    return state, status


def call_api(state, path_to_df: str, prompt: str):
    # print(path_to_df)
    # print(prompt)
    url = "http://localhost:8000/process_text/"
    params = {"path_to_df": path_to_df, "prompt": prompt}

    response = requests.get(url, params=params)
    result = response.json()["processed_text"]
    state.response_method_one = result[len("Output: ") :]

    return state


def generate_response(state, status):
    if state.que_response_gen:
        status.info("Ready for response generation!")

        st.write("----------------------------------------------------")

        if st.button("Ask query"):
            st.write("")
            with st.spinner("Generating response..."):
                # on_click=call_api, kwargs={"state": state, "path_to_df": state.file.name, "prompt": state.prompt_method_one}
                state = call_api(
                    state, path_to_df=state.file.name, prompt=state.prompt_method_one
                )

    return state, status


def display_response(state, status):
    if state.response_method_one is not None:
        status.info("Dislaying response")
        _, col2 = st.columns([0.3, 0.7])
        with col2:
            st.caption("Response:")
            st.success(state.response_method_one, icon="🤖")


def structured_pipeline(state, status):
    add_title_step_1()

    state = excel_csv_loading(state)

    state, status = convert_file_to_df(state, status)

    status = plot_earth_model(state, status)

    add_title_step_2(state)
    add_title_step_3(state)
    add_title_step_4(state)
    add_title_step_5(state)
    conclude(state)

    # state, status = input_query_text_area(state, status)
    # state = generate_proper_prompt(state)
    # state, status = generate_response(state, status)

    # display_response(state, status)

    return state, status

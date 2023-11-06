import streamlit as st
import pandas as pd
import requests
import mantis.rock_physics as manRP
import mantis.rock_physics.fluid as manFL
from mantis_vision.statefulness import *
import mantis_vision.base_functions as bf
import yagmail
import re  # for email validation
from PIL import Image


def hline():
    col1, col2, col3 = st.columns([0.4, 1, 0.4])
    with col1:
        st.write(" ")
    with col2:
        st.markdown(
            """<hr style="height:5px;border:2px solid #333333;
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

        except FileNotFoundError:
            st.write("File not found")
    with col3:
        st.write(" ")


def add_info_message(message: str):
    """
    Adding info message
    """
    st.info(
        f"""{message}""",
        icon="ℹ️",
    )


def format_title(title: str):
    st.markdown(f"### {title}")


def file_loading_process(state, status):
    format_title(
        "Start here. Upload a CSV or XLS file with four columns: Depth, Vp, Vs, Rho"
    )
    uploaded_file = st.file_uploader(label="", type=["xlsx", "csv"], key="input_file")

    # if uploaded_file is None:
    #     state.input_file = None
    #     # state = state_upload_file_none(state)

    # else:
    #     # file converted to numpy array for later processing

    #     state.input_file = uploaded_file
    #     if state.input_file.name.endswith(".csv"):
    #         state.current_earth_model = pd.read_csv(state.input_file, dtype=float)
    #     elif state.file.name.endswith(".xlsx"):
    #         state.current_earth_model = pd.read_excel(state.input_file, dtype=float)
    #     state.file_path = state.input_file.name
    #     # state.current_earth_model = state.file_path
    if state.input_file.name.endswith(".csv"):
        state.current_earth_model = pd.read_csv(state.input_file, dtype=float)
    elif state.file.name.endswith(".xlsx"):
        state.current_earth_model = pd.read_excel(state.input_file, dtype=float)
    status.info("First load an earth model")

    state.file_uploaded = True
    status.info("Current Earth Model")
    with st.sidebar:
        state.current_earth_model_plot = bf.plot_1d_model(state.current_earth_model)
        st.write("")
        # st.write(state.current_earth_model)
        st.write(state.current_earth_model_plot)


def add_title_step_1():
    """
    Adding title for step 1 - specifying file type
    """
    format_title(
        "Start here. Upload a CSV or XLS file with four columns: Depth, Vp, Vs, Rho"
    )


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
        status.info("Current Earth Model")
        state.current_earth_model_plot = bf.plot_1d_model(state.current_earth_model)
        # st.write("")
        # # st.write(state.current_earth_model)
        # # st.write(state.current_earth_model_plot)
        # status.info(state.current_earth_model_plot)
    return state, status


def add_title_step_2(state, status):
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
        -display["Depth"]
        + state.current_earth_model.iloc[state.current_layer + 1]["Depth"],
        1,
    )
    st.write(display)

    # status.info(f"Layer {state.current_layer} chosen")


def add_title_step_3(state):
    st.markdown(
        f"### Now choose the fluid that will displace water and a rock physics model"
    )
    col1, col2, col3 = st.columns([0.3, 0.3, 1])
    with col1:
        second_fluid = st.radio(
            label="Displacement Fluid",
            options=["CarbonDioxide", "Hydrogen", "Methane"],
        )
        fluid1 = manFL.Fluid.from_presets(name="Water", temperature=23, pressure=16.0)
        fluid2 = manFL.Fluid.from_presets(
            name=second_fluid, temperature=23, pressure=16.0
        )
        state.current_fluid = manFL.FluidMix(fluid1=fluid1, fluid2=fluid2)

        state.current_fluid_plot = bf.fluid_mix_plot(
            state.current_fluid, title="Fluid properties"
        )
        with st.expander("Advanced"):
            pres_range = bf.fluid_data["Pres-MPa"].unique()
            st.slider(
                "Pressure (MPa)",
                min_value=int(pres_range.min()),
                max_value=int(pres_range.max()),
                step=5,
                key="pres",
            )
            temp_range = bf.fluid_data["Temp-degC"].unique()
            st.slider(
                "Temperature (deg C)",
                min_value=float(temp_range.min()),
                max_value=float(temp_range.max()),
                step=3.5,
                key="temp",
            )

    with col2:
        model = st.radio(
            label="Rock Physics Model",
            options=[
                "Gassmann",
                "SLS",
                "White",
                "Hudson",
                "Chapman",
                # "Continuous Random Medium",
            ],
        )
        for key, val in bf.model_parameters_dict[model].items():
            if key not in state and key != "identifier":
                state[key] = val["default"]
        params_dict = state.current_earth_model.iloc[state.current_layer][1:].to_dict()
        layer_parameters = {key: float(val) for key, val in params_dict.items()}
        model_parameters = {
            key: state[key]
            for key, val in bf.model_parameters_dict[model].items()
            if key != "identifier"
        }
        fluid = {"fluid": state.current_fluid}
        # st.write(model_parameters)

        state.current_parameters = {**layer_parameters, **fluid, **model_parameters}
        st.write(state.current_parameters)
        state.current_model = manRP.models(
            identifier=bf.model_parameters_dict[model]["identifier"],
            **state.current_parameters,
        )

        state.current_model_plot = bf.rock_plot(state.current_model.Cij)
        with st.expander("Advanced"):
            try:
                params = bf.model_parameters_dict[model]
                for key, value in params.items():
                    if key != "fluid" and key != "identifier":
                        st.slider(
                            label=value["description"],
                            min_value=value["min"],
                            max_value=value["max"],
                            key=key,
                            step=value["step"],
                        )
            except KeyError:
                pass
    with col3:
        radio = st.radio(
            "plots", options=["fluid properties", "rock properties", "cij"]
        )
        cij_container = st.container()
        st.write(f"{second_fluid} displacing water using {model} model")
        if radio == "fluid properties":
            cij_container.write(state.current_fluid_plot)
        elif radio == "rock properties":
            cij_container.write(state.current_model_plot)
        elif radio == "cij":
            cij_container.write(
                bf.format_XY(state.current_model.Cij()), unsafe_allow_html=True
            )
            # cij_container.write(bf.plot_rock_properties(state.current_model))
    # state.current_fluid = manFL.Fluid.from_presets(
    #     name=state.current_fluid, temperature=52.0, pressure=16.0
    # )

    # if (
    #     st.button("I have forward modelled my layer, let's do some AVO!")
    #     and state.file_uploaded
    # ):
    #     state.layer_modelled = True
    #     advance()


def add_title_step_4(state):
    if state.layer_modelled:
        st.markdown(f"### Now choose the parameters for the rock physics model")
        state.current_parameters = st.slider(
            label="parameters",
            min_value=0,
            max_value=len(state.current_earth_model),
            step=1,
        )


def add_title_step_5(state):
    if state.layer_modelled:
        st.markdown(
            f"### Now choose an interface to see the AVO, fAVO, and AVA response"
        )
        if st.button("How about wavefield modelling?"):
            state.complete_simulation = True


def structured_pipeline(state, status):
    if "stage" not in st.session_state:
        st.session_state.stage = 0

    def set_state(i):
        st.session_state.stage = i

    def set_state_after_email(email: str):
        if re.fullmatch(bf.regex, email) is None:
            st.write("Email not sent or invalid email address")
            st.toast("Thank you for your participation!")
        else:
            try:
                yag = yagmail.SMTP(
                    "mantis.from.image@gmail.com",
                    # oauth2_file=".streamlit/credentials.json",
                    oauth2_file=".streamlit/credentials.json",
                )
                yag.send(to=email, subject="test")
            except Exception as e:
                st.write(e)
            st.toast("Thank you for your feedback!")

    with st.sidebar:
        container = st.container()
    if st.session_state.stage == 0:
        status.info(f"First Choose an earth model")
        st.button("sd", on_click=set_state, args=[1])

    if st.session_state.stage >= 1:
        format_title(
            "Start here. Upload a CSV or XLS file with four columns: Depth, Vp, Vs, Rho"
        )
        state.input_file = st.file_uploader(
            label="", type=["xlsx", "csv"], on_change=set_state, args=[2]
        )
        if state.input_file is not None:
            if state.input_file.name.endswith(".csv"):
                state.current_earth_model = pd.read_csv(state.input_file)
            elif state.file.name.endswith(".xlsx"):
                state.current_earth_model = pd.read_excel(state.input_file)
            state.file_path = state.input_file.name
            state.current_earth_model_plot = bf.plot_1d_model(state.current_earth_model)
            container.write(state.current_earth_model_plot)
            # state.current_earth_model_plot = bf.plot_1d_model(state.current_earth_model)

    if st.session_state.stage >= 2:
        if state.current_earth_model_plot is None:
            st.write("Please upload a valid file first")
            set_state(1)
        else:
            add_title_step_2(state, status)

            # st.write(len(state.current_earth_model))
            st.button(
                "I have chosen my layer, let's do some rock physics on that layer.",
                on_click=set_state,
                args=[3],
            )
            # color = st.selectbox(
            #     "Pick a Color",
            #     [None, "red", "orange", "green", "blue", "violet"],
            #     on_change=set_state,
            #     args=[3],
            # )
            # if color is None:
            #     set_state(2)
    if st.session_state.stage >= 3:
        add_title_step_3(state)
        add_title_step_4(state)
        st.button(
            "I have forward modelled my layer, let's do some AVO!",
            on_click=set_state,
            args=[4],
        )
    if st.session_state.stage >= 4:
        st.button(
            "Enough AVO, let's see some synthetically generated wavefields!",
            on_click=set_state,
            args=[5],
        )
    # if st.session_state.stage >= 5:
    #     st.button(
    #         "",
    #         on_click=set_state,
    #         args=[6],
    #     )
    if st.session_state.stage >= 5:
        st.write(f"Thank you!")
        with st.form(key="my_form", clear_on_submit=True):
            st.write(
                """Please enter your email so that we send you a one-page report of your session. 
                Feel free (bot not obliged) to include any feedback you may have. We will only contact you 
                if you ask us to."""
            )
            feedback = st.text_input(label="Feedback")
            st.text_input(
                label="Email (optional, but required for the report)",
                key="user_email",
            )

            def callback(arg):
                set_state_after_email(state.user_email)
                set_state(arg)

            submit_button = st.form_submit_button(
                label="Submit and/or restart session", on_click=callback, args=[0]
            )
            # if submit_button:
            #     # set_state_after_email(state.user_email)
            #     st.toast("Let's see if this works!")

    return state, status


def structured_pipeline_old(state, status):
    hline()
    add_title_step_1()

    state = excel_csv_loading(state)
    if state.input_file is not None:
        state, status = convert_file_to_df(state, status)

        state, status = plot_earth_model(state, status)
    # hline()

    # add_info_message(
    #     "Good job loading an earth model! Now let's select a layer to do some rock physics in"
    # )
    # advance()
    # hline()
    # add_title_step_2(state, status)
    # hline()
    # if state.layer_modelled:
    #     add_info_message(
    #         "Ace! Now let's choose a fluid and a rock physics model to do some forward modelling"
    #     )
    #     advance()
    #     hline()
    #     add_title_step_3(state)
    #     add_title_step_4(state)
    #     hline()

    # hline()
    # add_title_step_5(state)
    # hline()
    state = conclude(state)

    return state, status


def conclude(state):
    st.write("### Thank you for using the app!")

    def form_reset():
        reset_state(st.session_state)
        st.toast("Thank you for your feedback!")

    with st.form(key="my_form", clear_on_submit=True):
        st.write(
            """Please enter your email so that we send you a one-page report of your session. 
            Feel free (bot not obliged) to include any feedback you may have. We will only contact you 
            if you ask us to."""
        )
        feedback = st.text_input(label="Feedback")
        email = st.text_input(label="Email")
        submit_button = st.form_submit_button(
            label="Submit (resets the session)", on_click=form_reset
        )
        if submit_button:
            st.experimental_rerun()

    return state

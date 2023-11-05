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


def load_1d_model():
    uploaded_file = st.file_uploader(label="", type=["xlsx", "csv"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            st.session_state.input_file = pd.read_csv(uploaded_file, dtype=float)
        elif uploaded_file.name.endswith(".xlsx"):
            st.session_state.input_file = pd.read_excel(uploaded_file, dtype=float)
    if st.session_state.input_file is not None:
        st.toast("File uploaded")


def plot_1d_model_to_sidebar(df: pd.DataFrame):
    with st.sidebar:
        plt = bf.plot_1d_model(df)
        st.session_state.current_earth_model_plot = st.pyplot(plt)
        st.write(f"Current 1-d model")
        # st.info("File plotted")


def select_earth_layer():
    st.markdown(
        f"### Choose a layer that you want to change rock physics properties for"
    )
    st.session_state.current_layer = st.slider(
        label="layer number",
        min_value=0,
        max_value=len(st.session_state.input_file) - 2,
        step=1,
    )
    display = st.session_state.input_file.iloc[st.session_state.current_layer]

    display["Thickness"] = round(
        -display["Depth"]
        + st.session_state.input_file.iloc[st.session_state.current_layer + 1]["Depth"],
        1,
    )
    st.dataframe(display)


def choose_rock_physics_models():
    st.markdown(
        f"### Now choose the fluid that will displace water and a rock physics model"
    )
    (
        col1,
        col2,
    ) = st.columns([0.3, 0.3])
    with col1:
        second_fluid = st.radio(
            label="Displacement Fluid",
            options=["CarbonDioxide", "Hydrogen", "Methane"],
        )

        fluid1 = manFL.Fluid.from_presets(
            name="Water",
            temperature=st.session_state.temp,
            pressure=st.session_state.pres,
        )
        fluid2 = manFL.Fluid.from_presets(
            name=second_fluid,
            temperature=st.session_state.temp,
            pressure=st.session_state.pres,
        )
        st.session_state.current_fluid = manFL.FluidMix(fluid1=fluid1, fluid2=fluid2)

        st.session_state.current_fluid_plot = bf.fluid_mix_plot(
            st.session_state.current_fluid, title="Fluid properties"
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
                # "Chapman",
                # "Chapman",
                # "Continuous Random Medium",
            ],
        )
        for key, val in bf.model_parameters_dict[model].items():
            if key not in st.session_state and key != "identifier":
                st.session_state[key] = val["default"]
        params_dict = st.session_state.input_file.iloc[st.session_state.current_layer][
            1:
        ].to_dict()
        layer_parameters = {key: float(val) for key, val in params_dict.items()}
        model_parameters = {
            key: st.session_state[key]
            for key, val in bf.model_parameters_dict[model].items()
            if key != "identifier"
        }
        model_parameters = {
            key: (
                10**val
                if (
                    key == "permeability"
                    or key == "bubble_radius"
                    or key == "aspect_ratio"
                )
                else val
            )
            for key, val in model_parameters.items()
        }
        fluid = {"fluid": st.session_state.current_fluid}

        st.session_state.current_parameters = {
            **layer_parameters,
            **fluid,
            **model_parameters,
        }
        st.session_state.current_model = manRP.models(
            identifier=bf.model_parameters_dict[model]["identifier"],
            **st.session_state.current_parameters,
        )
        st.session_state.current_fluid.saturation = 0.8
        # st.write(
        #     st.session_state.current_model, st.session_state.current_fluid.saturation
        # )

        st.session_state.current_model_plot = bf.rock_plot(
            st.session_state.current_model.Cij
        )
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
    st.markdown(
        f"### {second_fluid} displacing water using {model} model at 80% saturation"
    )


def plot_rock_physics_models():
    radio = st.radio("plots", options=["fluid properties", "rock properties", "cij"])
    cij_container = st.container()

    if radio == "fluid properties":
        cij_container.write(st.session_state.current_fluid_plot)
    elif radio == "rock properties":
        cij_container.write(st.session_state.current_model_plot)
    elif radio == "cij":
        cij_container.write(
            bf.format_XY(st.session_state.current_model.Cij()), unsafe_allow_html=True
        )


# def plot_fAVO():
#     (
#         col1,
#         col2,
#     ) = st.columns([0.3, 0.3])
#     with col1:
#         second_fluid = st.radio(
#             label="Displacement Fluid",
#             options=["CarbonDioxide", "Hydrogen", "Methane"],
#         )

#         fluid1 = manFL.Fluid.from_presets(
#             name="Water",
#             temperature=st.session_state.temp,
#             pressure=st.session_state.pres,
#         )
#         fluid2 = manFL.Fluid.from_presets(
#             name=second_fluid,
#             temperature=st.session_state.temp,
#             pressure=st.session_state.pres,
#         )
#         st.session_state.current_fluid = manFL.FluidMix(fluid1=fluid1, fluid2=fluid2)

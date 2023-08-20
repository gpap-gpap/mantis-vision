from __future__ import annotations
from typing import Callable
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import pandas as pd
import mantis.rock_physics.fluid as manFL
import mantis.rock_physics as manRP
import numpy as np

# from mantis.rock_physics.fluid import fluid_data as fd


expected_logs = ["Depth", "Vp", "Vs", "Rho"]

fluid_data = pd.DataFrame(manFL.fluid_data)

model_parameters_dict = {
    "SLS": {
        "Q_sls": {
            "description": "Quality factor",
            "min": 5,
            "max": 50,
            "step": 5,
            "default": 10,
        },
        "Log_omega_ref": {
            "description": "Transition Frequency",
            "min": -2.0,
            "max": 7.0,
            "step": 0.5,
            "default": 0.0,
        },
    },
}


# def model_to_input_parameters():
#     return


def plot_1d_model(dataframe: pd.DataFrame, highligh_layer: int = None):
    if dataframe is None:
        pass
    else:
        try:
            fig, axes = plt.subplots(figsize=(10, 15))
            curve_names = expected_logs

            depth, vp, vs, rho = tuple(expected_logs)
            ax1 = plt.subplot2grid((1, 3), (0, 0), rowspan=1, colspan=1)

            ax2 = plt.subplot2grid((1, 3), (0, 1), rowspan=1, colspan=1)

            ax3 = plt.subplot2grid((1, 3), (0, 2), rowspan=1, colspan=1)
            ax1.plot(vp, depth, drawstyle="steps", data=dataframe)
            ax2.plot(vs, depth, drawstyle="steps", data=dataframe)
            ax3.plot(rho, depth, drawstyle="steps", data=dataframe)
            for i, ax in enumerate(fig.axes):
                ax.set_ylim(0, 1100)  # Set the depth range
                ax.invert_yaxis()
                ax.grid()
                ax.set_xlabel(curve_names[i + 1])

            for ax in [ax2, ax3]:
                plt.setp(ax.get_yticklabels(), visible=False)

            # Reduce the space between each subplot
            fig.subplots_adjust(wspace=0.1)
            return fig
        except (AttributeError, ValueError):
            return None


def fluid_mix_plot(f: manFL.FluidMix, title: str = ""):
    def fluid(sw: float, patch_parameter: float = 1.0):
        f.saturation = sw
        f.patch_q = patch_parameter
        result = (f.modulus, f.density, f.viscosity, *(f.effectivePermeability))
        return result

    mod1, mod2 = f.fluid1.modulus, f.fluid2.modulus
    saturation = np.linspace(0, 1, 100)
    plots = {}
    plots["uniform"] = np.array([fluid(sw, 1) for sw in saturation])
    plots["intermediate"] = np.array([fluid(sw, 5 * mod2 / mod1) for sw in saturation])
    plots["patchy"] = np.array([fluid(sw, 2 * mod2 / mod1) for sw in saturation])

    fig, ax = plt.subplots(3, 1, figsize=(10, 8))
    # fig.tight_layout()
    # plt.subplots_adjust(wspace=4, hspace=None)
    fig.subplots_adjust(hspace=0.1)
    ax[0].set_ylabel("Fluid Modulus (GPa)")
    ax[0].set_title(title)
    for key, value in plots.items():
        ax[0].plot(saturation, value[:, 0], label=key)
    ax[0].legend()
    ax[0].set_xticklabels([])

    # ax[1].set_ylabel("Fluid Density (gr/cc)")

    # for key, value in plots.items():
    #     ax[1].plot(saturation, value[:, 1], label=key)
    # ax[1].set_xticklabels([])
    ax[1].set_ylabel("Fluid effective mobility")

    for key, value in plots.items():
        ax[1].plot(saturation, 1 / value[:, 2], label=key)
        ax[1].set_yscale("log")
    ax[1].set_xticklabels([])
    ax[2].set_xlabel("Water Saturation")
    ax[2].set_ylabel("Relative Permeability")

    ax[2].plot(saturation, plots["uniform"][:, 3], label=f.fluid1.name)
    ax[2].plot(saturation, plots["uniform"][:, 4], label=f.fluid2.name)
    ax[2].legend()

    return fig


def rock_plot(cij: Callable = None):
    freq = np.logspace(-2.0, 7.0, 50)
    moduli = np.real(np.stack([cij(i) for i in freq]))
    try:
        fig, ax = plt.subplot(1, 1, figsize=(15, 15))
        ax.set_xlabel("log frequency")
        ax.set_ylabel("rock elastic modulus (MPa)")
        ax.plot(freq, moduli[:, 0, 0], linewidth=5, label="$C_{11}$")
        ax.plot(freq, moduli[:, 1, 1], linewidth=4, label="$C_{22}}$")
        ax.plot(freq, moduli[:, 2, 2], label="$C_{33}$")
        ax.legend(bbox_to_anchor=[0.9, 0.3], labelcolor="linecolor")
        # for i, ax in enumerate(fig.axes):
        #     ax.set_ylim(700, 1100) # Set the depth range
        #     ax.invert_yaxis()
        #     ax.grid()
        #     ax.set_xlabel(curve_names[i+1])

        # for ax in [ax2, ax3]:
        #     plt.setp(ax.get_yticklabels(), visible = False)

        # Reduce the space between each subplot
        fig.subplots_adjust(wspace=0.1)
        return fig
    except (AttributeError, ValueError):
        return "no model loaded"


def add_line(fig: plt.Figure, depth: float = 0.0):
    fig.add_artist(lines.Line2D([0, 10000], [depth, depth]))
    return fig


frequency_axis = np.linspace(-2.0, 7.0, 50)
saturation_axis = np.linspace(0, 1, 50)


# def plot_rock_fluid(cij: Callable | None = None, fluid: manFL.FluidMix = None):
#     def fl_modulus(saturation: float):
#         fluid.saturation = saturation
#         return fluid.modulus

#     try:
#         fl_data = [fl_modulus(s) for s in saturation]
#         moduli_data = [real(cij(i)) for i in freq]

#         # for i, ax in enumerate(fig.axes):
#         #     ax.set_ylim(700, 1100) # Set the depth range
#         #     ax.invert_yaxis()
#         #     ax.grid()
#         #     ax.set_xlabel(curve_names[i+1])

#         # for ax in [ax2, ax3]:
#         #     plt.setp(ax.get_yticklabels(), visible = False)

#         # Reduce the space between each subplot
#         fig.subplots_adjust(wspace=0.1)
#         return fig
#     except (AttributeError, ValueError):
#         return "no model loaded"
#     fig, axes = plt.subplots(figsize=(15, 15))
#     ax1 = plt.subplot2grid((2, 1), (0, 0), rowspan=1, colspan=1)
#     ax2 = plt.subplot2grid((2, 1), (1, 0), rowspan=1, colspan=1)

#     ax1.set_xlabel("Water Saturation")
#     ax1.set_ylabel("Fluid modulus (MPa)")
#     ax1.plot(saturation, fl_data)
#     ax1.plot(s1, fluid(s1), "o", markersize=20)
#     ax1.text(
#         0.1,
#         fluid(0.99),
#         f"Water {fluid(1)} MPa, \n{st.session_state.current_fluid}: {fluid(0)} MPa",
#         color="black",
#         fontsize=15,
#     )

#     ax2.set_xlabel("log frequency")
#     ax2.set_ylabel("rock elastic modulus (MPa)")
#     ax2.plot(freq, moduli[:, 0, 0], linewidth=5, label="$C_{11}$")
#     ax2.plot(freq, moduli[:, 1, 1], linewidth=4, label="$C_{22}}$")
#     ax2.plot(freq, moduli[:, 2, 2], label="$C_{33}$")
#     ax2.legend(bbox_to_anchor=[0.9, 0.3], labelcolor="linecolor")

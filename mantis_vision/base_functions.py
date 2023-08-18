import matplotlib.pyplot as plt
import pandas as pd
from mantis.rock_physics.fluid import fluid_data as fd

expected_logs = ["Depth(m)", "Vp(Km/s)", "Vs(Km/s)", "Rho(g/cm3)"]

fluid_data = pd.DataFrame(fd)


def plot_1d_model(dataframe: pd.DataFrame, highligh: int = None):
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
            return "no model loaded"


def plot_rock_fluid(cij: Callable = None, fluid: Callable = None, s1: float = None):
    try:
        fl_data = [fluid(s) for s in saturation]
        moduli = np.real(np.stack([cij(i) for i in freq]))
        fig, axes = plt.subplots(figsize=(15, 15))
        ax1 = plt.subplot2grid((2, 1), (0, 0), rowspan=1, colspan=1)
        ax2 = plt.subplot2grid((2, 1), (1, 0), rowspan=1, colspan=1)

        ax1.set_xlabel("Water Saturation")
        ax1.set_ylabel("Fluid modulus (MPa)")
        ax1.plot(saturation, fl_data)
        ax1.plot(s1, fluid(s1), "o", markersize=20)
        ax1.text(
            0.1,
            fluid(0.99),
            f"Water {fluid(1)} MPa, \n{st.session_state.current_fluid}: {fluid(0)} MPa",
            color="black",
            fontsize=15,
        )

        ax2.set_xlabel("log frequency")
        ax2.set_ylabel("rock elastic modulus (MPa)")
        ax2.plot(freq, moduli[:, 0, 0], linewidth=5, label="$C_{11}$")
        ax2.plot(freq, moduli[:, 1, 1], linewidth=4, label="$C_{22}}$")
        ax2.plot(freq, moduli[:, 2, 2], label="$C_{33}$")
        ax2.legend(bbox_to_anchor=[0.9, 0.3], labelcolor="linecolor")
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

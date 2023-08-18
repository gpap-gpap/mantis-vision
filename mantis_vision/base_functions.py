import matplotlib.pyplot as plt
import pandas as pd

expected_logs = ["Depth(m)", "Vp(Km/s)", "Vs(Km/s)", "Rho(g/cm3)"]


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

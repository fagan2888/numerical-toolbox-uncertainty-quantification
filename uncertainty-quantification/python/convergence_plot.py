import matplotlib.pyplot as plt
import pandas as pd


def convergence_plot(sample, expected, qoi_name, absolute_deviation=False):
    """
    This function is a custom-made convergence plot for some Monte-Carlo
    sample.

    Parameters
    ----------
    sample: Series, 1d-array, or list.
        A vector of random observations.
    expected: float, int.
        Expected value of sample mean.
    qoi_name: str
        Label of y-axis.
    absolute_deviation: bool
        Plots absolute deviation of means to zero expectation value.

    Returns
    -------
    dp: Figure
        Returns Figure object setting figure-level attributes.

    """
    plt.style.use("../_configs/uq.mplstyle")

    df = pd.DataFrame(sample, columns=["qoi_realization"])
    df["cum_sum"] = df["qoi_realization"].cumsum()
    df["mean_iteration"] = df["cum_sum"] / (df.index.to_series() + 1)

    fig, ax = plt.subplots()

    if absolute_deviation is not True:
        # Compute sample mean for each iteration
        title = "Convergence of Monte-Carlo Uncertainty Propagation (level)"
        file_str = "level"
        legend_loc = "lower right"

        conv_plot, = ax.plot(
            df.index + 1, df["mean_iteration"], lw=3.0, label="Sample Mean"
        )

    else:
        title = "Convergence of MC Uncertainty Propagation (absolute deviation)"
        file_str = "abs_dev"
        legend_loc = "upper right"

        conv_plot, = ax.plot(
            df.index + 1,
            abs(df["mean_iteration"] - expected),
            lw=3.0,
            label="Sample Mean",
        )
        expected = 0

    # Plot expected value.
    exp_plot = ax.hlines(
        expected,
        1,
        len(sample),
        lw=2.5,
        linestyle="--",
        label="Under Mean Parametrization",
    )

    ax.set_title(title, fontsize=28, y=1.05)
    ax.set_xlim(1, len(sample))
    ax.grid(True, linestyle=(0, (5, 10)))
    ax.set_ylabel(qoi_name, fontsize=24, labelpad=14)
    ax.set_xlabel("Number of iterations", fontsize=24, labelpad=14)
    ax.tick_params(axis="both", labelsize=20)
    ax.legend(
        handles=[exp_plot, conv_plot],
        fontsize=20,
        loc=legend_loc,
        edgecolor="black",
        fancybox=False,
    )

    plt.savefig("figures/convergence_plot_{}.png".format(file_str), bbox_inches="tight")

    return plt

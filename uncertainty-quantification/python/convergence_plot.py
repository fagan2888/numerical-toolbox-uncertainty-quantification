import matplotlib.pyplot as plt
import pandas as pd


def convergence_plot(sample, expected, y_label):
    """
    This function is a custom-made convergence plot for some Monte-Carlo
    sample.

    Parameters
    ----------
    sample: Series, 1d-array, or list.
        A vector of random observations.
    expected: float, int.
        Expected value of sample mean.

    Returns
    -------
    dp: Figure
        Returns Figure object setting figure-level attributes.
    ax: Axes
        Returns Axes object for setting axes attributes.

    """
    # Compute sample mean for each iteration
    df = pd.DataFrame(sample, columns=["qoi_realization"])
    df["cum_sum"] = df["qoi_realization"].cumsum()
    df["mean_iteration"] = df["cum_sum"] / (df.index.to_series() + 1)

    fig, ax = plt.subplots(figsize=(12, 9))

    conv_plot, = ax.plot(
        df.index + 1, df["mean_iteration"], lw=2.5, label="Sample mean"
    )

    # Plot expected value.
    exp_plot = ax.hlines(
        expected, 1, len(sample), lw=2.0, linestyle="--", label="Expected value"
    )

    ax.set_title("Convergence of Monte-Carlo Uncertainty Propagation", fontsize=24)
    ax.set_xlim(1, len(sample))
    ax.grid(True, linestyle=(0, (5, 10)))
    ax.set_ylabel(y_label, fontsize=22, labelpad=14)
    ax.set_xlabel("Number of iterations", fontsize=22, labelpad=14)
    ax.tick_params(axis="both", labelsize=14)
    ax.legend(
        handles=[exp_plot, conv_plot],
        fontsize=18,
        loc="upper right",
        edgecolor="black",
        fancybox=False,
    )

    plt.savefig("figures/convergence_plot.png", bbox_inches="tight")

    return plt

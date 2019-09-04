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
        expectation value of sample mean.

    Returns
    -------
    dp: Figure
        Returns Figure object setting figure-level attributes.
    ax: Axes
        Returns Axes object for setting axes attributes.

    """
    df = pd.DataFrame(sample, columns=["qoi_realization"])
    df["cum_sum"] = df["qoi_realization"].cumsum()
    df["mean_iteration"] = df["cum_sum"] / (df.index.to_series() + 1)

    plt.figure(figsize=(12, 9))
    plt.title("Convergence of Monte-Carlo Uncertainty Propagation", fontsize=24)

    conv_plot, = plt.plot(
        df.index + 1, df["mean_iteration"], lw=2.5, label="MC Convergence"
    )

    # Plot expected.
    exp_plot = plt.hlines(
        expected, 1, len(sample), lw=2.0, linestyle="--", label="Expected value"
    )

    plt.xlim(1, len(sample))
    plt.grid(True, linestyle=(0, (5, 10)))

    # Make sure that all labels are large enough -
    plt.ylabel(y_label, fontsize=22, labelpad=14)
    plt.xlabel("Number of iterations", fontsize=22, labelpad=14)

    # Ensure axis ticks are large enough to be easily read.
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)

    plt.legend(
        handles=[exp_plot, conv_plot],
        fontsize=18,
        loc="upper right",
        edgecolor="black",
        fancybox=False,
    )

    plt.savefig("figures/convergence_plot.png", bbox_inches="tight")

    return plt

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def distplot(sample, qoi_name):
    """
    This function is a custom-made wrapper around seaborn.distplot.

    Parameters
    ----------
    sample: Series, 1d-array, or list.
        A vector of random observations.

    Returns
    -------
    dp: Figure
        Returns Figure object setting figure-level attributes.
    qoi_name: str
        Name of Quantity of interest used for x label and png-name.

    """
    plt.style.use("_configs/uq.mplstyle")

    fig, ax = plt.subplots()

    # Plot mean as vertical line.
    mean = ax.axvline(
        np.mean(sample), color="#3F5D7D", linestyle="--", lw=4, label="Sample Mean"
    )

    # Call seaborn.distplot and set options.
    dp = sns.distplot(
        sample,
        hist=True,
        kde=True,
        bins=100,
        color="#3F5D7D",
        norm_hist=True,
        hist_kws={"edgecolor": "#3F5D7D"},
        kde_kws={"linewidth": 5},
    )

    ax.set_title("Distribution of {}".format(qoi_name), y=1.05)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylabel("Kernel Density Estimate", labelpad=30)
    ax.legend(handles=[mean], edgecolor="white")

    plt.savefig("figures/distplot_{}.png".format(qoi_name), bbox_inches="tight")

    return dp

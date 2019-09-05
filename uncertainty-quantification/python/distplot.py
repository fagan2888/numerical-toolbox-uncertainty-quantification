import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def distplot(sample):
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

    """
    fig, ax = plt.subplots(figsize=(12, 9))

    # Plot mean as vertical line.
    mean = ax.axvline(
        np.mean(sample), color="#3F5D7D", linestyle="--", lw=4, label="Sample mean"
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

    ax.set_title("Distribution of Quantity of Interest", fontsize=28, y=1.05)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="both", labelsize=20)
    ax.set_ylabel("Kernel Density Estimate", fontsize=24)
    ax.legend(handles=[mean], fontsize=20, edgecolor="white")

    plt.savefig("figures/distplot.png", bbox_inches="tight")

    return dp

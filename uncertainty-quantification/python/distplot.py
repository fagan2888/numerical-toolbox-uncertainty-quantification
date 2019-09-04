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
    ax: Axes
        Returns Axes object for setting axes attributes.

    Notes
    -----
    `xlabel` and file-title are left to be set outside `custom_distplot` call.

    """
    # Common sizes: (10, 7.5) and (12, 9): ~1.33x wider than tall.
    plt.figure(figsize=(12, 9))

    plt.title("Distribution of Quantity of Interest", fontsize=24)

    # Remove plot frame lines
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Set axis ticks size
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    # Set y-axis label.
    plt.ylabel("Kernel Density Estimate", fontsize=22)

    # Plot mean as vertical line.
    mean = plt.axvline(
        np.mean(sample), color="#3F5D7D", linestyle="--", lw=3, label="Mean value"
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
        kde_kws={"linewidth": 4},
    )

    # Set legend.
    plt.legend(handles=[mean], fontsize=18, edgecolor="white")

    plt.savefig("figures/distplot.png", bbox_inches="tight")
    return dp, ax

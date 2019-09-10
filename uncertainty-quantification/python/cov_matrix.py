import numpy as np
import pandas as pd
import respy as rp


def create_cov_matrix():
    """
    This module computes the covariance matrix fo Keane and Wolpin (1994)
    based on the Standard Deviation of Estimated Paramters in table 4.1..
    It accounts for the the difference between respy and KW94 in two points:
    - The order of a-parameters differs
    - The factors for cross-experience are multiplied by (-1) in respy

    Note
    ----
    - Correlations and Choleksy factors for same variables are the same only in
      this peculiar case of data set 1 parametrization.
    - The code is written simple and explicit in order to be easy to check
      and to update.

    """
    params, options = rp.get_example_model("kw_94_one", with_data=False)

    df = pd.read_csv("csv/table41_kw_94.csv", sep=",", index_col=0)
    df["var"] = df["sd"] ** 2

    cov = np.zeros((len(params), len(params)))

    # alphas, betas and gamma order coincides in respy and KW94.
    np.fill_diagonal(cov[1:17, 1:17], df["var"][0:16])

    # as: Attentation! order in respy differs from KW94.

    # diagonal
    cov[17, 17] = df.loc["a11", "var"]
    cov[18, 18] = df.loc["a22", "var"]
    cov[19, 19] = df.loc["a33", "var"]
    cov[20, 20] = df.loc["a44", "var"]

    # non-diagonal
    cov[21, 21] = df.loc["a21", "var"]
    cov[22, 22] = df.loc["a31", "var"]
    cov[23, 23] = df.loc["a32", "var"]
    cov[24, 24] = df.loc["a41", "var"]
    cov[25, 25] = df.loc["a42", "var"]
    cov[26, 26] = df.loc["a43", "var"]

    return cov

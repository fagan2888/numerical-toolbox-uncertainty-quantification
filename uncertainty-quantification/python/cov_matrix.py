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

    Return
    ------
    cov_df (DataFrame):
        Covariance Matrix labeled by variable names on both axes
    """
    # TODO: Generic for all respy example models, this refers to all the code.
    params, options = rp.get_example_model("kw_94_one", with_data=False)

    df = pd.read_csv("csv/table41_kw_94.csv", sep=",", index_col=1)
    df["var"] = df["sd"] ** 2

    cov_df = pd.DataFrame(
        data=np.zeros((len(df["var"]), len(df["var"]))),
        index=df["parameter"].values,
        columns=df["parameter"].values,
    )

    # alphas, betas and gamma order coincides in respy and KW94.
    np.fill_diagonal(cov_df.values, df["var"].values)

    return cov_df

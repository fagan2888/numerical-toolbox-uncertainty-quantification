"""
This module computes the covariance matrix fo Keane and Wolpin (1994)
based on the Standard Deviation of Estimated Paramters in table 4.1..
It accounts for the the difference between respy and KW94 in three points:
- The order of parameters differs
- The factors for cross-experience are multiplied by -100 in respy
- beta2 is MINUS is_return_highschool and MINUS is_return_not_highschool.
"""
import json

import numpy as np
import pandas as pd
import respy as rp


def var_epsilon(mean_left, mean_right, var_left, var_right):
    """
    Computes the Variance of the sum of the product of a number of pairs
    of random variables. All random variables in the sum are iid.

    Paramters
    ---------
    mean_left: array_like
        1d-vector of means.
    mean_right: array_like
        1d-vector of means.
    var_left: array_like
        1d-vector of variances.
    var_right: array_like
        1d-vector of variances.

    Returns
    -------
    var: int
        Variance of the sum of the product of a number of pairs
        of random variables.

    Notes
    -----
    The formula for the product of independent variables can be found at
    https://en.wikipedia.org/wiki/Variance#Product_of_independent_variables.

    """
    assert (
        len(mean_left) == len(mean_right) == len(var_left) == len(var_right)
    ), "Mean and var vectors must have same length."

    sub_vars = []

    for i in range(len(mean_left)):
        sub_var_temp = (
            (mean_left[i] ** 2 * var_right[i])
            + (mean_right[i] ** 2 * var_left[i])
            + (var_left[i] * var_right[i])
        )
        sub_vars.append(sub_var_temp)

    var = sum(sub_vars)

    return var


params, options = rp.get_example_model("kw_94_one", with_data=False)

df = pd.read_csv("../csv/table41_columns_kw_94.csv", sep=",", index_col=0)
df["var"] = df["sd"] ** 2

cov = np.zeros((len(params), len(params)))

# alpha1s
cov[1, 1] = df.loc["alpha10", "var"]
cov[2, 2] = df.loc["alpha11", "var"]
cov[3, 3] = df.loc["alpha12", "var"]

# transformed cross-experience
cov[4, 4] = (df.loc["alpha13", "sd"] * (-100)) ** 2

# alpha2s
cov[18, 18] = df.loc["alpha20", "var"]
cov[19, 19] = df.loc["alpha21", "var"]
cov[22, 22] = df.loc["alpha22", "var"]
cov[20, 20] = df.loc["alpha24", "var"]

# transformed cross-experience
cov[23, 23] = (df.loc["alpha23", "sd"] * (-100)) ** 2
cov[21, 21] = (df.loc["alpha25", "sd"] * (-100)) ** 2

# betas
cov[36, 36] = -df.loc["beta2", "var"]
cov[37, 37] = -df.loc["beta2", "var"]

# gamma
cov[42, 42] = df.loc["gamma0", "var"]

# epsilons
eta_mean = [0, 0, 0, 0]
eta_var = [1, 1, 1, 1]

as_mean = df["true"].iloc[16:].tolist()
as_var = df["var"].iloc[16:].tolist()

cov[47, 47] = var_epsilon([as_mean[0]], [eta_mean[0]], [as_var[0]], [eta_var[0]])

cov[48, 48] = var_epsilon(as_mean[1:3], eta_mean[0:2], as_var[1:3], eta_var[0:2])

cov[49, 49] = var_epsilon(as_mean[3:6], eta_mean[0:3], as_var[3:6], eta_var[0:3])

cov[50, 50] = var_epsilon(as_mean[6:11], eta_mean[:4], as_var[6:11], eta_var[0:4])

cov_list = cov.tolist()

with open("../json/cov_list.json", "w") as write_file:
    json.dump(cov_list, write_file)

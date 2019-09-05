"""
This module computes the covariance matrix fo Keane and Wolpin (1994)
based on the Standard Deviation of Estimated Paramters in table 4.1.
It accounts for the the difference between respy and KW94 in three points:
- The order of parameters differs
- The factors for cross-experience are multiplied by -100 in respy
- Both use the Cholesky decomposition matrix elements
"""
import json

import numpy as np
import pandas as pd
import respy as rp

params, options = rp.get_example_model("kw_94_one", with_data=False)


df = pd.read_csv("table41_columns_kw_94.csv", sep=";", index_col=0)

cov = np.zeros((len(params), len(params)))

# alpha1s
cov[1, 1] = df.loc["alpha10", "sd"] ** 2
cov[2, 2] = df.loc["alpha11", "sd"] ** 2
cov[3, 3] = df.loc["alpha12", "sd"] ** 2

# transformed cross-experience
cov[4, 4] = (df.loc["alpha13", "sd"] * (-100)) ** 2

# alpha2s
cov[18, 18] = df.loc["alpha20", "sd"] ** 2
cov[19, 19] = df.loc["alpha21", "sd"] ** 2
cov[22, 22] = df.loc["alpha22", "sd"] ** 2
cov[20, 20] = df.loc["alpha24", "sd"] ** 2

# transformed cross-experience
cov[23, 23] = (df.loc["alpha23", "sd"] * (-100)) ** 2
cov[21, 21] = (df.loc["alpha25", "sd"] * (-100)) ** 2

# betas
cov[36, 36] = (-df.loc["beta1", "sd"] - df.loc["beta2", "sd"]) ** 2
cov[36, 36] = (-df.loc["beta1", "sd"] - df.loc["beta2", "sd"]) ** 2

# gamma
cov[42, 42] = df.loc["gamma0", "sd"] ** 2

# as
cov[47, 47] = df.loc["a11", "sd"] ** 2
cov[48, 48] = df.loc["a22", "sd"] ** 2
cov[49, 49] = df.loc["a33", "sd"] ** 2
cov[50, 50] = df.loc["a44", "sd"] ** 2

cov_list = cov.tolist()

with open("../json/cov_list.json", "w") as write_file:
    json.dump(cov_list, write_file)

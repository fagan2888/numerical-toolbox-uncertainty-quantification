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

# as

# diagonal
cov[47, 47] = df.loc["a11", "var"]
cov[48, 48] = df.loc["a22", "var"]
cov[49, 49] = df.loc["a22", "var"]
cov[50, 50] = df.loc["a22", "var"]

# non-diagonal
cov[47, 47] = df.loc["a21", "var"]
cov[47, 47] = df.loc["a31", "var"]
cov[47, 47] = df.loc["a32", "var"]
cov[47, 47] = df.loc["a41", "var"]
cov[47, 47] = df.loc["a42", "var"]
cov[47, 47] = df.loc["a43", "var"]

cov_list = cov.tolist()

with open("../json/cov_list.json", "w") as write_file:
    json.dump(cov_list, write_file)

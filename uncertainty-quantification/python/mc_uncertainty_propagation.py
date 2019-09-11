import json

import chaospy as cp
import numpy as np
import pandas as pd
import respy as rp
from python.model_wrapper import model_wrapper_kw_94


def mc_uncertainty_propagation(mean, cov, n_draws, save_json=False):
    """
    Conducts a Monte Carlo Uncertainty Propagation.
    To conduct the Monte Carlo Uncertainty Propagation, a large number of
    input parameters is drawn randomly given their joint distribution.
    For each input paramter vector, the Quantity of Interest (QoI) is computed
    by calling function model_wrapper_kw_94 from the module`model_wrapper.py`.
    This results in a distribution of the QoI. The example model is the
    Discrete Occupational Choice Dynamic Programing Model in
    Keane and Wolpin (1994). For more details see `model_wrapper.py`.

    Parameters
    ----------
    mean: pandas.Series
        Vector of mean of input parameters labeled by parameter names.
    cov: DataFrame
        Covariance Matrix labeled by variable names on both axes
    n_draws: int
        number of random draws of input parameters.
    save_json: bool
        Save qoi as json for later use, e.g. if runtime is high

    Returns
    -------
    QoI: list
        Sample of realizations of Quantity of Interest.
        Number of elements equals len(n_draws).

    Notes
    -----
    Here it is assumed that the joint distribution of input parameters is
    Normal.

    """
    distribution = cp.MvNormal(loc=mean, scale=cov)

    df = pd.read_csv("csv/table41_kw_94.csv", sep=",")

    qoi = [np.nan] * n_draws

    np.random.seed(187)
    draws = distribution.sample(n_draws)

    kw94_params = [
        pd.Series(data=draw.ravel(), index=df["parameter"].values) for draw in draws.T
    ]

    respy_params = [transform_params_kw94_respy(kwp) for kwp in kw94_params]
    qoi = [model_wrapper_kw_94(rp.values) for rp in respy_params]

    if save_json is True:
        with open("json/qoi.json", "w") as write_file:
            json.dump(qoi, write_file)
    else:
        pass

    return qoi


def transform_params_kw94_respy(kw94_params):
    """
    Transforms parameters vector in format of KW94 (see table 4.1)
    to respy format.
    It accounts for the the difference between respy and KW94 in two points:
    - The order of a-parameters differs
    - The factors for squared experience and beta2 are multiplied by (-1) in respy
    - KW94 specifyies the distribution of
    elements in a Cholesky Decomposition matrix but respy takes
    Standard deviations and Correlations.

    Parameters
    ----------
    kw94_params: pd.Series indexed by KW94 Paramter names
        Vector of model input parameters in KW94 format.

    Returns
    -------
    params: pd.Series indexed by respy Paramter names
        Vector of model input parameters in respy format.

    """
    assert len(kw94_params) == 26, "Length of KW94 vector must be 26."

    params, _ = rp.get_example_model("kw_94_one", with_data=False)

    respy_params = pd.Series(
        data=np.full(len(params["value"].values), np.nan), index=params.index
    )

    # Copy values that are not in KW94 from respy paramters.
    respy_params[("delta", "delta")] = params.loc[("delta", "delta"), "value"]
    respy_params[("meas_error", "sd_a")] = params.loc[("meas_error", "sd_a"), "value"]
    respy_params[("meas_error", "sd_b")] = params.loc[("meas_error", "sd_b"), "value"]

    # Set values that are transformed with *(-1) by respy
    # square experiences alphas
    respy_params[("wage_a", "exp_a_square")] = -kw94_params["alpha13"]
    respy_params[("wage_a", "exp_b_square")] = -kw94_params["alpha15"]
    respy_params[("wage_b", "exp_b_square")] = -kw94_params["alpha23"]
    respy_params[("wage_b", "exp_a_square")] = -kw94_params["alpha25"]
    # betas
    respy_params[("nonpec_edu", "at_least_twelve_exp_edu")] = -kw94_params["beta1"]
    respy_params[("nonpec_edu", "not_edu_last_period")] = -kw94_params["beta2"]

    # Set SDs and Corrs that are Cholesky elements in KW94.
    chol = np.zeros((4, 4))
    np.fill_diagonal(chol, kw94_params[["a11", "a22", "a33", "a44"]])
    chol[1, 0] = kw94_params["a21"]
    chol[2, :2] = [kw94_params["a31"], kw94_params["a32"]]
    chol[3, :3] = [kw94_params["a41"], kw94_params["a42"], kw94_params["a43"]]

    cov = np.matmul(chol, chol.T)
    sd = np.sqrt(np.diag(cov))

    respy_params[("shocks", "sd_a")] = sd[0]
    respy_params[("shocks", "sd_b")] = sd[1]
    respy_params[("shocks", "sd_edu")] = sd[2]
    respy_params[("shocks", "sd_home")] = sd[3]
    respy_params[("shocks", "corr_b_a")] = cov[1, 0] / (sd[1] * sd[0])
    respy_params[("shocks", "corr_edu_a")] = cov[2, 0] / (sd[2] * sd[0])
    respy_params[("shocks", "corr_edu_b")] = cov[2, 1] / (sd[2] * sd[1])
    respy_params[("shocks", "corr_home_a")] = cov[3, 0] / (sd[3] * sd[0])
    respy_params[("shocks", "corr_home_b")] = cov[3, 1] / (sd[3] * sd[1])
    respy_params[("shocks", "corr_home_edu")] = cov[3, 2] / (sd[3] * sd[2])

    # Fill in KW94 paramters that are not transformed.
    # alphas
    respy_params[("wage_a", "constant")] = kw94_params["alpha10"]
    respy_params[("wage_a", "exp_edu")] = kw94_params["alpha11"]
    respy_params[("wage_a", "exp_a")] = kw94_params["alpha12"]
    respy_params[("wage_a", "exp_b")] = kw94_params["alpha14"]

    respy_params[("wage_b", "constant")] = kw94_params["alpha20"]
    respy_params[("wage_b", "exp_edu")] = kw94_params["alpha21"]
    # second number behind alpha switched compared to above
    respy_params[("wage_b", "exp_a")] = kw94_params["alpha24"]
    respy_params[("wage_b", "exp_b")] = kw94_params["alpha22"]

    # betas
    respy_params[("nonpec_edu", "constant")] = kw94_params["beta0"]

    # gamma
    respy_params[("nonpec_home", "constant")] = kw94_params["gamma0"]

    return respy_params

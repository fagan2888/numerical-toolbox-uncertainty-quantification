import json

import numpy as np
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
    mean: array_like
        Vector of mean of input parameters.
    cov: array_like
        Covariance Matrix of input parameters distribution.
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
    qoi = [np.nan] * n_draws

    for i in range(n_draws):
        np.random.seed(i + 100)
        kw94_params = np.random.multivariate_normal(mean, cov)
        respy_params = transform_params_kw94_respy(kw94_params)
        qoi[i] = model_wrapper_kw_94(respy_params)

    if save_json is True:
        with open("json/qoi.json", "w") as write_file:
            json.dump(qoi, write_file)
    else:
        pass

    return qoi


def transform_params_kw94_respy(params):
    """
    Transforms parameters vector in format of KW94 (see table 4.1)
    to respy format. The difference is that KW94 specifyies the distribution of
    elements in a Cholesky Decomposition matrix but respy takes
    Standard deviations and Correlations.

    Parameters
    ----------
    params: array_like
        Vector of model input parameters in KW94 format.

    Returns
    -------
    params: array_like
        Vector of model input parameters in respy format.

    """
    chol = np.zeros((4, 4))
    np.fill_diagonal(chol, params[17:21])
    chol[1, 0] = params[21]
    chol[2, :2] = [params[22], params[23]]
    chol[3, :3] = [params[24], params[25], params[26]]

    cov = np.matmul(chol, chol.T)

    sd = np.sqrt(np.diag(cov))

    params[17:21] = sd
    params[21] = cov[1, 0] / (sd[1] * sd[0])
    params[22] = cov[2, 0] / (sd[2] * sd[0])
    params[23] = cov[2, 1] / (sd[2] * sd[1])
    params[24] = cov[3, 0] / (sd[3] * sd[0])
    params[25] = cov[3, 1] / (sd[3] * sd[1])
    params[26] = cov[3, 2] / (sd[3] * sd[2])

    return params

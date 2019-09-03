import numpy as np
from python.model_wrapper import model_wrapper_kw_94


def mc_uncertainty_propagation(mean, cov, n_draws):
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
        mc_params = mc_params = np.random.multivariate_normal(mean, cov)
        qoi[i] = model_wrapper_kw_94(mc_params)

    return qoi

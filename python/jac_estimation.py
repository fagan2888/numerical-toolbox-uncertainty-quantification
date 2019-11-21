"""
Estimates covariance matrix for KW94 Dataset 1 with Simulated Max. Likelihood.

"""

import json

import numpy as np
import pandas as pd
import respy as rp

from estimagic.inference.likelihood_covs import cov_jacobian
from estimagic.differentiation.differentiation import jacobian
from estimagic.optimization.optimize import maximize

from respy.likelihood import get_crit_func

def jac_estimation(save=False):
    """
    Estimates covariance matrix for KW94 Dataset 1 with Simulated Max. Likelihood.
    The Jacobian matrix is used instead of Hessian because its much faster.

    Parameters
    ----------
    save: Bool
        Indicates wether to save data.

    """
    # Df is sample of 1000 agents in 40 periods.
    params, options, df = rp.get_example_model("kw_94_one")
    
    # Log-likelihood function for sample of agents.
    log_like_obs_func = get_crit_func(params, options, df, version='log_like_obs')
    
    # Jacobian matrix.
    jacobian_matrix = jacobian(log_like_obs_func, params, extrapolation=False)
    
    # Drop zero lines to avoid multicollinearity for matrix inversion.
    jacobian_matrix = jacobian_matrix.loc[:, (jacobian_matrix != 0).any(axis=0)]
    
    jacobian_cov_matrix = cov_jacobian(jacobian_matrix.to_numpy())
    
    jacobian_cov_matrix = cov_jacobian(jacobian_matrix.to_numpy())
    
    # Calculate standard errors, last 3 cols are zeros.
    sd_df = pd.DataFrame(
        data=np.sqrt(np.diag(jacobian_cov_matrix)),
        index=params[:27].index,
        columns=["standard deviation"]
    )
    
    cov_df = pd.DataFrame(
    data=jacobian_cov_matrix,
    index=params[:27].index,
    columns=params[:27].index,
    )

    corr_df = cov_df.copy(deep=True)
    for i in range(0,len(cov_df)):
        for j in range(0,len(cov_df)):
            corr_df.iloc[i,j] = cov_df.iloc[i,j]/(
                np.sqrt(cov_df.iloc[i,i]*cov_df.iloc[j,j]))
    
    # Estimate parameters.
    # log_like = log_like_obs.mean(). Used for consistency with optimizers.
    # Gives log-likelihood function for mean agent.
    crit_func = rp.get_crit_func(params, options, df, "log_like")
    
    constr = rp.get_parameter_constraints("kw_94_one")
    
    _, par_estimates = maximize(
    crit_func,
    params,
    "scipy_L-BFGS-B",
    db_options={"rollover": 200},
    algo_options={"maxfun": 1},
    constraints=constr,
    dashboard=False
    )
    
    par_df = pd.DataFrame(
        data=par_estimates["value"].values[:27],
        index=params[:27].index,
        columns=["mean"]
    )

    if save is True:
        cov_df.to_csv("csv/est_cov.csv")
        corr_df.to_csv("csv/est_corr.csv")
        sd_df.to_csv("csv/est_sd.csv")
        par_df.to_csv("csv/est_parameters.csv")
    else:
        pass
    
    return par_df, cov_df, corr_df, sd_df













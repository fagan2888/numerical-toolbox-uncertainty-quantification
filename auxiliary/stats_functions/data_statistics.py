import pickle
import numpy as np

from stats_functions.education_statistics import education_statistics
from stats_functions.utility_statistics import utility_statistics

def data_replication(repl_df, repl_policy_df, n_edu_stats, n_groups):
    """
    This function computes the Quantitites of Interest (QoIs) when the Input
    Paramters of the model are set to their mean. It also computes the variances
    of the Monte Carlo sample of the QoIs that came from computation on a 
    random sample of input paramters.

    Parameters
    ----------
    repl_df: DataFrame
        Simulated agents given baseline parametrization
    repl_policy_df: DataFrame
        Simulated agents given mean policy parametrization
    n_edu_stats: int   
        number of education statistics that are computed
    n_groups: int
        number of type groups. Type group is an an attribute of
        QoIs/statistics which are used to condition on.

    Returns
    -------
    None: NoneType

    Notes
    -----
        The function saves the Qois under mean parametrization
        of the model input. It also saves the variance of the
        QoIs for the model evaluation of a Monte Carlo sample
        of input paramters under a specified policy.
        The data are saved as pickle in `/results`

    """

    repl_var_ratio = [None] * 2
    repl_var_ratio[0] = utility_statistics(repl_df) # utility_stats not a precise name
    repl_var_ratio[1] = utility_statistics(repl_policy_df)
    
    repl_edu_stats = np.full([2, n_edu_stats, n_groups], np.nan)  # (1,x,x) is subsidy sample
    repl_edu_stats[0, :, :] = education_statistics(repl_df)[1]
    repl_edu_stats[1, :, :] = education_statistics(repl_policy_df)[1]
    
    repl_policy_impact = np.full([n_edu_stats, n_groups], np.nan)
    repl_policy_impact = repl_edu_stats[1, :, :] - repl_edu_stats[0, :, :]
    # dump arrays to pickle
    with open('results/repl_var_ratio.pkl', 'wb') as f:
    	pickle.dump(repl_var_ratio, f)
    with open('results/repl_edu_stats.pkl', 'wb') as f:
    	pickle.dump(repl_edu_stats, f)
    with open('results/repl_policy_impact.pkl', 'wb') as f:
    	pickle.dump(repl_policy_impact, f)

    return None


def data_mc_compute_mean_and_variances(
        sample_policy_edu_stats, sample_policy_variance_ratio,
        n_edu_stats, n_groups, n_scenarios):
    """
    This function computes the mean and variances of each
    sample draw of the Quantities of Interest that was
    computed in the Monte Carlo Simulation. Variane and
    Mean are results of the Uncertainty Quantification
    in the narrow sense.

    Parameters
    ----------
        sample_policy_edu_stats: numpy.ndarray
            education statistics for each Monte Carlo draw of
            model input paramters that were propagated through
            the model
        sample_policy_variance_ratio: numpy.ndarray
            variance ratio for each Monte Carlo draw of
            model input paramters that were propagated through
            the model
        n_edu_stats: int
            number of education statistics
        n_groups: int
            number of types groups
        n_scenarios: int
            number of policy and baseline paramter and option
            specifications
    Returns
    -------
        None: None-Type

    Notes
    -----
        This function dumps the means and variances of the 
        Quantities of interest to '/results'.


    """
    
    # compute variances
    var_mc_var_ratio = [None] * n_scenarios
    var_mc_var_ratio[0] = np.var(sample_policy_variance_ratio)
    mean_mc_var_ratio = [None] * n_scenarios
    mean_mc_var_ratio[0] = np.mean(sample_policy_variance_ratio)   
    
    with open('results/var_mc_var_ratio.pkl', 'wb') as f:
        pickle.dump(var_mc_var_ratio, f)
    with open('results/mean_mc_var_ratio.pkl', 'wb') as f:
        pickle.dump(mean_mc_var_ratio, f)
    
    var_mc_policy_edu_stats = np.full([n_edu_stats, n_groups], np.nan)
    mean_mc_policy_edu_stats = np.full([n_edu_stats, n_groups], np.nan)
    # outside graphs loop for readability
    for j in range(n_edu_stats):
        for k in range(n_groups):
            var_mc_policy_edu_stats[j, k] = np.var(sample_policy_edu_stats[:, j, k])
            mean_mc_policy_edu_stats[j, k] = np.mean(sample_policy_edu_stats[:, j, k])
    with open('results/var_mc_policy_edu_stats.pkl', 'wb') as f:
        pickle.dump(var_mc_policy_edu_stats, f)
    with open('results/mean_mc_policy_edu_stats.pkl', 'wb') as f:
        pickle.dump(mean_mc_policy_edu_stats, f)

    return None
""" 
The module aims to replicate the education statistics in table14
and the variance ratio referring to table12 in Keane/Wolpin(1997).
It does not use any data from the Monte Carlo simulation of
input paramters that are propagated through the model.
The model is specified as the extended version in Keane/Wolpin(1997).
This module should be run before prior to visualization.py

"""

import respy as rp

from stats_functions.data_statistics import data_replication


# Set number of type groups and education stats
# according to `education_statistics`.
# n_groups is larger than in Monte Carlo module.
n_groups = 5
n_edu_stats = 4

# Write policy (dict) that specifies the paramters change in params (df)
policy = {'affected_paramter_loc': (
    'nonpec_edu', 'hs_graduate'), 'change': +2000}

# Initialize base parameters and options.
repl_params, options, _ = rp.get_example_model("kw_97_extended")

# Speed issue: Adjust number of sample agents in csv-files.
options['simulation_agents'] = 5000


# Simulate base dataframe
repl_df = rp.simulate(repl_params, options)[1]

# Initialze policy parameters by adding policy effect on desired paramters
repl_policy_params = repl_params.copy(deep=True)
repl_policy_params.loc[policy['affected_paramter_loc'], 'value'] += policy['change']

# Compute QoIs and variance of Qois for (mean) policy
# and baseline paramters and dump them as pickle
repl_policy_df = rp.simulate(repl_policy_params, options)[1]

execute_data_replication = data_replication(
        repl_df, repl_policy_df, n_edu_stats, n_groups)
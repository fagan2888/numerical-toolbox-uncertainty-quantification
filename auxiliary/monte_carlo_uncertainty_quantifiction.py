"""
This module
- creates a working covariance matrix for the model input paramter vector.
The covariance matrix consists only of nonzero values at the main diagonal
for return parameters to guarantee solvability and simulability.
- samples a number of draws from the joint normal distribution of the input
paramter vector according to its mean vector and cocariance matrix.
- Each input paramter vector draw is propagated through the model, i.e.
1000 agents are sampled (speed issue) and Quantities of Interest, i.e. the
impact of a policy which reduces college tuition costs by 50% and the
between-type variance of value functions divided by the variance are computed.
The samples are dumped as picke to `/results`. 
- Additionally, the mean and variances of each QoI for the samples are
computed and dumped to the same location as pickles.
"""

import respy as rp
import numpy as np
import pickle

from stats_functions.education_statistics import education_statistics
from stats_functions.utility_statistics import utility_statistics
from stats_functions.data_statistics import data_mc_compute_mean_and_variances


# Set number of type groups and education stats
# according to `education_statistics`
n_groups = 1
n_edu_stats = 4

# Speed issue: number of scenaries = 1,
n_scenarios = 1

# Set number of monte carlo draws
n_draws = 1000

# Write policy (dict) that specifies the paramters change in params (df)
policy = {'affected_paramter_loc': (
    'nonpec_edu', 'hs_graduate'), 'change': +2000}

# Initialize base parameters and options
repl_params, options, _ = rp.get_example_model("kw_97_extended")

# Speed issue: Adjust number of sample agents in csv-files
options['simulation_agents'] = 5000

# Initialze policy parameters by adding policy effect on desired paramters
repl_policy_params = repl_params.copy(deep=True)
repl_policy_params.loc[policy['affected_paramter_loc'], 'value'] += policy['change']

# The policy paramters is the mean of the Monte Carlo paramters sample
policy_mean = repl_policy_params['value'].to_numpy()

# Simulate base dataframe
repl_df = rp.simulate(repl_params, options)[1]

# Compute base stats to prepare subtraction from all policy stats from sample
repl_edu_stats = np.full([n_edu_stats, n_groups], np.nan)
repl_edu_stats = education_statistics(repl_df)[0]

# Create fictional covariance matrix that creates some variance
# and does not raise errors.
# I.e. the variance of a long dense line of paramters equals a sensible number
cov = np.zeros((len(policy_mean), len(policy_mean)))
for i in range(46,61): #52 is index of affected paramter
    cov[i,i] = 1000

# Initialize sample of education statistics (QoI 1)
# (n_draws x 5 x 1)
sample_policy_edu_stats = np.full([n_draws, n_edu_stats, n_groups], np.nan)
# (n_draws x 1) 
temp_mc_edu_stats = np.full([n_edu_stats, n_groups], np.nan)

# Speed issue: variance ratio UQ only for policy model
sample_policy_variance_ratio = np.full([n_scenarios, n_draws], np.nan)

# Initialize temporary policy paramters vector; changes for each paramters draw 
temp_mc_policy_params = repl_policy_params.copy(deep=True)

# Monte Carlo loop
for i in range(n_draws):
    # Set new seed in each iteration because `respy.simulate` sets a seed
    # for each loop where the function is called
    np.random.seed(i+1000)
    # Get temporary random paramters vector
    temp_random_params_value = np.random.multivariate_normal(policy_mean, cov)
    # Insert it in parameter dataframe taken by `respy.simulate`
    temp_mc_policy_params['value'] = temp_random_params_value
    # Simulate temporary sample based on random parameters draw
    temp_mc_policy_df = rp.simulate(temp_mc_policy_params, options)[1]
    # Compute education statistics (QoI 1) based on temporary simulated sample
    temp_mc_edu_stats = education_statistics(temp_mc_policy_df)[0]
    # Subtract baseline QoIs to obtain policy effect
    sample_policy_edu_stats[i, :, :] = temp_mc_edu_stats - repl_edu_stats
    # # Compute variance ratio (QoI 2) based on temporary simulated sample
    sample_policy_variance_ratio[0, i] = utility_statistics(temp_mc_policy_df)
    # Keep track of process
    print(i)

# Dump intermediary MC results as pickle 
# (distplotting by calling extra function in jupyter notebook)
# because computation time is too long for a call in jupyter notebook
with open('intermediate_data/mc_sample_policy_edu.pkl', 'wb') as f:
    pickle.dump(sample_policy_edu_stats, f)

with open('intermediate_data/mc_sample_policy_ratio.pkl', 'wb') as f:
    pickle.dump(sample_policy_variance_ratio, f)

execute_vars_computation = data_mc_compute_mean_and_variances(
        sample_policy_edu_stats, sample_policy_variance_ratio,
        n_edu_stats, n_groups, n_scenarios)


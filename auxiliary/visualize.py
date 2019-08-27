"""
This module creates and saves costumized displots for the Monte Carlo
simulations of the quantities of interest, i.e. the education statistics
in table14 and the variance ratio that refers to table12.
It also creates Convergence Plots for the same QoIs that are depicted
in distplots.

It is crucial to set the number of draws equal to module
main_uq_monte_carlo.py

"""

import pickle
import matplotlib.pyplot as plt

from visualization.custom_distplot import custom_distplot
from visualization.convergence_plot import convergence_plot

#open pkls
with open('results/intermediate_data/mc_sample_policy_edu.pkl', 'rb') as f:
    sample_policy_edu_stats = pickle.load(f)
   
with open('results/intermediate_data/mc_sample_policy_ratio.pkl', 'rb') as f:
    sample_policy_variance_ratio = pickle.load(f)

with open('results/results/repl_policy_impact.pkl', 'rb') as f:
    repl_policy_impact = pickle.load(f)

with open('results/repl_var_ratio.pkl', 'rb') as f:
    repl_var_ratio = pickle.load(f)      

# set the number of draws equal to module main_uq_monte_carlo.py
n_draws = 1000
# Set number of type groups and education stats
# according to `education_statistics`
n_groups = 1
n_edu_stats = 4

# Speed issue: number of scenarios = 1: Subsidy only
n_scenarios = 1

colors = [(0, 0.4470, 0.7410), (0.8500, 0.3250, 0.0980), (
    0.9290, 0.6940, 0.1250), (0.4660, 0.6740, 0.1880)]
# Prepare xlabels and file-titles
# (Speed issue: Normally, attr_one = ['No Subsidy', 'Subsidy'])
attr_one = ['Subsidy']
attr_two = ['Percentage high school graduates',
            'Percentage college graduates', 'Mean schooling',
            'Mean years in college']
attr_three = ['All Types', 'Type 1', 'Type 2', 'Type 3', 'Type 4']

for i in range(n_scenarios):
	# Plot custom distplots for UQ of variance ratio (next to table12)
    dp_uq = custom_distplot(sample_policy_variance_ratio[i, :])
    plt.xlabel('Between-type-variance-to-variance ratio',
               fontsize=16, labelpad=10)
    temp_name = '{}{}_{}'.format(
        'results/graphs/', attr_one[i], 'variance_ratio.png')

    plt.savefig(temp_name.replace(" ", ""), bbox_inches="tight")
    plt.close()
    # Plot convergence plots
    plot_means = convergence_plot(
    	repl_var_ratio[1], sample_policy_variance_ratio[
    	i, :], 'Variance ratio', n_draws, (0.4940, 0.1840, 0.5560))
    temp_name = '{}_{}'.format('results/graphs/convergence','var_ratio') 
    plt.savefig(temp_name, bbox_inches="tight")
    
for j in range(n_edu_stats):
    for k in range(n_groups):
        # Plot custom distplot for UQ of education statistics (table 14)
        if j < 2:
            # scale to percentage values
            dp = custom_distplot(sample_policy_edu_stats[:, j, k]*100)
        else:
            dp = custom_distplot(sample_policy_edu_stats[:, j, k])
        plt.xlabel(attr_two[j], fontsize=16, labelpad=10)
        temp_name = '{}{}_{}{}'.format(
            'results/graphs/policy_impact_', attr_three[
                k], attr_two[j], '.png')

        plt.savefig(temp_name.replace(" ", ""), bbox_inches="tight")
        plt.close()
        # Plot convergence plots
        plot_means = convergence_plot(repl_policy_impact[
            j,k], sample_policy_edu_stats[:,j,k], attr_two[
            j], n_draws, colors[j])
        temp_name = '{}_{}'.format('results/graphs/convergence',attr_two[j]) 
        plt.savefig(temp_name, bbox_inches="tight")
       
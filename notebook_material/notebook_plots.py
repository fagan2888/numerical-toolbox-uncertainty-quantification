"""This module provides small plots functions for the jupyter notebook"""

import matplotlib.pyplot as plt
import seaborn as sns

def notebook_convergence_plot(mc_E, true_E, mc_Var, true_Var):
    """create convergence plot of Qoi"""
    plt.figure(figsize=(10, 7.5))
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    plt.title('Convergence Plot: Crude Monte Carlo Simulation', fontsize=18)
    plt.plot(abs_dev(mc_E, true_E), color=(0, 0.4470, 0.7410))
    plt.plot(abs_dev(mc_Var, true_Var), color=(0.8500, 0.3250, 0.0980))
    plt.ylim([0, 0.15])
    plt.legend(('Absolute Deviation Mean', 'Absolute Deviation Variance'),
               loc='upper right', fontsize=16, frameon=False)
    plt.xlabel('sample size', fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14);
    plt.show

def abs_dev(mc, true):
    """compute absolute deviation"""
    return abs(mc-true)

def notebook_histogram(samples):
    """create histogram of QoI"""
    plt.figure(figsize=(10, 7.5))
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    sns.distplot(samples, kde=False, bins = 10)
    plt.title('Histogram: Sample of propagated input paramters', fontsize=18)
    plt.xlabel('Value model output', fontsize=16)
    plt.ylabel('Number of observations in bin', fontsize=16)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14);
    plt.show()
#!/usr/bin/env python
"""This script creates the result for our Monte Carlo explorations."""
import os

# In this script we only have explicit use of MULTIPROCESSING as our level of parallelism. This
# needs to be done right at the beginning of the script.
update = {
    "NUMBA_NUM_THREADS": "1",
    "OMP_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
}
os.environ.update(update)

import multiprocessing as mp
import argparse

import chaospy as cp
import pandas as pd
import numpy as np
import respy as rp

from uq_auxiliary import transform_params_kw94_respy
from uq_auxiliary import get_quantitiy_of_interest
from uq_configurations import INPUT_DIR, RSLT_DIR
from uq_auxiliary import model_wrapper_kw_94


def run(args):

    # We need to take stock for baseline parameters and store them for future processing.
    base_params, base_options = rp.get_example_model("kw_94_one", with_data=False)
    edu, policy_df = model_wrapper_kw_94(base_params, base_options, 500)

    base_quantity = pd.DataFrame(edu, columns=['avg_schooling'], index=[0], dtype="float")
    base_quantity.to_pickle(RSLT_DIR / "base_quantity.uq.pkl")
    base_params.to_pickle(RSLT_DIR / "base_params.uq.pkl")

    # We need to set up the covariance matrix and the estimated parameters from the paper.
    df = pd.read_csv(f"{INPUT_DIR}/table41_kw_94.csv", sep=",")
    mean, cov = df["true"].values, np.diag((df["sd"] ** 2).values)

    # We are ready to draw the random points of evaluation.
    np.random.seed(args.seed)
    distribution = cp.MvNormal(loc=mean, scale=cov)

    samples = list()
    for _ in range(args.num_draws):
        samples.append(distribution.sample())

    quantities = mp.Pool(args.num_procs).map(get_quantitiy_of_interest, samples)

    # We now store the random parameters and the quantity of interest for further processing.
    index = pd.read_csv(f"{INPUT_DIR}/table41_kw_94.csv", sep=",")["parameter"].values

    params = list()
    for sample in samples:
        sample = pd.Series(data=sample, index=index)

        param_sample = pd.DataFrame(transform_params_kw94_respy(sample), columns=["value"])
        params.append(param_sample)
    mc_params = pd.concat(params, keys=range(args.num_draws), names=['iteration'])

    mc_quantities = pd.DataFrame(quantities, columns=['avg_schooling'], index=range(args.num_draws))
    mc_quantities.index.name = 'iteration'

    mc_quantities.to_pickle("mc_quantity.respy.pkl")
    mc_params.to_pickle("mc_params.respy.pkl")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Create results for UQ analysis.")

    parser.add_argument("-s", "--seed", action="store", dest="seed", default=123, type=int,
                        help="set seed for the analysis")

    parser.add_argument("-d", "--draws", action="store", dest="num_draws", default=5, type=int,
                        help="set number of draws")

    parser.add_argument("-p", "--procs", action="store", dest="num_procs", default=2, type=int,
                        help="set number of processes")

    args = parser.parse_args()

    run(args)
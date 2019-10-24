import numpy as np
import respy as rp

import pandas as pd

from uq_configurations import INPUT_DIR


def get_quantity_of_interest(sample):

    # We need the baseline options and a grid for the indices. It does not matter which of the
    # three KW94 specifications we use here.
    base_params, base_options = rp.get_example_model("kw_94_one", with_data=False)
    index = pd.read_csv(f"{INPUT_DIR}/table41_kw_94.csv", sep=",")["parameter"].values

    sample = pd.Series(data=sample, index=index)
    param_sample = transform_params_kw94_respy(sample)
    param_sample = pd.DataFrame(param_sample, columns=["value"])

    policy_edu, _ = model_wrapper_kw_94(param_sample, base_options, 500.0)
    base_edu, _ = model_wrapper_kw_94(param_sample, base_options, 0.0)

    return policy_edu - base_edu


def model_wrapper_kw_94(params, base_options, tuition_subsidy):
    # TODO: This needs to done only once during the whole script. However, this requires me to
    #  set up a more complicated structure for the parallelism and so we will simply postpone
    #  this until we have a more serious application.
    simulate = rp.get_simulate_func(params, base_options)

    policy_params = params.copy()
    policy_params.loc[("nonpec_edu", "at_least_twelve_exp_edu"), "value"] += tuition_subsidy
    policy_df = simulate(policy_params)

    edu = policy_df.groupby("Identifier")["Experience_Edu"].max().mean()

    return edu, policy_df


def transform_params_kw94_respy(kw94_params):

    assert len(kw94_params) == 26, "Length of KW94 vector must be 26."

    params, _ = rp.get_example_model("kw_94_one", with_data=False)

    rp_params = pd.Series(
        data=np.full(len(params["value"].values), np.nan), index=params.index
    )

    # Copy values that are not in KW94 from respy paramters.
    rp_params[("delta", "delta")] = params.loc[("delta", "delta"), "value"]
    rp_params[("meas_error", "sd_a")] = params.loc[("meas_error", "sd_a"), "value"]
    rp_params[("meas_error", "sd_b")] = params.loc[("meas_error", "sd_b"), "value"]
    rp_params[("lagged_choice_1_edu", "edu_ten")] = params.loc[
        ("lagged_choice_1_edu", "edu_ten"), "value"
    ]
    rp_params[("initial_exp_edu", "10")] = params.loc[
        ("initial_exp_edu", "10"), "value"
    ]
    rp_params[("maximum_exp", "edu")] = params.loc[("maximum_exp", "edu"), "value"]

    # Set values that are transformed with *(-1) by respy
    # square experiences alphas
    rp_params[("wage_a", "exp_a_square")] = -kw94_params["alpha13"]
    rp_params[("wage_a", "exp_b_square")] = -kw94_params["alpha15"]
    rp_params[("wage_b", "exp_b_square")] = -kw94_params["alpha23"]
    rp_params[("wage_b", "exp_a_square")] = -kw94_params["alpha25"]
    # betas
    rp_params[("nonpec_edu", "at_least_twelve_exp_edu")] = -kw94_params["beta1"]
    rp_params[("nonpec_edu", "not_edu_last_period")] = -kw94_params["beta2"]

    # Set SDs and Corrs that are Cholesky elements in KW94.
    chol = np.zeros((4, 4))
    np.fill_diagonal(chol, kw94_params[["a11", "a22", "a33", "a44"]])
    chol[1, 0] = kw94_params["a21"]
    chol[2, :2] = [kw94_params["a31"], kw94_params["a32"]]
    chol[3, :3] = [kw94_params["a41"], kw94_params["a42"], kw94_params["a43"]]

    cov = np.matmul(chol, chol.T)
    sd = np.sqrt(np.diag(cov))

    rp_params[("shocks_sdcorr", "sd_a")] = sd[0]
    rp_params[("shocks_sdcorr", "sd_b")] = sd[1]
    rp_params[("shocks_sdcorr", "sd_edu")] = sd[2]
    rp_params[("shocks_sdcorr", "sd_home")] = sd[3]
    rp_params[("shocks_sdcorr", "corr_b_a")] = cov[1, 0] / (sd[1] * sd[0])
    rp_params[("shocks_sdcorr", "corr_edu_a")] = cov[2, 0] / (sd[2] * sd[0])
    rp_params[("shocks_sdcorr", "corr_edu_b")] = cov[2, 1] / (sd[2] * sd[1])
    rp_params[("shocks_sdcorr", "corr_home_a")] = cov[3, 0] / (sd[3] * sd[0])
    rp_params[("shocks_sdcorr", "corr_home_b")] = cov[3, 1] / (sd[3] * sd[1])
    rp_params[("shocks_sdcorr", "corr_home_edu")] = cov[3, 2] / (sd[3] * sd[2])

    # Fill in KW94 paramters that are not transformed.
    # alphas
    rp_params[("wage_a", "constant")] = kw94_params["alpha10"]
    rp_params[("wage_a", "exp_edu")] = kw94_params["alpha11"]
    rp_params[("wage_a", "exp_a")] = kw94_params["alpha12"]
    rp_params[("wage_a", "exp_b")] = kw94_params["alpha14"]

    rp_params[("wage_b", "constant")] = kw94_params["alpha20"]
    rp_params[("wage_b", "exp_edu")] = kw94_params["alpha21"]
    # second number behind alpha switched compared to above
    rp_params[("wage_b", "exp_a")] = kw94_params["alpha24"]
    rp_params[("wage_b", "exp_b")] = kw94_params["alpha22"]

    # betas
    rp_params[("nonpec_edu", "constant")] = kw94_params["beta0"]

    # gamma
    rp_params[("nonpec_home", "constant")] = kw94_params["gamma0"]

    return rp_params

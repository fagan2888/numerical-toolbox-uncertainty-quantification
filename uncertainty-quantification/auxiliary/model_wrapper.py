import numpy as np
import pandas as pd
import respy as rp


def model_wrapper_kw_94(input_params):
    """Computes the Quantity of Interest (QoI) of some model given some input
    paramters. The model is the Dicrete Occupational Dynamic Programming Model
    in Keane and Wolpin (1994).

    Paramters
    ---------
    params: array_like
        Vector of 59 input parameters.

    Returns
    -------
    qoi: float
        Quantity of Interest.
        The QoI is the effect of a 500 dollar tuition subsidy on
        years of schooling. See table 6, page 668 in KW94.

    """
    # Check input_params
    assert len(input_params) == 59, "The Length of input_params must be 59"

    # Build simulate function. It can be reused as only parameters change.
    params, options = rp.get_example_model("kw_94_one", with_data=False)
    options["simulation_agents"] = 4000
    simulate = rp.get_simulate_func(params, options)

    tuition_subsidies = [0, 500]
    data_frames = []

    for tuition_subsidy in tuition_subsidies:
        params, _ = rp.get_example_model("kw_94_one", with_data=False)
        # Set paramters equal to input paramters.
        params["value"] = input_params
        params.loc[("nonpec_edu", "hs_graduate"), "value"] += tuition_subsidy
        data_frames.append(simulate(params))

    for df in data_frames:
        df["Bootstrap_Sample"] = pd.cut(df.Identifier, bins=40, labels=np.arange(1, 41))

    df_wo_ts = data_frames[0]
    df_w_ts = data_frames[1]

    # Split the sample in 40 parts.
    df_wo_ts["Bootstrap_Sample"] = pd.cut(
        df_wo_ts.Identifier, bins=40, labels=np.arange(1, 41)
    )
    df_w_ts["Bootstrap_Sample"] = pd.cut(
        df_w_ts.Identifier, bins=40, labels=np.arange(1, 41)
    )

    mean_exp_wo_ts = (
        df_wo_ts.loc[df_wo_ts.Period.eq(39), ["Bootstrap_Sample", "Experience_Edu"]]
        .groupby("Bootstrap_Sample")
        .mean()
    )
    mean_exp_w_ts = (
        df_w_ts.loc[df_w_ts.Period.eq(39), ["Bootstrap_Sample", "Experience_Edu"]]
        .groupby("Bootstrap_Sample")
        .mean()
    )

    diff = mean_exp_w_ts - mean_exp_wo_ts
    diff = diff.reset_index().set_index(["Bootstrap_Sample"]).stack()

    qoi = diff.mean()

    return qoi

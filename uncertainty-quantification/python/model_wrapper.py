import respy as rp


def model_wrapper_kw_94(input_params):
    """Computes the Quantity of Interest (QoI) of some model given some input
    paramters. The model is the Dicrete Occupational Dynamic Programming Model
    in Keane and Wolpin (1994) (abbreviated by KW94).

    Parameters
    ----------
    params: array_like
        Vector of 59 input parameters.

    Returns
    -------
    qoi_diff: float
        Quantity of Interest.
        The QoI is the effect of a 500 dollar tuition subsidy on
        years of schooling. See table 6, page 668 in KW94.

    Notes
    -----
    Different from KW94, the sample is not split in 40 subsamples but left as
    one. Yet, the mean over one large sample or 40 subsamples of the large
    sample is identical.

    """
    # Build simulate function. It can be reused as only parameters change.
    params, options = rp.get_example_model("kw_94_two", with_data=False)
    options["simulation_agents"] = 4000
    simulate = rp.get_simulate_func(params, options)

    # Check whether length of input_params is correct.
    assert len(input_params) == len(
        params["value"].to_numpy()
    ), "The number of input parameters must equal the number of model parameters."

    tuition_subsidies = [0, 1000]
    data_frames = []

    for tuition_subsidy in tuition_subsidies:
        params, _ = rp.get_example_model("kw_94_two", with_data=False)
        # Set paramters equal to input paramters.
        params["value"] = input_params
        params.loc[
            ("nonpec_edu", "at_least_twelve_exp_edu"), "value"
        ] += tuition_subsidy
        data_frames.append(simulate(params))

    df_wo_ts = data_frames[0]
    df_w_ts = data_frames[1]

    mean_exp_wo_ts = df_wo_ts.loc[df_wo_ts.Period.eq(39), ["Experience_Edu"]].mean()
    mean_exp_w_ts = df_w_ts.loc[df_w_ts.Period.eq(39), ["Experience_Edu"]].mean()

    qoi_diff = (mean_exp_w_ts - mean_exp_wo_ts).squeeze()

    return qoi_diff

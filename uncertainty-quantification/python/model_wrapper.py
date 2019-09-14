import respy as rp


def model_wrapper_kw_94(input_params, tuition_subsidy):
    """
    The model is the Dicrete Occupational Dynamic Programming Model
    in Keane and Wolpin (1994) (abbreviated by KW94). This function
    computes the mean years of education of a sample of agents when
    a specifyable college tuition subsidy is distributed.

    Parameters
    ----------
    params: array_like
        Vector of 59 input parameters.

    Returns
    -------
    edu: float
        Years of education when there is a tuition subsidy of
        specified value on years of college education.
        See table 6, page 668 in KW94.
    tuition_subsidy: float
        The tuition subsidy value

    Notes
    -----
    -Different from KW94, the sample is not split in 40 subsamples but left as
    one. Yet, the mean over one large sample or 40 subsamples of the large
    sample is identical.
    -Normally one would compute the Qoi entirely in this model wrapper.
    Since we want to pull out a reference number to prevent it from being
    computed on simulated data for each iteration this is not done here.

    """
    # Build simulate function. It can be reused as only parameters change.
    params, options = rp.get_example_model("kw_94_one", with_data=False)
    options["simulation_agents"] = 4000
    simulate = rp.get_simulate_func(params, options)

    # Check whether length of input_params is correct.
    assert len(input_params) == len(
        params["value"].to_numpy()
    ), "The number of input parameters must equal the number of model parameters."

    params_ts, _ = rp.get_example_model("kw_94_one", with_data=False)
    # Set paramters equal to input paramters.
    params_ts["value"] = input_params
    params_ts.loc[("nonpec_edu", "at_least_twelve_exp_edu"), "value"] += tuition_subsidy
    df_w_ts = simulate(params_ts)

    edu = df_w_ts.loc[df_w_ts.Period.eq(39), ["Experience_Edu"]].mean().squeeze()

    return edu

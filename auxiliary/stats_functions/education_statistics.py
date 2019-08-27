import numpy as np


def education_statistics(df):
    """
    Compute content of table 14 in Keane/Wolpin(1997).

    This function computes the Percentage of high school graduates, the
    Percentage of college graduates, the mean years of schooling and the mean
    years of college by occupation types and for all types taken together.
    The computations are run on a sample of agents in the format of the
    function output from `respy.simulate`

    Parameters
    ----------
    df: DataFrame
        sample of agents in the format of the function output from
        `respy.simulate`.

    Returns
    -------
    mc_statistics: numpy.ndarray
        Due to computation speed reasons, the Monte Carlo simulation
        of model input paramters that are propagated through the model
        only uses the education statistics for 'All Types' as
        Quantities of Interest.
    statistics: numpy.ndarray
        2d-array of the statistics in table 4. The rows are the means
        and percentages and the columns are the five different type
        groups. I.e:
        - the first row contains the percentage value of graduates for
        each type and for all types taken together.
        - the second row contains the percentage value of college
        graduates for the above groups.
        - the third row contains the mean value of schooling years for
        the above groups
        - the fourth row contains the mean value of college years for
        the above groups.
    Notes
    -----
		'mc_statistics a version of `statistics` that has been decreased
        in the second dimension. Only the statistics for "All Types" are
        contained to have less computation time in the Monte Carlo loops.
        Yet, 'statics' is used for the replication of the education
        statistics in table 14 using a deterministic model input vector
        with the values from the extended model in Keane/Wolpin(1997)

    """

    # get sample of agents in last period
    # assumes agents have the same maximal age
    df = df.loc[df['Period'] == df['Period'].max()]

    statistics = np.full([4, 5], np.nan)

    # compute values for all types
    statistics[0, 0] = sum(df.Experience_Edu >= 12) / len(df)
    statistics[1, 0] = sum(df.Experience_Edu >= 16) / len(df)
    statistics[2, 0] = sum(df.Experience_Edu >= 0) / len(df)
    statistics[3, 0] = (df[(df.Experience_Edu > 12)].sum()["Experience_Edu"]
                        - 12 * sum(df.Experience_Edu > 12)) / len(df)

    # compute type-specific values
    for i in range(0,4):
        statistics[0, i+1] = sum(sum(
            [(df.Experience_Edu >= 12) & (df.Type == i)])) / sum(df.Type == i)
        statistics[1, i+1] = sum(sum([(df.Experience_Edu >= 16) & (df.Type == i)
                                    ])) / sum(df.Type == i)
        statistics[2, i+1] = df[(df.Type == i)].sum()["Experience_Edu"] \
            / sum(df.Type == i)
        statistics[3, i+1] = (df[(df.Experience_Edu > 12) & (df.Type == i)
                               ].sum()["Experience_Edu"] - 12 * sum(
            (df.Experience_Edu > 12) & (df.Type == i))) / sum(df.Type == i)

    # Speed issue: Use only the "All Types" column for Monte Carlo simulation
    # Sustain second dimension equals one
    mc_statistics = np.full([4, 1], np.nan)
    mc_statistics[:, 0] = statistics[0:4,0]

    return mc_statistics, statistics

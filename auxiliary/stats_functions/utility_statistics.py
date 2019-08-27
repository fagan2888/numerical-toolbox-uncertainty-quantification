import numpy as np


def utility_statistics(df):
    """
    This function computes the ratio of between-type variance in expected
    lifetime utility to the total variance.

    It is assumed that expected lifetime utility means expected DISCOUNTED
    lifetime utlity and that this equals the value function which is equivalent
    to the maximum over the first period value functions for each occupation
    choice.

    Parameters
    ----------
    df: DataFrame
        sample of agents in the format of the function output from
        `respy.simulate`

    Returns
    -------
    ratio: float
        ratio of between-type variance in expected lifetime utility
        to the total variance.

    Raises
    ------
    AssertionError
        - If `abs(sum(type_weights) - 1)` is smaller/equals `0.02`
        - If `ratio` is smaller/equal `1`
        - If `within_group_var + bw_group_var - var` is smaller/equals 0.0001
    Notes
    -----
         In Keane/Wolpin(1997) the ratio equals 90%. Their figure is based on
         their simulated data which contains 5,000 observations.

    """

    # Compute Value Function as maximum over first period value functions for
    # each occupation choice
    df_temp = df[(df['Period'] == 0)].copy()
    df_temp['max_Value_Function'] = (np.nanmax(df_temp[
        ['Value_Function_A', 'Value_Function_B', 'Value_Function_Mil',
         'Value_Function_Edu', 'Value_Function_Home']], axis=1))

    # compute type/group weights used in between-type variance
    type_weights = ((df_temp.groupby('Type').size() /
                     df_temp['Type'].count())).to_numpy()
    assert abs(sum(type_weights) - 1) <= 0.02

    # compute mean of mean and type means
    mean_of_means = df_temp['max_Value_Function'].mean()
    type_means = df_temp.groupby(
        'Type')['max_Value_Function'].mean().to_numpy()

    # compute variance and between-type variance
    var = df_temp['max_Value_Function'].var()
    bw_group_var = np.full([1, 4], np.nan)
    bw_group_var = sum(np.multiply(
        type_weights, (type_means - mean_of_means)**2))

    # compute the variance ratio
    ratio = bw_group_var / var

    # Use law of total variance as validity check
    type_vars = df_temp.groupby(
        'Type')['max_Value_Function'].var().to_numpy()
    within_group_var = sum(np.multiply(
        type_weights, type_vars))
    assert within_group_var + bw_group_var - var <= 0.0001

    assert ratio <= 1


    return ratio

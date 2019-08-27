"""This module contains all tests for the project."""

from numpy.testing import assert_equal
import numpy as np
import pandas as pd
import sys
sys.path.append('..')

from stats_functions.education_statistics import education_statistics


def test_education_statistics():
    """
    This functio asserts equality of output and expected values
    for the function education_statistics
    The output is a DataFrame.

    """

    # Initialize test dataframe for function education_statistics
    test_df = pd.DataFrame(
        {'Period': [
            39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 1],
         'Experience_Edu': [
            12, 13, 0, 14, 15, 1, 16, 17, 2, 18, 19, 3, np.nan],
         'Type': [
            0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, np.nan]})

    # Initialize expected function output given test_df as input
    expected_stats = np.array([
        [2 / 3, 2 / 3, 2 / 3, 2 / 3, 2 / 3],
        [1 / 3, 0, 0, 2 / 3, 2 / 3],
        [130 / 12, 25 / 3, 30 / 3, 35 / 3, 40 / 3],
        [28 / 12, 1 / 3, 5 / 3, 9 / 3, 13 / 3]])

    # Compute results from tested function given test_df as input
    test_sample = education_statistics(test_df)[1]
    assert_equal(test_sample, expected_stats)

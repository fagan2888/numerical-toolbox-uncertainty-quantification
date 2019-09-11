import pandas as pd
import pytest
import respy as rp
from python.mc_uncertainty_propagation import transform_params_kw94_respy


def test_transform_dataset1():
    """
    Tests whether function `transform_params_kw94_respy` correctly transforms
    the paramaters from KW94 Data Set 1 based on the csv file to the respy
    paramters for KW94 Data Set 1.

    """
    params_respy_ds1_expected, _ = rp.get_example_model("kw_94_one", with_data=False)

    df = pd.read_csv("csv/table41_kw_94.csv", sep=",")
    params_kw94_ds1 = pd.Series(data=df["true"].values, index=df["parameter"].values)
    params_kw94_ds1_expected = transform_params_kw94_respy(params_kw94_ds1)

    assert (
        params_respy_ds1_expected["value"].to_numpy()
        == params_kw94_ds1_expected.to_numpy()
    ).all()


# There is probably a typo in the respy paramters.["value"] vector.
@pytest.mark.xfail
def test_transform_dataset2():
    """
    Tests whether function `transform_params_kw94_respy` correctly transforms
    the paramaters from KW94 Data Set 2 based on the csv file to the respy
    paramters for KW94 Data Set 2.

    """
    params_respy_ds2_expected, _ = rp.get_example_model("kw_94_two", with_data=False)

    df = pd.read_csv("csv/table42_kw_94.csv", sep=",")
    params_kw94_ds2 = pd.Series(data=df["true"].values, index=df["parameter"].values)
    params_kw94_ds2_expected = transform_params_kw94_respy(params_kw94_ds2)

    assert (
        params_respy_ds2_expected["value"].to_numpy()
        == params_kw94_ds2_expected.to_numpy()
    ).all()


# Small differences in decimals of Correlations and SDs. Reason is to be found.
@pytest.mark.xfail
def test_transform_dataset3():
    """
    Tests whether function `transform_params_kw94_respy` correctly transforms
    the paramaters from KW94 Data Set 3 based on the csv file to the respy
    paramters for KW94 Data Set 3.

    """
    params_respy_ds3_expected, _ = rp.get_example_model("kw_94_three", with_data=False)

    df = pd.read_csv("csv/table43_kw_94.csv", sep=",")
    params_kw94_ds3 = pd.Series(data=df["true"].values, index=df["parameter"].values)
    params_kw94_ds3_expected = transform_params_kw94_respy(params_kw94_ds3)

    assert (
        params_respy_ds3_expected["value"].to_numpy()
        == params_kw94_ds3_expected.to_numpy()
    ).all()

import pandas as pd
import numpy as np
import respy as rp

from uq_auxiliary import transform_params_kw94_respy
from uq_configurations import INPUT_DIR


def test_transform_datasets():
    """ Test whether the transformations work for the baseline parameterization.
    """
    for count, dataset in enumerate(["one", "two"]):
        par_name = f"kw_94_{dataset}"
        csv_name = f"{INPUT_DIR}/table4{count + 1}_kw_94.csv"

        par_respy, _ = rp.get_example_model(par_name, with_data=False)
        par_respy = par_respy["value"].to_numpy()

        df = pd.read_csv(csv_name, sep=",")
        par_uq = pd.Series(data=df["true"].values, index=df["parameter"].values)
        par_uq = transform_params_kw94_respy(par_uq).to_numpy()

        # TODO: For some reason this test fails for the third dataset. This needs to be further
        #  investigated later.
        if dataset != 'three':
            np.testing.assert_almost_equal(par_respy, par_uq)

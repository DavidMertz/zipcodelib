"""Function to lookup values associated with a zip code

This module's function is inserted into the parent namespace
"""

from glob import glob
from os.path import dirname
import pandas as pd


def lookup(zc):
    "Function to lookup values associated with a zip code"
    dir = dirname(__file__)
    dfs = []
    for feature_set in glob("%s/features/*.csv" % dir):
        df = pd.read_csv(feature_set, dtype={"ZIPCODE": str})
        df.set_index("ZIPCODE", inplace=True)
        df.index.name = "ZIPCODE"
        dfs.append(df)

    combo = pd.concat(dfs, axis=1, sort=False)
    return combo.loc[zc]

from os.path import dirname
import pandas as pd

from ..util import download


def _run(use_cached=True):
    """Plugin to generate the MEAN_AGI and NUM_RETURNS features

    Based on IRS data.

    Note: As of 2019-01, year 2015 is the most recent data
    that is formatted correcly. 2016 exists, but has errors.
    Later years have not yet been published.
    """
    url = "https://www.irs.gov/pub/irs-soi/15zpallnoagi.csv"

    # No progress bar; content-length misreported in HTTP header
    fname = download(url, use_cached=use_cached, progress=False)

    df = pd.read_csv(fname, dtype={"ZIPCODE": str})
    df.set_index("ZIPCODE", inplace=True)
    df.index.name = "ZIPCODE"
    df = df[["A00100", "N1"]]
    df["N1"] = df.N1.astype(int)
    # The units here are odd! What is reported is aggregate AGI
    # for entire zipcode, in 1000s of dollars. Calculate per-capita
    df["MEAN_AGI"] = 1000 * df.A00100 / df.N1
    df.drop(["A00100"], axis=1, inplace=True)
    df.columns = ["NUM_RETURNS", "MEAN_AGI"]
    df.sort_index(inplace=True)

    # The IRS data is messy in several ways, including having
    # "zip codes" 00000 and 99999 with many rows of each.  Best
    # to drop that ambiguuous data (maybe it represents miscoded
    # zip codes in those missing, but it is unclear)
    df = df[~df.index.duplicated()]

    dir = dirname(__file__)
    df.to_csv("%s/../features/IRS.csv" % dir)

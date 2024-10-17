from time import time
from os.path import dirname
import pandas as pd

# TODO: Decide how meta-loaders will assure base loaders have run
# ... as a temporary fix, we just hope for cached files available


def _run(use_cached=True):
    """Plugin to generate the POPULATION_DENSITY feature

    This is a "meta-loader" in that in creates a synthetic
    feature from other datasets.  load_lat_long() gets us land
    area; load_household() gets us population.
    """
    start = time()
    dir = dirname(__file__)
    print("Generating synthetic feature POPULATION_DENSITY...")
    demog = pd.read_csv("%s/../features/demographic.csv" % dir, dtype={"ZIPCODE": str})
    geo = pd.read_csv("%s/../features/geography.csv" % dir, dtype={"ZIPCODE": str})
    demog = demog.set_index("ZIPCODE")
    geo = geo.set_index("ZIPCODE")
    combo = pd.concat([geo, demog], axis=1, join="inner")
    combo["POPULATION_DENSITY"] = combo.POPULATION / combo.LAND_AREA
    combo.sort_index(inplace=True)
    combo[["POPULATION_DENSITY"]].to_csv("%s/../features/pop_density.csv" % dir)
    print("Completed in %.1f seconds" % (time() - start))

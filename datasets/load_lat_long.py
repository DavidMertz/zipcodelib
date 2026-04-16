import zipfile
from os.path import dirname, abspath
import pandas as pd

# Add the project root to the path so we can import util
import sys
sys.path.insert(0, abspath(dirname(__file__) + "/.."))

from util import download


def _run(use_cached=True):
    """Plugin to generate features LATITUDE, LONGITUDE, LAND_AREA

    Based on US Census Bureau data
    """
    domain = "http://www2.census.gov/"
    path = "geo/docs/maps-data/data/gazetteer/2025_Gazetteer/"
    zipfname = "2025_Gaz_zcta_national.zip"
    url = domain + path + zipfname
    dir = dirname(__file__)

    fname = download(url, use_cached=use_cached)
    zipfile.ZipFile(fname).extractall(path="%s/../cache" % dir)
    datafile = fname.replace(".zip", ".txt")

    df = pd.read_csv(datafile, dtype={"GEOID": str}, sep="|")
    df = df.set_index("GEOID")
    df.index.name = "ZIPCODE"
    df.columns = [col.strip() for col in df.columns]
    df = df[["INTPTLAT", "INTPTLONG", "ALAND_SQMI"]]
    df.columns = ["LATITUDE", "LONGITUDE", "LAND_AREA"]
    df.sort_index(inplace=True)
    df.to_csv("%s/../features/geography.csv" % dir)

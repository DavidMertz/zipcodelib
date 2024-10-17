import zipfile
from os.path import dirname
import pandas as pd

from ..util import download


def _run(use_cached=True):
    """Plugin to generate features LATITUDE, LONGITUDE, LAND_AREA

    Based on US Census Bureau data
    """
    domain = "http://www2.census.gov/"
    path = "geo/docs/maps-data/data/gazetteer/2018_Gazetteer/"
    zipfname = "2018_Gaz_zcta_national.zip"
    url = domain + path + zipfname
    dir = dirname(__file__)

    fname = download(url, use_cached=use_cached)
    zipfile.ZipFile(fname).extractall(path="%s/../cache" % dir)
    datafile = fname.replace(".zip", ".txt")

    df = pd.read_csv(datafile, dtype={"GEOID": str}, sep="\t")
    df.set_index("GEOID", inplace=True)
    df.index.name = "ZIPCODE"
    df.columns = [col.strip() for col in df.columns]
    df = df[["INTPTLAT", "INTPTLONG", "ALAND_SQMI"]]
    df.columns = ["LATITUDE", "LONGITUDE", "LAND_AREA"]
    df.sort_index(inplace=True)
    df.to_csv("%s/../features/geography.csv" % dir)

from time import time
from os.path import dirname
import pandas as pd

# Data was obtained from the US Census Bureau, starting at:
#
#     https://factfinder.census.gov/faces/tableservices/
#
# This site requires selection and navigation of table features
# within a web browser, and does not provide a RESTful interface in
# any obvious way.

key = {
    "GEO.id": "Id",
    "GEO.id2": "Id2",
    "GEO.display-label": "Geography",
    "HD01_S001": "Number; SEX AND AGE - Total population",
    "HD01_S020": "Number; SEX AND AGE - Total population - Median age (years)",
    "HD01_S076": "Number; RACE - Total population",
    "HD01_S095": "Number; RACE - Total population - Two or More Races",
    "HD01_S099": "Number; RACE - Total population - Two or More Races - White; Some Other Race [3]",
    "HD01_S100": "Number; RACE - Race alone or in combination with one or more other races: [4] - White",
    "HD01_S101": "Number; RACE - Race alone or in combination with one or more other races: [4] - Black or African American",
    "HD01_S102": "Number; RACE - Race alone or in combination with one or more other races: [4] - American Indian and Alaska Native",
    "HD01_S103": "Number; RACE - Race alone or in combination with one or more other races: [4] - Asian",
    "HD01_S104": "Number; RACE - Race alone or in combination with one or more other races: [4] - Native Hawaiian and Other Pacific Islander",
    "HD01_S105": "Number; RACE - Race alone or in combination with one or more other races: [4] - Some Other Race",
    "HD01_S106": "Number; HISPANIC OR LATINO - Total population",
    "HD01_S107": "Number; HISPANIC OR LATINO - Total population - Hispanic or Latino (of any race)",
    "HD01_S112": "Number; HISPANIC OR LATINO - Total population - Not Hispanic or Latino",
    "HD01_S130": "Number; RELATIONSHIP - Total population",
    "HD01_S131": "Number; RELATIONSHIP - Total population - In households",
    "HD01_S134": "Number; RELATIONSHIP - Total population - In households - Child",
    "HD01_S136": "Number; RELATIONSHIP - Total population - In households - Other relatives",
    "HD01_S138": "Number; RELATIONSHIP - Total population - In households - Other relatives - 65 years and over",
    "HD01_S139": "Number; RELATIONSHIP - Total population - In households - Nonrelatives",
    "HD01_S142": "Number; RELATIONSHIP - Total population - In households - Nonrelatives - Unmarried partner",
    "HD01_S143": "Number; RELATIONSHIP - Total population - In group quarters",
    "HD01_S144": "Number; RELATIONSHIP - Total population - In group quarters - Institutionalized population",
    "HD01_S146": "Number; RELATIONSHIP - Total population - In group quarters - Institutionalized population - Female",
    "HD01_S147": "Number; RELATIONSHIP - Total population - In group quarters - Noninstitutionalized population",
    "HD01_S149": "Number; RELATIONSHIP - Total population - In group quarters - Noninstitutionalized population - Female",
    "HD01_S150": "Number; HOUSEHOLDS BY TYPE - Total households",
    "HD01_S151": "Number; HOUSEHOLDS BY TYPE - Total households - Family households (families) [7]",
    "HD01_S153": "Number; HOUSEHOLDS BY TYPE - Total households - Family households (families) [7] - Husband-wife family",
    "HD01_S154": "Number; HOUSEHOLDS BY TYPE - Total households - Family households (families) [7] - Husband-wife family - With own children under 18 years",
    "HD01_S155": "Number; HOUSEHOLDS BY TYPE - Total households - Family households (families) [7] - Male householder, no wife present",
    "HD01_S156": "Number; HOUSEHOLDS BY TYPE - Total households - Family households (families) [7] - Male householder, no wife present - With own children under 18 years",
    "HD01_S157": "Number; HOUSEHOLDS BY TYPE - Total households - Family households (families) [7] - Female householder, no husband present",
    "HD01_S158": "Number; HOUSEHOLDS BY TYPE - Total households - Family households (families) [7] - Female householder, no husband present - With own children under 18 years",
    "HD01_S159": "Number; HOUSEHOLDS BY TYPE - Total households - Nonfamily households [7]",
    "HD01_S160": "Number; HOUSEHOLDS BY TYPE - Total households - Nonfamily households [7] - Householder living alone",
    "HD01_S161": "Number; HOUSEHOLDS BY TYPE - Total households - Nonfamily households [7] - Householder living alone - Male",
    "HD01_S162": "Number; HOUSEHOLDS BY TYPE - Total households - Nonfamily households [7] - Householder living alone - Male - 65 years and over",
    "HD01_S163": "Number; HOUSEHOLDS BY TYPE - Total households - Nonfamily households [7] - Householder living alone - Female",
    "HD01_S164": "Number; HOUSEHOLDS BY TYPE - Total households - Nonfamily households [7] - Householder living alone - Female - 65 years and over",
    "HD01_S167": "Number; HOUSEHOLDS BY TYPE - Total households - Average household size",
    "HD01_S168": "Number; HOUSEHOLDS BY TYPE - Total households - Average family size [7]",
    "HD01_S169": "Number; HOUSING OCCUPANCY - Total housing units",
    "HD01_S171": "Number; HOUSING OCCUPANCY - Total housing units - Vacant housing units",
    "HD01_S177": "Number; HOUSING OCCUPANCY - Total housing units - Vacant housing units - All other vacants",
    "HD01_S180": "Number; HOUSING TENURE - Occupied housing units",
    "HD01_S181": "Number; HOUSING TENURE - Occupied housing units - Owner-occupied housing units",
    "HD01_S183": "Number; HOUSING TENURE - Occupied housing units - Owner-occupied housing units - Average household size of owner-occupied units",
    "HD01_S184": "Number; HOUSING TENURE - Occupied housing units - Renter-occupied housing units",
    "HD01_S186": "Number; HOUSING TENURE - Occupied housing units - Renter-occupied housing units - Average household size of renter-occupied units",
}


def _run(use_cached=True):
    """Plugin to generate numerous demographic features

    Based on US Census Bureau data.

    This is a "static loader" in that it utilizes a data source that was
    somewhat manually downloaded to the project directories
    """
    start = time()
    dir = dirname(__file__)
    print("Generating demographic features from US Census data...")

    df = pd.read_csv(
        "%s/../tuned_data/DEC_10_DP_DPDP1_with_ann.csv" % dir,
        header=None,
        skiprows=2,
        names=list(key),
    )

    zipcodes = df["GEO.display-label"].str.replace("ZCTA5 ", "")
    population = df.HD01_S001
    median_age = df.HD01_S020
    white_percentage = 100 * df.HD01_S100 / population
    black_percentage = 100 * df.HD01_S101 / population
    indian_percentage = 100 * df.HD01_S102 / population
    asian_percentage = 100 * df.HD01_S103 / population
    hawaiian_percentage = 100 * df.HD01_S104 / population
    hispanic_percentage = 100 * df.HD01_S107 / population
    child_percentage = 100 * df.HD01_S134 / population
    household_size = df.HD01_S167
    live_alone_percentage = 100 * df.HD01_S159 / population

    demographic = pd.DataFrame(
        {
            "ZIPCODE": zipcodes,
            "POPULATION": population,
            "MEDIAN_AGE": median_age,
            "WHITE_PERCENTAGE": white_percentage,
            "BLACK_PERCENTAGE": black_percentage,
            "INDIAN_PERCENTAGE": indian_percentage,
            "ASIAN_PERCENTAGE": asian_percentage,
            "HAWAIIAN_PERCENTAGE": hawaiian_percentage,
            "HISPANIC_PERCENTAGE": hispanic_percentage,
            "CHILD_PERCENTAGE": child_percentage,
            "HOUSEHOLD_SIZE": household_size,
            "LIVE_ALONE_PERCENTAGE": live_alone_percentage,
        }
    )
    demographic.set_index("ZIPCODE", inplace=True)
    demographic.index.name = "ZIPCODE"

    demographic.sort_index(inplace=True)
    demographic.to_csv("%s/../features/demographic.csv" % dir)
    print("Completed in %.1f seconds" % (time() - start))

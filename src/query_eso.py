import pandas as pd
import pyvo
from astropy.coordinates import SkyCoord
import astropy.units as u

# connect to ESO tap service
ESO_TAP_URL = "https://archive.eso.org/tap_obs"
service = pyvo.dal.TAPService(ESO_TAP_URL)

def query_star(ra, dec):

    # convert coordinates in catalogue to degrees in decimal
    coords = SkyCoord(ra, dec, unit=(u.hourangle, u.deg))

    ra_deg = coords.ra.deg
    dec_deg = coords.dec.deg

    # query ESO portal using ra_deg and dec_deg
    # ask rik about ADQL, what the hell
    query = f"""
    SELECT
    """
    result = service.search(query)

    # convert ESO result to pandas
    observations_df = result.to_table().to_pandas()

    return observations_df

def query_catalogue(catalogue_path):

    stars = pd.read_csv(catalogue_path)

    results = []

    # ignore the row index, iterate through stars
    for _, star in stars.iterrows():

        name = star["Name"]
        ra = star["RAJ2000"]
        dec = star["DEJ2000"]

        observations = query_star(ra, dec)

        observations["catalogue_target"] = name

        results.append(observations)

    # combine into one big inventory dataframe
    inventory = pd.concat(results, ignore_index = True)

    return inventory
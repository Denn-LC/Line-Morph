
import pandas as pd
from astropy.coordinates import SkyCoord
import astropy.units as u
from utils.clean_eso import clean_eso


def match_stars(catalogue_path, eso_path, ra_col, dec_col, instrument = None):

    stars = pd.read_csv(catalogue_path)
    observations = clean_eso(eso_path)

    # filter by instrument if specified
    if instrument is not None:
        observations = observations[observations["ins_id"] == instrument]

    # convert catalogue coords to skycoord
    star_coords = SkyCoord(
        ra = stars[ra_col].astype(str).to_numpy(),
        dec = stars[dec_col].astype(str).to_numpy(),
        unit = (u.hourangle, u.deg)
    )

    # ESO coordinates are already in degrees
    eso_coords = SkyCoord(
        ra = observations["ra"].to_numpy() * u.deg,
        dec = observations["dec"].to_numpy() * u.deg
    )

    # find the nearest catalogue star for each ESO observation
    index, separation, _ = eso_coords.match_to_catalog_sky(star_coords)

    # only keep matches within 5 arcseconds
    matched = separation < 5 * u.arcsec

    observations = observations[matched].copy()

    # Add the matched star name and angular separation
    observations["Name"] = stars.iloc[index[matched]]["Name"].to_numpy()
    observations["separation_arcsec"] = separation[matched].arcsec

    return observations

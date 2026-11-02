
import pandas as pd
import matplotlib.pyplot as plt
from utils.match_stars import match_stars


def plot_teff(catalogue_path, eso_path, ra_col, dec_col, name,
              instrument = "XSHOOTER", arm = "NIR"):

    stars = pd.read_csv(catalogue_path)

    # match ESO observations to catalogue stars
    observations = match_stars(
        catalogue_path,
        eso_path,
        ra_col,
        dec_col,
        instrument = instrument
    )

    # filter by spectral arm if asked in arg
    if arm is not None:
        observations = observations[
            observations["obs_title"].str.contains(f"_{arm}_", na=False)
        ]

    # get unique observed stars
    observed_names = observations["Name"].unique()
    observed_stars = stars[stars["Name"].isin(observed_names)]

    # get temperatures, drop empty
    temperatures = observed_stars["Teff"].dropna()

    print(f"{name}: {len(temperatures)} stars observed with {instrument}, {arm}")

    # plot teff
    plt.hist(temperatures, bins = 12, edgecolor="black")
    plt.xlabel("Temperature (K)")
    plt.ylabel("Number of stars")
    plt.title(f"{name} {instrument} {arm} (n = {len(temperatures)})")
    plt.tight_layout()
    plt.savefig(
        f"figures/{name.lower()}/{name.lower()}_{str(instrument).lower()}_{str(arm).lower()}_teff.png"
    )
    plt.close()

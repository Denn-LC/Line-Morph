import pandas as pd
import os
import matplotlib.pyplot as plt
from utils.clean_eso import clean_eso

def plot_teff(catalogue_path, eso_path, name, arm = "NIR"):

    stars = pd.read_csv(catalogue_path)
    eso_stars = clean_eso(eso_path)

    # get xshooter observations, then keep the near infrared ones
    xshooter = eso_stars[eso_stars["ins_id"] == "XSHOOTER"]
    observations = xshooter[xshooter["obs_title"].str.contains(f"_{arm}_", na = False)]

    # remove all caps, spaces and hypens so names all match
    star_names = stars["Name"].str.replace(r"[\s-]", "", regex = True).str.lower()
    eso_names = observations["obj"].str.replace(r"[\s-]", "", regex = True).str.lower()

    # only keep stars in nir region
    observed_stars = stars[star_names.isin(eso_names)]

    # plot temperatures and save the figure
    temperatures = observed_stars["Teff"].dropna()

    print(f"{name}: {len(temperatures)} stars with {arm} observations")

    plt.hist(temperatures, bins = 12, edgecolor = "black")
    plt.xlabel("Temperature (K)")
    plt.ylabel("Number of stars")
    plt.title(f"{name} X-Shooter {arm} (n = {len(temperatures)})")
    plt.tight_layout()
    # make the folder if it doesnt exist already
    os.makedirs(f"figures/{name.lower()}", exist_ok=True)
    plt.savefig(f"figures/{name.lower()}/{name.lower()}_{arm.lower()}_teff.png")
    plt.close()
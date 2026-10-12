import pandas as pd
import matplotlib.pyplot as plt
from utils.clean_eso import clean_eso

stars = pd.read_csv("data/catalogues/fairlamb_2015.csv")
eso_stars = clean_eso("data/fairlamb_2015_eso_export.csv")

# get xshooter observations, then keep the near infrared ones
print(eso_stars["ins_id"].unique())
xshooter = eso_stars[eso_stars["ins_id"] == "XSHOOTER"]
nir = xshooter[xshooter["obs_title"].str.contains("_NIR_", na = False)]

# remove all caps, spaces and hypens so names all match
star_names = stars["Name"].str.replace(r"[\s-]", "", regex = True).str.lower()
nir_names = nir["obj"].str.replace(r"[\s-]", "", regex = True).str.lower()

# only keep stars in nir region
observed_stars = stars[star_names.isin(nir_names)]

# plot temperatures and save the figure

# test
print("ESO rows:", len(eso_stars))
print("X-shooter rows:", len(xshooter))
print("NIR rows:", len(nir))
print("Matched stars:", len(observed_stars))
print("Temperatures:", observed_stars["Teff"].head())

plt.hist(observed_stars["Teff"], bins = 10, edgecolor = "black")
plt.xlabel("Temperature (K)")
plt.ylabel("Number of stars")
plt.tight_layout()
plt.savefig("figures/temperature_histogram.png")
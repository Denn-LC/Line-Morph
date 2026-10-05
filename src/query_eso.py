import pandas as pd
import pyvo

# Create and connect to ESO tap object
ESO_TAP_URL = "https://archive.eso.org/tap_obs"
service = pyvo.dal.TAPService(ESO_TAP_URL)

stars = pd.read_csv("data/catalogues/fairlamb_2015.csv")

first_star=stars.iloc[0]

print(first_star["Name"])
print(first_star["RAJ2000"])
print(first_star["DEJ2000"])
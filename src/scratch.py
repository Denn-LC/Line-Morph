from utils.csv_to_eso import csv_to_eso

csv_to_eso(
    "data/catalogues/vioque/vioque2018_high.csv",
    "data/catalogues/vioque/vioque2018_high_eso.csv",
    "RAICRS",
    "DEICRS"
)

csv_to_eso(
    "data/catalogues/vioque/vioque2018_low.csv",
    "data/catalogues/vioque/vioque2018_low_eso.csv",
    "RAICRS",
    "DEICRS"
)
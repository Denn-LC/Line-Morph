
import pandas as pd
from utils.match_stars import match_stars


def main():

    catalogue_path = "data/catalogues/vioque/vioque_2018.csv"
    eso_path = "data/catalogues/vioque/vioque_2018_observations.csv"

    stars = pd.read_csv(catalogue_path)

    observations = match_stars(
        catalogue_path,
        eso_path,
        "RAICRS",
        "DEICRS",
        instrument="XSHOOTER"
    )

    # Keep only NIR observations
    nir = observations[
        observations["obs_title"].str.contains("_NIR_", na=False)
    ]

    target = nir[nir["Name"].str.strip() == "Hen 3-938"]

    print(target.to_string(index=False))

    # Count observations for each star
    counts = nir.groupby("Name").size()

    # Add observation counts to the catalogue
    stars["NIR_count"] = stars["Name"].map(counts).fillna(0).astype(int)

    # Keep stars with NIR observations
    stars = stars[stars["NIR_count"] > 0]

    # Sort from hottest to coolest
    stars = stars.sort_values("Teff", ascending=False)

    print(stars[["Name", "Teff", "NIR_count"]].head(20).to_string(index=False))


if __name__ == "__main__":
    main()

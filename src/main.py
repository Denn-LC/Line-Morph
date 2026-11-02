from utils.match_stars import match_stars


def main():
    observations = match_stars(
        "data/catalogues/vioque/vioque_2018.csv",
        "data/catalogues/vioque/vioque_2018_observations.csv",
        "RAICRS",
        "DEICRS",
        instrument="XSHOOTER"
    )

    print("Observations:", len(observations))
    print("Unique stars:", observations["Name"].nunique())
    print(observations["separation_arcsec"].describe())
    nir = observations[
    observations["obs_title"].str.contains("_NIR_", na=False)
    ]

    print("NIR observations:", len(nir))
    print("NIR unique stars:", nir["Name"].nunique())

    print(
    observations[["Name", "obj", "separation_arcsec"]]
    .sort_values("separation_arcsec", ascending=False)
    .head(10)
    )

    print(
    observations.groupby("Name")["separation_arcsec"]
    .min()
    .describe()
    )

    for radius in [3, 4, 5, 7, 10]:
        subset = observations[observations["separation_arcsec"] < radius]

        print(f"{radius} arcsec: {subset['Name'].nunique()} stars, {len(subset)} observations")

if __name__ == "__main__":
    main()
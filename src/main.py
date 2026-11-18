
from astropy.io import fits
import matplotlib.pyplot as plt

def main():
    path = "data/processed/reflex/hen3-938/NIR/reflex_end_products/molecfit/XSHOOTER/2026-11-12T16:52:25/ADP.2024-02-29T08:05:55.704/Hen_3-938_SCIENCE_TELLURIC_CORR.fits"

    with fits.open(path) as hdul:
        data = hdul["TELLURIC_DATA"].data

        # Molecfit wavelengths are in micrometres
        wavelength = data["lambda"] * 1000  # convert to nm

        original = data["flux"]
        corrected = data["cflux"]

    
    # Only plot the wavelengths we're interested in
    mask = (wavelength >= 1270) & (wavelength <= 1295)

    plt.plot(wavelength[mask], original[mask], label="Original")
    plt.plot(wavelength[mask], corrected[mask], label="Corrected")

    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Flux")
    plt.title("Hen 3-938: Pa-beta")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()

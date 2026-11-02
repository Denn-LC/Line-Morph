
from astropy.io import fits
import matplotlib.pyplot as plt


def main():
    path = "data/spectra/hen3-938/NIR/ADP.2024-02-29T08:05:55.704.fits"

    with fits.open(path) as hdul:
        hdul.info()

        spectrum = hdul[1].data
        print(spectrum.names)

        wavelength = spectrum["WAVE"][0]
        flux = spectrum["FLUX"][0]

        print("Wavelength range:", wavelength.min(), wavelength.max())
        print("Wavelength unit:", hdul[1].columns["WAVE"].unit)
        print("Flux unit:", hdul[1].columns["FLUX"].unit)

        plt.plot(wavelength, flux, linewidth=0.7)

        plt.xlim(2150, 2180)
        plt.axvline(2166.1, color="red", linestyle="--", label="Br-gamma rest wavelength")

        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Flux")
        plt.title("Hen 3-938: Br-gamma (NIR)")
        plt.legend()
        plt.show()

if __name__ == "__main__":
    main()

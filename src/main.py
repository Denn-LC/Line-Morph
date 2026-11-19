
import matplotlib.pyplot as plt
from astropy.io import fits

def main():
    path = "data/processed/hen3-938/ADP.2024-02-29T08:05:55.704_corrected.fits"

    with fits.open(path) as hdus:
        data = hdus["TELLURIC_DATA"].data
        wavelength = data["lambda"] * 1000  # µm to nm
        near_helium = (wavelength >= 1075) & (wavelength <= 1090)

        plt.plot(wavelength[near_helium], data["flux"][near_helium], label="Original")
        plt.plot(wavelength[near_helium], data["cflux"][near_helium], label="Corrected")


    
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Flux")
    plt.title("Hen 3-938 · He I")
    plt.legend()
    plt.tight_layout()
    plt.xlim(1080, 1086)
    plt.ylim(1e-14, 4e-14)
    plt.show()

if __name__ == "__main__":
    main()

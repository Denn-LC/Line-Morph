import sqlite3
import matplotlib.pyplot as plt
import numpy as np

from dataclasses import dataclass
from astropy.io import fits
from contextlib import closing

@dataclass
class NormalizedSpectrum:
    wavelength: np.ndarray
    flux: np.ndarray
    continuum: np.ndarray
    normalized_flux: np.ndarray
    fit_pixels: np.ndarray
    converged: bool


def normalize(
    path,
    window = (1075.0, 1090.0),
    exclude = (),
    degree = 2,
    sigma = 3.0,
    max_passes = 10,
):
    with fits.open(path) as hdus:
        data = hdus["TELLURIC_DATA"].data
        wavelength = np.asarray(data["lambda"], dtype = float) * 1000  # convert µm to nm
        flux = np.asarray(data["cflux"], dtype = float)

    lo, hi = window
    in_window = (wavelength >= lo) & (wavelength <= hi)
    if not in_window.any():
        raise ValueError(f"{path}: no data in the {lo}-{hi} nm window")

    wavelength = wavelength[in_window]
    flux = flux[in_window]
    x = wavelength - wavelength.mean()

    finite_flux = np.isfinite(flux)
    fit_pixels = finite_flux.copy()

    # excluded line pixels stay in the spectrum and are not part of the fit
    for lo, hi in exclude:
        fit_pixels &= (wavelength < lo) | (wavelength > hi)

    converged = False

    for passes in range(max_passes + 1):
        if np.unique(x[fit_pixels]).size < degree + 1:
            raise ValueError(f"{path}: too few distinct wavelengths for the fit")

        coefficients = np.polyfit(x[fit_pixels], flux[fit_pixels], degree)
        continuum = np.polyval(coefficients, x)

        residuals = flux - continuum
        scatter = residuals[fit_pixels].std()

        if scatter == 0:
            converged = True
            break

        next_pixels = fit_pixels & (np.abs(residuals) <= sigma * scatter)

        if np.array_equal(next_pixels, fit_pixels):
            converged = True
            break

        if passes == max_passes:
            break

        fit_pixels = next_pixels

    if np.any(~np.isfinite(continuum) | (continuum <= 0)): # if any continuum value is non-finite, zero, or negative, reject the fit
        raise ValueError(f"{path}: fitted continuum must be finite and positive")

    normalized_flux = np.full_like(flux, np.nan)
    normalized_flux[finite_flux] = flux[finite_flux] / continuum[finite_flux]

    return NormalizedSpectrum(
        wavelength=wavelength,
        flux = flux,
        continuum = continuum,
        normalized_flux = normalized_flux,
        fit_pixels = fit_pixels,
        converged = converged,
    )

import sqlite3
from contextlib import closing


def save_normalized_spectrum(spectrum, star_id, product_id, corrected_path):
    with closing(sqlite3.connect("data/line_morph.sqlite")) as db, db:
        db.executescript("""
            PRAGMA foreign_keys = ON;

            CREATE TABLE IF NOT EXISTS observations (
                product_id TEXT PRIMARY KEY,
                star_id TEXT NOT NULL,
                corrected_path TEXT NOT NULL,
                converged INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS profile_pixels (
                product_id TEXT NOT NULL REFERENCES observations(product_id),
                pixel_index INTEGER NOT NULL,
                wavelength_nm REAL NOT NULL,
                corrected_flux REAL,
                continuum REAL NOT NULL,
                normalized_flux REAL,
                used_in_fit INTEGER NOT NULL,
                PRIMARY KEY (product_id, pixel_index)
            );
        """)

        db.execute("""
            INSERT INTO observations VALUES (?, ?, ?, ?)
            ON CONFLICT(product_id) DO UPDATE SET
                star_id = excluded.star_id,
                corrected_path = excluded.corrected_path,
                converged = excluded.converged
        """, (product_id, star_id, str(corrected_path), int(spectrum.converged)))

        pixels = zip(
            spectrum.wavelength,
            spectrum.flux,
            spectrum.continuum,
            spectrum.normalized_flux,
            spectrum.fit_pixels,
            strict = True,
        )

        db.execute("DELETE FROM profile_pixels WHERE product_id = ?", (product_id,))
        db.executemany(
            "INSERT INTO profile_pixels VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                (product_id, i, wave, flux, continuum, normalized, int(used))
                for i, (wave, flux, continuum, normalized, used) in enumerate(pixels)
            ),
        )

def plot_normalization(spectrum, title = "He I 1083 nm"):
    wave = spectrum.wavelength
    used = spectrum.fit_pixels

    fig, (ax_fit, ax_profile) = plt.subplots(2, 1, sharex=True)

    ax_fit.plot(wave, spectrum.flux, label = "Corrected flux")
    ax_fit.plot(wave, spectrum.continuum, label = "Continuum")
    ax_fit.scatter(wave[used], spectrum.flux[used], s = 8, label = "Fit pixels")
    ax_fit.set(title = title, ylabel = "Flux")
    ax_fit.legend()

    ax_profile.plot(wave, spectrum.normalized_flux)
    ax_profile.axhline(1, linestyle = "--")
    ax_profile.set(xlabel = "Wavelength (nm)", ylabel = "Normalised flux")

    fig.tight_layout()
    return fig